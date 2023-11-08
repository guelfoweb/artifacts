import os

def extension(folder, ext):
	# search file extension recursively
	# I use it for .dex
	return [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames if os.path.splitext(f)[1] == ext]

def filename(folder, file):
	# search filename (+extension) recursively
	# I use it for AndrodiManifest.txt
	return [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames if os.path.splitext(f)[0] in file]


# return sorted list
def extension_sort(folder, ext):
	files = extension(folder, ext)
	if files:
		files.sort()
		file_list = [f.replace(folder+'/', '') for f in files]
		return file_list
	return files
