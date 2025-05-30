import re
import ipaddress
from . import match_regex

def get(filepaths):
    regex = {
        "ip": r"[^A-Za-z0-9\.]([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})[^A-Za-z0-9\.]",
        "url": r"[A-Za-z]+://[a-zA-Z0-9./?=_%:-]*",
        "param": r"model=|result=|androidid=|upload=|&upload|action=|&action|bot=|&bot|gate=|&gate|\w+\.php\?",
    }

    exclude = [
        ".android.com", "apache.org", "publicsuffix.org", "mozilla.org", "fontawesome.io",
        "googleapis.com", "googleadservices.com", ".googlesyndication.com",
        ".google-analytics.com", ".google.com", "com.google.", "goo.gl",
        "googleads.", ".adobe.com", ".doubleclick.net", ".apache.org", "purl.org",
        "gimp.org", ".w3.org", "schema.org", "firebase.com", "googletagmanager.com",
        "gstatic.com", "googlesource.com"
    ]

    result = {key: match_regex.inFolder(filepaths, pattern, exclude) for key, pattern in regex.items()}

    # Validate and clean URLs
    if result["url"]:
        url_pattern = re.compile(r"((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}")
        result["url"] = [
            re.sub(r'^(https?://)?(http)', r'\1', url)  # Fix malformed URLs
            for url in result["url"]
            if url_pattern.search(url)
        ]

    # Validate and clean IP addresses
    if result["ip"]:
        result["ip"] = [
            ip for ip in result["ip"]
            if not (ip.startswith("0.") or ip.endswith(".0.0"))
            and is_valid_ip(ip)
        ]

    # Filter out empty strings in each result list
    result = {key: list(filter(None, values)) for key, values in result.items()}

    return result

def is_valid_ip(ip):
    """Check if an IP address is valid."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
