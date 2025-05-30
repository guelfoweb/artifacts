import os
import re
import concurrent.futures

def _decode_file(file, encodings=('ascii', 'utf-16-le')):
    """Attempts to decode the file content using the specified encodings."""
    for encoding in encodings:
        try:
            with open(file, 'rb') as f:
                return f.read().decode(encoding, errors='ignore')
        except (UnicodeDecodeError, OSError):
            continue
    return ""

def inFile(file, regex):
    """Searches for regex matches in a single file."""
    data = _decode_file(file)
    result = re.findall(regex, data)
    
    if file.endswith('AndroidManifest.xml') and not result:
        # Retry decoding if no result in AndroidManifest.xml
        data = _decode_file(file, encodings=('utf-16-le', 'ascii'))
        result = re.findall(regex, data)
    
    return result

def inFolder(filepaths, regex, exclude=False):    
    # Concurrent execution
    result = set()
    garbage = {'publicsuffixes.gz', 'plus.log', 'internal.log'}

    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        futures = {executor.submit(inFile, filepath, regex) for filepath in filepaths}

    for future in concurrent.futures.as_completed(futures):
        matches = future.result()
        if matches:
            result.update(m for m in matches if m not in garbage)
    
    # Handle exclude list
    if exclude:
        result = {r for r in result if not any(e in r for e in exclude)}
    
    return list(result)
