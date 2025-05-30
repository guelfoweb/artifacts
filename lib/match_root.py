from . import match_regex

def info(filepaths):
	"""Search for root-related paths in the specified folder."""
	regex = {
		"root": r"/sbin/|/system/bin/|/system/xbin/|/system/sd/xbin/|/system/bin/failsafe/|/data/local/xbin/|/data/local/bin/|/data/local/",
	}
	
	exclude = []

	return match_regex.inFolder(filepaths, regex["root"], exclude)


