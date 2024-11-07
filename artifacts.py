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

__version__ = '1.1.3'

# 1.1.3 Fixed: Skip files with unsupported compression methods during extraction
# 1.1.2 Fixed: Resolved conflict during extraction by renaming directories with names matching existing files
# 1.1.1 Fixed: Joesanbox url, updated strings to match and added koodous sandbox
# 1.1.0 Removed: 'activity' and 'report' from json, now they are used separately
# 1.0.9 Fixed: ZeroDivisionError in similarity
# 1.0.8 Added: LiteJDB support to 'add', 'del' and 'list'
# 1.0.7 Added: Similarity table with prettytable dependency
# 1.0.6 Fixed: jaccard similarity coefficient and added updatedb
# 1.0.5 Added: Checks if decoded base64 string matches the regex
# 1.0.4 Added: Decodes base64 strings
# 1.0.3 Fixed: Permission non found in result["activity"]["permission"]
# 1.0.2 Fixed: extractAPK file name too long
# 1.0.1 Added: details to family
# 1.0.0 start project

# Load json database
def load_db():
    filename = os.path.join('data', 'patterns.json')
    db = LiteJDB(filename)
    db.load()
    return db

# Delete family from LiteJDB
def delete_family(name, db):
    ids = db.query(f"name == '{name}'", "get_id")
    for id in ids:
        db.delete(id)
    db.save()

# Add family to LiteJDB
def add_family(name, activity, db):
    if not db.query(f"name == '{name}'", "get_id"):
        db.add({
            'name': name,
            'permission': activity['permission'],
            'application': activity['application'],
            'intent': activity['intent']
        })
        db.save()
    else:
        print(f"{name} already exists")

# List families in LiteJDB
def list_families(db):
    for index, row in db.df().iterrows():
        print(row['name'])

# Main function for APK analysis
def main():
    db = load_db()
    parser = argparse.ArgumentParser(prog="artifacts", description="apk analysis")

    # Command-line arguments
    parser.add_argument("apkfile", nargs='?', help="apk to analyze")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s " + __version__)
    parser.add_argument("-r", "--report", help="add report to json result", action="store_true")
    parser.add_argument("-s", "--similarity", help="shows the similarities", action="store_true")
    parser.add_argument("-a", "--activity", help="shows the activities", action="store_true")
    parser.add_argument("-l", "--list-all", help="Lists all families in the db", action="store_true")
    parser.add_argument("--del", help="Delete a family from db", dest="family_to_del")
    parser.add_argument("--add", help="Add a new family to db", dest="family_to_add")
    args = parser.parse_args()

    apkfile = args.apkfile

    # Handle --del, --list-all, or --add arguments without apkfile
    if not apkfile:
        if args.family_to_del:
            delete_family(args.family_to_del, db)
        elif args.list_all:
            list_families(db)
        else:
            parser.print_help()
        sys.exit()

    folder = os.path.basename(apkfile + "_tmp")
    os.makedirs(folder, exist_ok=True)
    time_start = time.time()

    try:
        # Extract APK and start analysis
        apk_file.extractAPK(apkfile, folder)
        md5 = apk_file.md5APK(apkfile)
        activity = manifest.info(folder)
        activity.update(intent.info(folder))

        # Handle individual arguments
        if args.activity:
            print(json.dumps(activity, indent=4))
            return

        if args.report:
            print(json.dumps(report.get(activity), indent=4))
            return

        if args.family_to_add:
            add_family(args.family_to_add, activity, db)
            return

        # Find family similarities if requested
        family = []
        if "permission" in activity:
            all_families = args.similarity
            family = similarity.get(activity, all_families, db.df())

        if args.similarity:
            print(family)
            return

        # Compile result data
        result = {
            "version": __version__,
            "md5": md5,
            "dex": search_file.extension_sort(folder, '.dex'),
            "library": search_file.extension_sort(folder, '.so'),
            "network": match_network.get(folder),
            "root": match_root.info(folder),
            "string": match_strings.get(folder),
            "family": family,
            "sandbox": sandbox.url(md5),
            "elapsed_time": round(time.time() - time_start, 2)
        }
        print(json.dumps(result, indent=4))

    finally:
        shutil.rmtree(folder)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted")
        shutil.rmtree(folder, ignore_errors=True)
        sys.exit(0)
