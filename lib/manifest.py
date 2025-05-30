import os
from . import search_file
from . import match_regex

def info(filepaths):
    result = {}

    # Check AndroidManifest.xml in filepaths
    manifest_files = search_file.filename(filepaths, ['AndroidManifest.xml'])
    
    if not manifest_files:
        #print("NO MANIFEST")
        return result
    
    # Get first AndroidManifest.xml
    manifest_path = manifest_files[0]
    
    # Check that it is a file
    if not os.path.isfile(manifest_path):
        return result
    
    regex = {
        "permission": "android.permission.[A-Z_]*",
        "application": r"com\.[A-Za-z0-9.]*"
    }
    
    # get permissions and applications
    for item in regex.keys():
        match = match_regex.inFile(manifest_path, regex[item])
        result.update({item: sorted(match)})
    
    return result