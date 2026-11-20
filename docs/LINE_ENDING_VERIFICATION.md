# Line-ending reproducibility correction - 20 November 2026

## Cause and affected files
Leyla reported that the path fix passed on Apple Silicon/macOS with Python 3.11.7, but stored Windows byte hashes still differed from her LF checkout. Her success after isolated line-ending adjustment is user-reported evidence, not a native run conducted here.

We compared each of the 17 input-manifest files against its HEAD Git blob: all four raw/metadata files, nine processed CSVs and four notebooks had local CRLF versus Git LF. In every case, replacing CRLF with LF made the contents identical. See [exact diagnosis](verification_eol_20261120/line_ending_diagnosis.json). No data values were changed.

## Minimal correction and Git policy
.gitattributes defaults unknown files to -text, explicitly sets known project text formats to text eol=lf, and marks SQLite/DB, PDF, PPTX, image and ZIP formats binary. Existing raw data/notebooks were not rewritten or mass-renormalized. Fresh checkouts follow LF irrespective of core.autocrlf; an existing checkout may retain CRLF until Git rewrites a file, which the normalizing hash also supports.

src/analysis.py adds inputs_normalized_sha256 and hash_policy=sha256-crlf-to-lf-text-v1 beside the existing byte manifest. Only .csv, .json, .ipynb, .py, .md, .txt, .yml and .yaml hashes replace byte sequence CRLF with LF. No decoding, trimming, whitespace folding, JSON reserialization or standalone-CR conversion occurs. All other extensions use exact SHA-256 bytes. SQL files use LF Git checkouts but are not part of the normalized input manifest; SQL queries are executed and checked separately.

scripts/verify_pipeline.py records byte differences for provenance, but uses normalized hashes for the protected raw/notebook content guard. Missing and conflicting path entries still fail through manifest_differences; Windows/POSIX key normalization is unchanged. Prepared CSV content is additionally checked numerically at the established 1e-9 tolerance. Local source-file immutability during execution is still checked BYTE FOR BYTE. No binary content is normalized: SQLite tables/integrity are compared semantically across rebuilds; source SQLite and deck/image files remain byte-protected against accidental mutation. Generated figure checks establish regeneration and filenames, not pixel equality.

## Historical evidence preserved
The original inputs_sha256 values in results/analysis/analysis_report.json are retained unchanged. The complete pre-correction report is archived as [historical byte manifest](verification_eol_20261120/historical_byte_analysis_report.json). Prior 19/20 November verification evidence remains unchanged. New executions still emit raw byte hashes alongside normalized hashes; these describe the actual checkout and may legitimately differ by OS. Never compare a normalized digest against an old raw digest.

## Tests and fresh checkout evidence
15 tests passed: the prior ten plus LF/CRLF equivalence, true text changes, exact binary hashes across seven extensions, significant other whitespace and standalone carriage returns. Windows/POSIX keys, missing keys and conflicting normalized entries remain covered. New tests were first observed failing before implementing the helper.

Two isolated fresh Git-index checkouts were created from a local clone plus the staged correction (no test commits): git checkout-index --all into empty directories with core.autocrlf=false and true respectively. Both obeyed .gitattributes and checked out raw data as LF. Both full reproduction runs passed:
- All four notebooks / 49 code cells.
- 19 CSV comparisons, three SQLite tables and integrity, four SQL queries.
- EDA, three model fits, all 24 sensitivity scenarios and four regenerated figures.
- Normalized input hashes match; raw-byte differences are reported rather than discarded.
- All 15 automated tests; source files unchanged.

[LF checkout run](verification_eol_20261120/checkout_lf_reproduction.json), [autocrlf checkout run](verification_eol_20261120/checkout_autocrlf_reproduction.json).

Actual platform: Windows x64, isolated Python 3.12.4 environment. Tests model LF checkouts and Windows CRLF content, not native macOS/Linux execution. No successful post-fix native Mac run is claimed. PDF/PPTX and SQLite bytes in both fresh checkouts were separately confirmed identical to the source.

## Scientific results and next Mac check
No CSV/model/figure or original data change was required. Main coefficients and all counts, p-values, R-squared and RMSE remain unchanged; only provenance fields were added. Main model: 2108 municipalities, 2254 operator observations, joint p 0.5584182183, R-squared 0.3899700430, RMSE 2.5078559943. Research question and weighting are unchanged.

Leyla: pull the updated feat/harmonized-analysis branch into a clean checkout, select her working environment, then run python -m unittest discover -s tests -v and python scripts/verify_pipeline.py. Expected: 15 passing tests, four notebooks, 19 CSV comparisons, no protected normalized-content differences. Raw byte differences alone are informational. Preserve/share a traceback if anything fails; do not manually convert original data or overwrite expected hashes to suppress a failure.

## Final committed-clone confirmation

After correction commit 5a4d5c70eba89f82088f05bc2356169d3273027b, a new git clone --no-hardlinks --branch feat/harmonized-analysis was created in an empty external directory. The complete pipeline passed again: four notebooks, 19 CSV comparisons, three SQLite tables/four SQL queries, four regenerated figures, 24 scenarios, 15 tests and zero normalized input differences. This is a regular clone of the actual commit, in addition to the two staged-index checkout tests. [Fresh committed-clone evidence](verification_eol_20261120/fresh_commit_reproduction.json). The second commit only adds this documentation/evidence; analysis code is unchanged.
