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
                print(f"Zip error for {name}: {e}")
            except NotImplementedError as e:
                print(f"Skipping {name}: {e}")
            except OSError as e:
                print(f"OSError for {name}: {e}")
    
def md5APK(apkfile):
    with open(apkfile, 'rb') as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()