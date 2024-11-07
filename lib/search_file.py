import os

def extension(folder, ext):
    """Recursively search for files with the specified extension."""
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames if os.path.splitext(f)[1] == ext]

def filename(folder, file):
    """Recursively search for files with the specified filename (without extension)."""
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames if os.path.splitext(f)[0] in file]

# return sorted list
def extension_sort(folder, ext):
    """Return a sorted list of files with the specified extension, relative to the folder."""
    files = extension(folder, ext)
    files.sort()
    return [os.path.relpath(f, start=folder) for f in files]
