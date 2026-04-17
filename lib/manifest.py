import os
import re
from typing import Dict, List, Optional, Union
from xml.etree import ElementTree as ET

from apkInspector.axml import parse_apk_for_manifest

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"


def _launcher_activity(root: ET.Element) -> Optional[str]:
    def get_name(element: ET.Element) -> Optional[str]:
        return element.attrib.get(f"{ANDROID_NS}name")

    activities = []
    for app_node in root.findall("application"):
        activities.extend(app_node.findall("activity"))

    for activity in activities:
        for intent_filter in activity.findall("intent-filter"):
            actions = {
                node.attrib.get(f"{ANDROID_NS}name")
                for node in intent_filter.findall("action")
            }
            categories = {
                node.attrib.get(f"{ANDROID_NS}name")
                for node in intent_filter.findall("category")
            }
            if (
                "android.intent.action.MAIN" in actions
                and "android.intent.category.LAUNCHER" in categories
            ):
                name = get_name(activity)
                if name:
                    return name

    for activity in activities:
        name = get_name(activity)
        if name:
            return name

    return None


def _normalize_component_name(name: str, package_name: Optional[str]) -> str:
    if not name:
        return ""
    if name.startswith(".") and package_name:
        return f"{package_name}{name}"
    if "." not in name and package_name:
        return f"{package_name}.{name}"
    return name


def _collect_component_names(root: ET.Element, package_name: Optional[str]) -> List[str]:
    targets = ("activity", "activity-alias", "service", "receiver", "provider")
    attrs = (f"{ANDROID_NS}name", f"{ANDROID_NS}targetActivity")
    names = set()

    for app_node in root.findall("application"):
        app_name = app_node.attrib.get(f"{ANDROID_NS}name")
        if app_name:
            names.add(_normalize_component_name(app_name, package_name))

        for tag in targets:
            for node in app_node.findall(tag):
                for attr in attrs:
                    value = node.attrib.get(attr)
                    if value:
                        normalized = _normalize_component_name(value, package_name)
                        if normalized:
                            names.add(normalized)

    return sorted(names, key=str.casefold)


def _clean_xml_for_parsing(xml_text: str) -> str:
    """Drop characters that are not valid in XML 1.0 documents."""
    def is_valid_xml_char(char: str) -> bool:
        code = ord(char)
        return (
            code in (0x9, 0xA, 0xD)
            or 0x20 <= code <= 0xD7FF
            or 0xE000 <= code <= 0xFFFD
            or 0x10000 <= code <= 0x10FFFF
        )

    return "".join(ch for ch in xml_text if is_valid_xml_char(ch))


def info(apk_path: str) -> Dict[str, Union[List[str], str]]:
    """Extract manifest metadata directly from the APK using apkInspector."""
    result: Dict[str, Union[List[str], str]] = {}

    if not apk_path or not os.path.isfile(apk_path):
        return result

    try:
        # Context: apkInspector CLI (`apkInspector -apk sample.apk -m`) also relies on parse_apk_for_manifest
        manifest_xml = parse_apk_for_manifest(apk_path, raw=False)
    except Exception:
        return result

    if not manifest_xml:
        return result

    if isinstance(manifest_xml, bytes):
        manifest_xml = manifest_xml.decode("utf-8", errors="ignore")

    manifest_xml_clean = _clean_xml_for_parsing(manifest_xml)

    try:
        root = ET.fromstring(manifest_xml_clean)
    except ET.ParseError:
        root = None

    if root is not None:
        package_name = root.attrib.get("package")
        if package_name:
            result["package_name"] = package_name

        launcher = _launcher_activity(root)
        if launcher:
            result["main_activity"] = launcher

        component_names = _collect_component_names(root, package_name)
        if component_names:
            result["application"] = component_names

    regex = {
        "permission": r"android\.permission\.[A-Z_]+",
    }

    for key, pattern in regex.items():
        matches = sorted({match for match in re.findall(pattern, manifest_xml_clean)}, key=str.casefold)
        result[key] = matches

    if "application" not in result:
        generic_app_regex = r"[A-Za-z0-9_]+\.[A-Za-z0-9_.]+"
        disallowed_prefixes = ("android.permission.", "android.intent.", "android.content.")
        fallback_matches = {
            match
            for match in re.findall(generic_app_regex, manifest_xml_clean)
            if not match.startswith(disallowed_prefixes)
        }
        fallback = sorted(fallback_matches, key=str.casefold)
        if fallback:
            result["application"] = fallback

    return result
