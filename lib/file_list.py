import os
import re

def get(folder):
    """Searches for regex matches in all files of a folder recursively."""
    exclude_extensions = re.compile(r'\.(ttf|png|SF|MF|dylib|jar|otf)$')
    
    result = set()
    filepaths = [
        os.path.join(dp, f) for dp, _, filenames in os.walk(folder) 
        for f in filenames if not exclude_extensions.search(f) and '.' in f
    ]

    return filepaths