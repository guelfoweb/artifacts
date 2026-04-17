# Repository Guidelines

## Project Structure & Module Organization
`artifacts.py` is the CLI front and should stay slim—hand off parsing, manifest work, and enrichment to focused helpers in `lib/`. Each module there maps to one task (`match_strings.py`, `similarity.py`, `sandbox.py`, etc.), so prefer new modules over inflating existing ones. Detection data lives under `data/` (patterns, permission categories, descriptions); update those JSON files rather than hard-coding values, and keep APK samples outside the repo.

## Build, Test, and Development Commands
- `python3 -m venv .venv && source .venv/bin/activate` — spin up an isolated toolchain.
- `pip install -r requirements.txt` — install PrettyTable and LiteJDB at the pinned versions.
- `python3 artifacts.py -h` — smoke-check argument parsing after refactors.
- `python3 artifacts.py <apk> -r -s` — end-to-end analysis with report and similarity tables.
- `python3 artifacts.py --list-all` — verify LiteJDB reads after mutating the database interface.

## Coding Style & Naming Conventions
Follow standard Python style: 4-space indents, snake_case identifiers, and module-level constants for tuning knobs. Keep modules import-safe (no work on import) and prefer pure functions that return dict/list payloads the CLI can serialize. When editing JSON assets, maintain alphabetical keys and sentence-case descriptions to keep diffs predictable.

## Output & Metadata Conventions
- The main CLI report must always expose the three hashes (`md5`, `sha1`, `sha256`) for the analyzed APK; reuse `lib/apk_file.hashAPK` so every code path stays in sync.
- Keep `activity_counts` ordered as `permission`, `application`, `intent` and ensure the values reflect the number of *unique* items extracted from the manifest/intents.
- `python3 artifacts.py --list-all` now emits a PrettyTable sorted alphabetically by family with the counts of permissions/applications/intents. Any changes to LiteJDB schemas should keep this tabular contract intact.
- When populating the internal DB (`python3 artifacts.py sample.apk --add NAME`) always pass the APK path as the positional argument so the permission/application/intent buckets are derived from an actual manifest, not manual edits.
- Include `package_name` and the resolved launcher `main_activity` in the report output; source them via `lib/manifest.py` rather than reimplementing manifest parsing elsewhere.

## Testing & Validation
No automated suite exists yet, so rely on reproducible manual runs. Maintain a curated set of benign APKs that exercise dex extraction, manifest parsing, and string matching, and note the commands you ran (`python3 artifacts.py demo.apk --activity`, etc.) in the PR. When adding detection content, craft minimal JSON fixtures under `data/` and verify the CLI surfaces them cleanly so future pytest coverage can hook in.

## Commit & Pull Request Guidelines
Recent history shows short, imperative subjects (`Fix ZIP version detection`, `patterns update`); keep using that format and scope each commit to one concern. Pull requests should describe the behavior change, list the commands executed for validation, call out data file edits, and reference related issues or reports. Include before/after snippets for PrettyTable output when it changes.

## Security & Operational Notes
Treat every APK as hostile: analyze inside disposable VMs, keep samples quarantined, and omit binaries from commits. Scrub PII and proprietary endpoints from shared JSON or logs. When contributing new indicators to `data/patterns.json`, cite the intelligence source in the PR description and note if it might expose live infrastructure.
