import hashlib
import zipfile

"""
def createTempDir():
	if not os.path.isdir(folder):
		os.makedirs(folder)
	else:
		os.remove(folder)
"""

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
		try:
			zip_ref.extractall(folder)
		except: # OSError: [Errno 36] File name too long
			for name in zip_ref.namelist():
				try:
					zip_ref.extractall(name, folder)
				except: #zipfile.BadZipFile as e:
					#print ("Zip error:", name)
					pass
	
def md5APK(apkfile):
	with open(apkfile, 'rb') as f:
		file_hash = hashlib.md5()
		while chunk := f.read(8192):
			file_hash.update(chunk)
	return file_hash.hexdigest()