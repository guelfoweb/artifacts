import os
from . import search_file
from . import match_regex

def info(folder):
	if not search_file.filename(folder, 'AndroidManifest.xml'):
		print ("NO MANIFEST")
		return {}

	# when AndroidManifest.xml exists but it is a folder
	manifest_path = os.path.join(folder, 'AndroidManifest.xml')
	if not os.path.isfile(manifest_path):
		return {}

	regex = {
		"permission": "android.permission.[A-Z_]*",
		"application": r"com\.[A-Za-z0-9.]*"
		}

	result = {}

	# get permission and application
	for item in regex.keys():
		match = match_regex.inFile(os.path.join(folder, 'AndroidManifest.xml'), regex[item])
		result.update({item: sorted(match)})

	return result