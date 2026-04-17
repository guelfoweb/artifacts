import os
import shutil
import hashlib
import logging
from apkInspector.headers import ZipEntry

logging.basicConfig(level=logging.WARNING)

CONFLICTS_DIR = "__apk_path_conflicts__"


def _path_conflicts_from_names(names):
    """Return file paths that are also used as parent directories."""
    files = [name.rstrip("/") for name in names if name and not name.endswith("/")]
    file_set = set(files)
    conflicts = set()

    for name in files:
        parts = name.split("/")
        prefix = ""
        for part in parts[:-1]:
            prefix = part if not prefix else f"{prefix}/{part}"
            if prefix in file_set:
                conflicts.add(prefix)

    return conflicts


def _path_conflicts_in_apk(apkfile):
    with open(apkfile, "rb") as apk_stream:
        zip_entry = ZipEntry.parse(apk_stream)
        names = zip_entry.namelist()
    return _path_conflicts_from_names(names)


def _rewrite_conflicting_path(name, conflicts):
    for conflict in sorted(conflicts, key=len, reverse=True):
        prefix = f"{conflict}/"
        if name.startswith(prefix):
            suffix = name[len(prefix):]
            return f"{CONFLICTS_DIR}/{conflict}/{suffix}"
    return name


def _sanitize_member_path(path):
    parts = []
    for part in path.replace("\\", "/").split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            parts.append("__up__")
        else:
            parts.append(part)
    return os.path.join(*parts) if parts else None


def _extract_apk_safe(apkfile, folder, conflicts=None):
    """Fallback extraction for tampered APKs with file/directory path collisions."""
    for entry in os.listdir(folder):
        full_path = os.path.join(folder, entry)
        if os.path.isdir(full_path):
            shutil.rmtree(full_path, ignore_errors=True)
        else:
            os.remove(full_path)

    with open(apkfile, "rb") as apk_stream:
        zip_entry = ZipEntry.parse(apk_stream)
        names = [name for name in zip_entry.namelist() if name and not name.endswith("/")]

        if conflicts is None:
            conflicts = _path_conflicts_from_names(names)
        for name in names:
            mapped_name = _rewrite_conflicting_path(name, conflicts)
            relative_path = _sanitize_member_path(mapped_name)
            if not relative_path:
                continue

            output_path = os.path.join(folder, relative_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as output_file:
                output_file.write(zip_entry.read(name))

def validateAPK(apkfile):
    # first 4 bytes APK, JAR (ZIP, XLSM): 
    # 50 4b 03 04
    header = "504b0304"
    with open(apkfile, 'rb') as file:
        byte = file.read(4)
        if not header == bytes(byte).hex():
            return False
        return True

def extractAPK(apkfile, folder):
    if not validateAPK(apkfile):
        print(f"The file {apkfile} under analysis is not an APK, I will proceed with the analysis if it is a DEX.")
        shutil.copy(apkfile, folder)
        return

    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)

    apk_label = os.path.splitext(os.path.basename(apkfile))[0]

    try:
        with open(apkfile, "rb") as apk_stream:
            zip_entry = ZipEntry.parse(apk_stream)
            result_code = zip_entry.extract_all(folder, apk_label)
    except Exception as exc:
        print(f"[WARNING] apkInspector extraction failed ({exc}). Falling back to safe mode.")
        logging.warning("apkInspector extraction failed (%s). Retrying in safe mode.", exc)
        _extract_apk_safe(apkfile, folder)
        return

    if result_code not in (0, 2, None):
        print(
            f"[WARNING] apkInspector returned code {result_code}. "
            "Falling back to safe mode."
        )
        logging.warning(
            "apkInspector extract_all returned code %s. Retrying in safe mode.",
            result_code
        )
        _extract_apk_safe(apkfile, folder)
        return

    extracted_files = list(os.scandir(folder))
    if not extracted_files:
        print("[WARNING] apkInspector reported success but no files were extracted. Falling back to safe mode.")
        logging.warning("apkInspector reported success but no files were extracted. Retrying in safe mode.")
        _extract_apk_safe(apkfile, folder)
        return

    if apk_label:
        nested_dir = os.path.join(folder, apk_label)
        if os.path.isdir(nested_dir):
            for entry in os.listdir(nested_dir):
                src = os.path.join(nested_dir, entry)
                dst = os.path.join(folder, entry)
                if os.path.exists(dst):
                    os.remove(dst) if os.path.isfile(dst) else shutil.rmtree(dst)
                shutil.move(src, dst)
            shutil.rmtree(nested_dir, ignore_errors=True)

    return

def hashAPK(apkfile, algorithms=("md5", "sha1", "sha256")):
    if isinstance(algorithms, str):
        algorithms = [algorithms]

    hashers = {algo: hashlib.new(algo) for algo in algorithms}

    with open(apkfile, 'rb') as f:
        while chunk := f.read(8192):
            for hasher in hashers.values():
                hasher.update(chunk)

    return {algo: hasher.hexdigest() for algo, hasher in hashers.items()}

def md5APK(apkfile):
    return hashAPK(apkfile, "md5")["md5"]
