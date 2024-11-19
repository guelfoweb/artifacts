import hashlib
import zipfile
import os

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
    with zipfile.ZipFile(apkfile, 'r') as zip_ref:
        for name in zip_ref.namelist():
            target_path = os.path.join(folder, name)
            
            # Check if a file or directory with the same name already exists
            if os.path.exists(target_path):
                # If it's a directory, rename it
                if os.path.isdir(target_path):
                    new_target_path = target_path + "_folder"
                    os.rename(target_path, new_target_path)
                    print(f"Renamed folder '{target_path}' to '{new_target_path}'")
            
            try:
                # Attempt to extract individual file
                zip_ref.extract(name, folder)
            except zipfile.BadZipFile as e:
                # This exception is raised when the ZIP file is corrupt or not a valid ZIP archive.
                print(f"Zip error for {name}: {e}")
            except NotImplementedError as e:
                # Raised when the ZIP file uses a compression method not supported by `zipfile`
                print(f"Skipping {name}: {e}")
            except RecursionError as e:
                # This occurs if there is infinite recursion during path resolution or directory creation,
                # likely caused by malformed ZIP entries or logical errors in handling paths.
                print(f"Skipping {name}: {e}")
            except NotADirectoryError as e:
                # Raised when trying to perform an operation on a directory, but a file is expected (or vice versa).
                # This can happen if the extracted file structure conflicts with existing files or directories.
                print(f"Not A Directory Error {name}: {e}")
            except OSError as e:
                # This is a broad exception for file system-related errors, such as permission issues,
                # path length limits, or invalid file names.
                print(f"OSError for {name}: {e}")
        
def md5APK(apkfile):
    with open(apkfile, 'rb') as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()
