# artifacts

![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-GPLv3-green.svg)
![Status](https://img.shields.io/badge/status-active-success)

**artifacts** is a CLI toolkit for static triage of suspicious APKs. It surfaces known strings, network indicators, manifest permissions/anomalies, and suggests likely malware families by comparing the findings against a LiteJDB dataset. Use it for the very first pass before switching to heavyweight tools such as Jadx, Bytecode-Viewer, or dynamic sandboxes.

## Table of Contents

- [Key Features](#key-features)
- [apkInspector Integration](#apkinspector-integration)
- [Requirements & Installation](#requirements--installation)
- [Quick Start](#quick-start)
- [CLI Commands](#cli-commands)
- [Datasets & Reporting](#datasets--reporting)
- [Contributing](#contributing)
- [Developers](#developers)
- [License](#license)

## Key Features

- **Robust extraction** – `apkInspector.headers.ZipEntry` lets us unpack obfuscated or tampered APKs directly inside the working temp folder, avoiding the limitations of Python's `zipfile`.
- **Manifest decoding** – `apkInspector.axml.parse_apk_for_manifest` decodes `AndroidManifest.xml` even when it is still in binary form, so we can read permissions/applicationId, package name, and launcher activity without fully expanding the archive.
- **String & IOC hunting** – regexes for Base64, URLs/IPs, Telegram IDs, plus curated network/root indicators stored in `data/*.json`.
- **Similarity scoring** – compares the extracted permission/application sets against the LiteJDB database (`data/patterns.json`) to suggest the closest family match.
- **Actionable reports** – `-r` builds a structured JSON report, `-s` prints similarity tables, `--activity` dumps the decoded manifest details.

> ℹ️ **Disclaimer**: outputs are heuristics meant for triage and can produce false positives. Always confirm with additional tooling or manual review.

## apkInspector Integration

This project relies on [apkInspector](https://github.com/erev0s/apkInspector) to reliably unpack APKs even when the ZIP structure is malformed or heavily obfuscated, and to decode `AndroidManifest.xml` straight from the package so permissions and components remain readable.

## Requirements & Installation

```bash
git clone https://github.com/guelfoweb/artifacts.git
cd artifacts
python3 -m venv .venv && source .venv/bin/activate   # recommended
pip install -r requirements.txt
```

Main dependencies:

- Python 3.10+
- [apkInspector](https://github.com/erev0s/apkInspector)
- [LiteJDB](https://github.com/guelfoweb/litejdb)
- prettytable

### Track unreleased apkInspector patches

`apkInspector` is installed from the upstream GitHub repository (branch `main`) so this project can consume fixes before the next PyPI release.

If you want reproducible builds, pin a specific commit instead of `main` in both `requirements.txt` and `pyproject.toml`:

```text
apkInspector @ git+https://github.com/erev0s/apkInspector.git@<commit_sha>
```

## Quick Start

```bash
# Full help
python3 artifacts.py -h

# Run analysis + JSON report + similarity table
python3 artifacts.py sample.apk -r -s

# List every family stored in LiteJDB
python3 artifacts.py --list-all
```

Sample output (truncated):

```json
{
  "version": "1.1.4",
  "md5": "ab879f4e8f9cf89652f1edd3522b873d",
  "sha1": "0b36f0f2ddfd73be3452dc955a6c97c45b4f78e9",
  "sha256": "4d0ec8e8c1fbbac866f38b5df31b3a775f482373789a9b6d33ad7bfb17e8c576",
  "package_name": "fdgfhfgjhfgj.dfgdfgdfhfjfgj.sdgdfgdfhd",
  "main_activity": "com.brkwl.apkstore.MainActivity",
  "dex": ["classes.dex"],
  "network": {
    "ip": ["1.1.1.1", "8.8.8.8"],
    "url": ["tg://telegram.org"]
  },
  "string": {
    "base64": [["MTc4LjIzNi4yNDcuMTI0", "178.236.247.124"]],
    "known": ["ping"]
  },
  "activity_counts": {
    "permission": 12,
    "application": 4,
    "intent": 7
  },
  "family": {
    "name": "SpyNote Italy 10/2023",
    "match": 100.0
  }
}
```

### How family matching works

- **Feature extraction** – `lib/manifest.py` parses the decoded manifest and normalizes the three indicator buckets (`permission`, `application`, `intent`) as alphabetically sorted lists.
- **Family dataset** – each entry in `data/patterns.json` provides the expected indicators for a known malware family. When you run `artifacts.py … -s`, the CLI loads this dataset via LiteJDB.
- **Per-bucket scoring** – for every family we compute the [Jaccard similarity](https://en.wikipedia.org/wiki/Jaccard_index) between the APK bucket and the family bucket (e.g., `permission_score = |perm_apk ∩ perm_family| / |perm_apk ∪ perm_family| * 100`). The same formula is applied to `application` and `intent`.
- **Final score** – the reported `family.match` is the arithmetic mean of the three bucket scores (all equally weighted) and is expressed as a percentage (e.g., `21.48` means ~21.48%). The `family.value` object surfaces the individual bucket percentages so you can tell *why* a match ranked higher (e.g., strong intent overlap but few shared permissions).
- **Interpreting the report** – identical APK permissions can still yield different percentages if the top-ranked family changes, because each family contributes its own reference set. As a rule of thumb, scores below ~50 % should be treated as weak evidence (possible false positives or new families) and warrant manual review or dataset enrichment. Log the similarity table (`-s`) to compare how your indicators intersect with multiple candidates.
- **Raw counts** – the `activity_counts` field in the main JSON result shows how many unique permissions, components, and intents were extracted from the APK, independent of any family match. This is useful when profiling previously unseen samples.

## CLI Commands

| Flag | Description |
| ---- | ----------- |
| `-h, --help` | Show the inline help. |
| `-v, --version` | Print the tool version. |
| `-r, --report` | Emit a structured JSON report. |
| `-s, --similarity` | Display the similarity table against the family DB. |
| `-a, --activity` | Dump decoded manifest activities/permissions. |
| `-l, --list-all` | List all families tracked in LiteJDB with the number of permissions, applications, and intents each entry defines. |
| `--fast` | Faster scan: skip regex-heavy IOC extraction (`network`, `root`, `string`). |
| `--del NAME` | Remove a family from the DB. |
| `--add NAME` | Add the currently analyzed APK (pass the malware sample as the positional argument) to the DB under `NAME`. |

## Datasets & Reporting

- **`data/patterns.json`** – defines known families, expected permissions, and application names. Updating this file improves matching without touching the Python code.
- **`data/permission_categories.json` / `permission_description.json`** – provide human-readable descriptions used in reports.
- The `-r` flag outputs category-based JSON (LOCATION, NETWORK, etc.) that can be pasted into tickets or knowledge bases.

## Contributing

1. Open an issue describing the bug/feature.
2. Work in a dedicated branch (e.g., `feature/apk-inspector-upgrade`).
3. Run the core commands (`python3 artifacts.py sample.apk -r -s`, `--list-all`) and attach the output to your PR.
4. Use imperative commit messages (e.g., `Add apkInspector extraction`).

See [AGENTS.md](AGENTS.md) for extended contributor guidance (coding style, security hygiene, etc.).

## Developers

- [Gianni Amato](https://github.com/guelfoweb/)
- [Andrea Draghetti](https://github.com/drego85/)

## License

Released under [GPL-3.0](LICENSE). Treat every APK as hostile: operate inside isolated VMs, never commit binaries to the repo, and sanitize sensitive data before sharing artifacts.
