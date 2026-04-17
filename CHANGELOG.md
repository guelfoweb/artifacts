# Changelog

All notable changes to this project are documented in this file. The format loosely follows the [Keep a Changelog](https://keepachangelog.com) recommendations, with versions listed in descending order.

## [1.2.0] - 2025-11-12
- Added deep apkInspector integration so manifest parsing and extraction stay resilient to malformed archives.
- Added `activity_counts` to summarize unique permissions, applications, and intents per APK.
- Added MD5, SHA1, and SHA256 hashes to the primary JSON report.
- Added package name and launcher `main_activity` details to the report output.
- Added new malware families to the embedded LiteJDB dataset.

## [1.1.4]
- Added Zip Header Fixer and archive detection.

## [1.1.3]
- Fixed skipping files with unsupported compression methods during extraction.

## [1.1.2]
- Fixed extraction conflicts by renaming directories whose names matched existing files.

## [1.1.1]
- Fixed JoeSandbox URL, updated matched strings, and added Koodous sandbox integration.

## [1.1.0]
- Removed `activity` and `report` from the JSON payload; they are now provided separately.

## [1.0.9]
- Fixed `ZeroDivisionError` in similarity scoring.

## [1.0.8]
- Added LiteJDB support to the `add`, `del`, and `list` commands.

## [1.0.7]
- Added the similarity table feature powered by PrettyTable.

## [1.0.6]
- Fixed the Jaccard similarity coefficient and added the `updatedb` command.

## [1.0.5]
- Added validation to ensure decoded Base64 strings match the intended regex.

## [1.0.4]
- Added automatic Base64 decoding.

## [1.0.3]
- Fixed missing permissions in `result["activity"]["permission"]`.

## [1.0.2]
- Fixed extraction failures caused by overly long APK filenames.

## [1.0.1]
- Added detailed family metadata to the output.

## [1.0.0]
- Initial project release.
