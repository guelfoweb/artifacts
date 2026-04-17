import os
import sys
import json
import time
import shutil
import argparse
from lib import apk_file, file_list, json_file, search_file, intent, manifest
from lib import match_strings, match_network, match_root
from lib import sandbox, similarity, report
from litejdb import LiteJDB
from prettytable import PrettyTable

__version__ = '1.2.0'

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
            'permission': activity.get('permission', []),
            'application': activity.get('application', []),
            'intent': activity.get('intent', [])
        })
        db.save()
        print(f"Family '{name}' added to database.")
    else:
        print(f"Family '{name}' already exists.")

# List families in LiteJDB
def list_families(db):
    df = db.df()

    if df.empty:
        print("No families stored in LiteJDB.")
        return

    def normalize(values):
        if not values:
            return []
        if isinstance(values, (set, tuple)):
            values = list(values)
        if isinstance(values, str):
            values = [values]
        return sorted(values, key=str.casefold)

    table = PrettyTable(["Family", "Permission", "Application", "Intent"])

    for _, row in df.sort_values("name").iterrows():
        counts = []
        for bucket in ("permission", "application", "intent"):
            values = normalize(row[bucket] if bucket in row and row[bucket] is not None else [])
            counts.append(len(values))
        table.add_row([row["name"], *counts])

    print(table)

def activity_counts(activity):
    summary = {}
    for bucket in ("permission", "application", "intent"):
        values = activity.get(bucket) or []
        if isinstance(values, (set, tuple)):
            values = list(values)
        elif isinstance(values, str):
            values = [values]
        summary[bucket] = len({v for v in values})
    return summary

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
    parser.add_argument(
        "--fast",
        help="skip regex-heavy IOC extraction (ip/url/base64/telegram/root) for faster analysis",
        action="store_true"
    )
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

    if not os.path.exists(apkfile):
        parser.exit(2, f"Error: APK file not found: {apkfile}\n")

    if not os.path.isfile(apkfile):
        parser.exit(2, f"Error: Path is not a file: {apkfile}\n")

    folder = os.path.basename(apkfile + "_tmp")
    os.makedirs(folder, exist_ok=True)
    time_start = time.time()

    try:
        # Extract APK and start analysis
        apk_file.extractAPK(apkfile, folder)
        hashes = apk_file.hashAPK(apkfile)
        filepaths = file_list.get(folder)
        activity = manifest.info(apkfile)
        activity.update(intent.info(filepaths))
        archives = search_file.search_archive(filepaths)

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
        if args.fast:
            network = {"ip": [], "url": [], "param": []}
            root = []
            string = {"base64": [], "telegram_id": [], "known": []}
        else:
            network = match_network.get(filepaths)
            root = match_root.info(filepaths)
            string = match_strings.get(filepaths)

        result = {
            "version": __version__,
            "md5": hashes.get("md5"),
            "sha1": hashes.get("sha1"),
            "sha256": hashes.get("sha256"),
            "package_name": activity.get("package_name"),
            "main_activity": activity.get("main_activity"),
            "dex": search_file.extension_sort(filepaths, '.dex'),
            "library": search_file.extension_sort(filepaths, '.so'),
            "archive": archives,
            "network": network,
            "root": root,
            "string": string,
            "activity_counts": activity_counts(activity),
            "family": family,
            "sandbox": sandbox.url(hashes.get("md5")),
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
