from . import match_regex

def info(folder):
	# root
	regex = {
		"root": "/sbin/|/system/bin/|/system/xbin/|/system/sd/xbin/|/system/bin/failsafe/|/data/local/xbin/|/data/local/bin/|/data/local/",
	}
	
	exclude = []

	return match_regex.inFolder(folder, regex["root"], exclude)


