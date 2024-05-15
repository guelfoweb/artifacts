import os
import sys
import json
import time
import shutil
import argparse

from lib import apk_file, json_file, search_file, intent, manifest
from lib import match_strings, match_regex, match_network, match_root
from lib import sandbox, similarity, report
from litejdb import LiteJDB

__version__ = '1.1.0'

# 1.1.0 removed 'activity' and 'report' from json, now they are used separately
# 1.0.9 fix ZeroDivisionError in similarity
# 1.0.8 added LiteJDB support to 'add', 'del' and 'list'
# 1.0.7 added similarity table with prettytable dependency
# 1.0.6 fixed jaccard similarity coefficient and added updatedb
# 1.0.5 checks if decoded base64 string matches the regex
# 1.0.4 decodes base64 strings
# 1.0.3 fixed permission non found in result["activity"]["permission"]
# 1.0.2 fixed extractAPK file name too long
# 1.0.1 added details to family
# 1.0.0 start project

# load json database
def load_db():
	filename = 'data' + os.sep + 'patterns.json'
	db = LiteJDB(filename)
	db.load()
	return db

# LiteJDB delete
def delete_family(name):
	query = "name == '{name}'".format(name=name)
	ids = db.query(query, "get_id")
	if ids:	# [1]
		for id in ids:
			db.delete(id)
	db.save()

def add_family(name, activity):
	query = "name == '{name}'".format(name=name)
	exists = db.query(query, "get_id")
	if not exists:
		db.add({'name': name, 'permission': activity['permission'], 'application': activity['application'], 'intent': activity['intent']})
		db.save()
	else:
		print (name, 'already exists at', exists)

def list_families():
	for index, row in db.df().iterrows():
		print (row['name'])

def main():
	global db
	db = load_db()

	parser = argparse.ArgumentParser(prog="artifacts", description="apk analysis")

	# args
	parser.add_argument("apkfile", nargs='?', help="apk to analyze")
	parser.add_argument("-v", "--version", action="version", version="%(prog)s " + __version__)
	parser.add_argument("-r", "--report", help="add report to json result", action="store_true", required=False)
	parser.add_argument("-s", "--similarity", help="shows the similarities", action="store_true", required=False)
	parser.add_argument("-a", "--activity", help="shows the activities", action="store_true", required=False)
	parser.add_argument("-l", "--list-all", help="Lists all families in the db", action="store_true", required=False)
	parser.add_argument("--del", help="Delete a family from db", dest="family_to_del", required=False)
	parser.add_argument("--add", help="Add a new family to db", dest="family_to_add", required=False)
	args = parser.parse_args()

	apkfile = args.apkfile

	# check if the domain name is correct
	if not apkfile or not os.path.isfile(apkfile) or not apk_file.validateAPK(apkfile):
		# LiteJDB delete
		if args.family_to_del:
			name = args.family_to_del
			delete_family(name)
		# LiteJDB list
		elif args.list_all:
			list_families()
		else:
			parser.print_help(sys.stderr)
		sys.exit()

	global folder
	folder = os.path.basename(apkfile+"_tmp")
	
	time_start = time.time()
	
	# extract file in folder
	apk_file.extractAPK(apkfile, folder)
	
	# hash
	md5, sha1, sha256 = apk_file.md5APK(apkfile)


	# permission + application + intent
	# {"permission": [], "application": [], "intent": []}
	activity = manifest.info(folder)
	activity.update(intent.info(folder))

	if args.activity:
		print (json.dumps(activity, indent=4))
		shutil.rmtree(folder)
		sys.exit(0)

	if args.report:
		print (json.dumps(report.get(activity), indent=4))
		shutil.rmtree(folder)
		sys.exit(0)

	# LiteJDB add
	if args.family_to_add:
		name = args.family_to_add
		add_family(name, activity)
		shutil.rmtree(folder)
		sys.exit(0)

	family = []
	if "permission" in activity.keys():
		all_families = True if args.similarity else False
		family = similarity.get(activity, all_families, db.df())

	if args.similarity:
		print (family)
		shutil.rmtree(folder)
		sys.exit(0)

	result = {}

	# start analysis
	result.update({
		"version": __version__,
		"md5": md5,
		"sha1": sha1,
		"sha256": sha256,
		"dex": search_file.extension_sort(folder, '.dex'),		# search .dex file in folder
		"library": search_file.extension_sort(folder, '.so'),	# search .so file in folder
		"network": match_network.get(folder),
		"root": match_root.info(folder),
		"string": match_strings.get(folder),
		"family": family,
		"sandbox": sandbox.url(sha256)
		})
	
	elapsed_time = time.time() - time_start

	# add report and elapsed_time
	result.update({
		"elapsed_time": round(elapsed_time, 2)
		})

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