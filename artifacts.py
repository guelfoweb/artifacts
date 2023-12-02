import os
import sys
import json
import time
import shutil
import argparse

from lib import apk_file, json_file, search_file, intent, manifest
from lib import match_strings, match_regex, match_network, match_root
from lib import sandbox, similarity, report

__version__ = '1.0.7'

# 1.0.7 added similarity table with prettytable dependency
# 1.0.6 fixed jaccard similarity coefficient and added updatedb
# 1.0.5 checks if decoded base64 string matches the regex
# 1.0.4 decodes base64 strings
# 1.0.3 fixed permission non found in result["activity"]["permission"]
# 1.0.2 fixed extractAPK file name too long
# 1.0.1 added details to family
# 1.0.0 start project

def main():
	parser = argparse.ArgumentParser(prog="artifacts", description="apk analysis")

	# args
	parser.add_argument("apkfile", nargs='?', help="apk to analyze")
	parser.add_argument("-v", "--version", action="version", version="%(prog)s " + __version__)
	parser.add_argument("-r", "--report", help="add report to json result", action="store_true", required=False)
	parser.add_argument("-s", "--similarity", help="get similarities", action="store_true", required=False)
	parser.add_argument("--updatedb", help="update database with a new family", dest="family", required=False)
	args = parser.parse_args()

	apkfile = args.apkfile

	# check if the domain name is correct
	if not apkfile or not os.path.isfile(apkfile) or not apk_file.validateAPK(apkfile):
		parser.print_help(sys.stderr)
		sys.exit()

	global folder
	folder = os.path.basename(apkfile+"_tmp")
	
	time_start = time.time()
	
	# extract file in folder
	apk_file.extractAPK(apkfile, folder)
	
	# hash md5
	md5 = apk_file.md5APK(apkfile)

	# permission + application + intent
	# it is a dict {"permission": [], "application": [], "intent": []}
	activity = manifest.info(folder)
	activity.update(intent.info(folder))

	if args.family:
		key = args.family
		db  = json_file.load_json("patterns.json")

		if key not in db.keys():
			db.update({key: activity})
			json_file.write_json(db, "patterns.json")
			print ("database updated with", args.family)
		else:
			print ("already exists", args.family)

		# remove folder and exit
		shutil.rmtree(folder)
		sys.exit(0)

	family = []
	if "permission" in activity.keys():
		all_families = True if args.similarity else False
		family = similarity.get(activity, all_families)

	if args.similarity:
		print (family)
		# remove folder and exit
		shutil.rmtree(folder)
		sys.exit(0)
		
	result = {}

	# start analysis
	result.update({
		"version": __version__,
		"md5": md5,
		"activity": activity,
		"dex": search_file.extension_sort(folder, '.dex'),		# search .dex file in folder
		"library": search_file.extension_sort(folder, '.so'),	# search .so file in folder
		"network": match_network.get(folder),
		"root": match_root.info(folder),
		"string": match_strings.get(folder),
		"family": family,
		"sandbox": sandbox.url(md5)
		})
	
	elapsed_time = time.time() - time_start

	if args.report:
		result.update({
			"report": report.get(result)
			})

	# add report and elapsed_time
	result.update({
		"elapsed_time": round(elapsed_time, 2)
		})

	# remove folder
	shutil.rmtree(folder)

	print (json.dumps(result, indent=4))

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\nInterrupted")
		# remove folder (global variable)
		shutil.rmtree(folder)
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)