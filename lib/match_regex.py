import os
import re
import concurrent.futures

def _ascii(file):
	with open(file, 'rb') as f:
		data = f.read().decode('ascii', errors='ignore')
	return data

def _utf16(file):
	with open(file, 'rb') as f:
		data = f.read().decode('utf-16-le', 'ignore')
	return data

def inFile(file, regex):
	# search regex in single file
	try:
		data = _ascii(file)
		encode = 'ascii'
	except:		
		# AndroidManifest.xml is a Android Binary XML
		data = _utf16(file)
		encode = 'utf-16-le'

	result = re.findall(regex, data)

	if file.endswith('AndroidManifest.xml') and not result:
		if encode == 'utf-16-le':
			data = _ascii(file)
		else:
			data = _utf16(file)

	result = re.findall(regex, data)

	return result

def inFolder(folder, regex, exclude=False):
	# search regex recursively
	exclude_extension_file = ('.ttf', '.png', '.SF', '.MF', 
							  '.dylib', '.jar', '.otf')
	garbage = ['publicsuffixes.gz', 'plus.log', 'internal.log']

	result = []
	filepaths = []

	for dp, dn, filenames in os.walk(folder):
		for f in filenames:
			if '.' not in f:
				continue
			filepath = os.path.join(dp, f)
			if filepath.endswith(exclude_extension_file):
				continue
			filepaths.append(filepath)
	
	with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
		results_executor = {executor.submit(inFile, filepath, regex) for filepath in filepaths}

	for item in concurrent.futures.as_completed(results_executor):
		match = item.result()
		if match:
			for m in match:
				if m not in result and m not in garbage:
					result.append(m)
	
	results = result.copy()
	
	# case exclude list from results
	if result and exclude:
		for r in result:
			for e in exclude:
				if e in r:
					if r in results:
						results.remove(r)
					continue
	return results