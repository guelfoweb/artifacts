import os
from . import apk_file

def extension(filepaths, ext):
    """Filter files with the specified extension from a list of filepaths."""
    return [fp.replace('_tmp','') for fp in filepaths if os.path.splitext(fp)[1] == ext]

def filename(filepaths, file):
    """Filter files with the specified filename from a list of filepaths."""
    return [fp for fp in filepaths if os.path.basename(fp) in file]

def extension_sort(filepaths, ext):
    """Return a sorted list of files with the specified extension from a list of filepaths."""
    files = extension(filepaths, ext)
    files.sort()
    return files

def search_archive(filepaths):
    """Return list of archives (ZIP, APK, etc.)"""
    return [filepath.replace('_tmp','') for filepath in filepaths if apk_file.validateAPK(filepath)]