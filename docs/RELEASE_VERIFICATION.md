# Release verification - 19 November 2026

## Scope and outcome
PASS: fresh Windows x64 Python 3.12.4 virtual environment, isolated from the existing project environment. This is a Windows test, not a Linux/macOS or clean-machine certification. The venv was created from the existing Python 3.12.4 interpreter with system site-packages disabled; packages were installed anew (pip cache permitted).

No commit, push, PR, merge or Moodle publication was performed. Branch: `feat/harmonized-analysis`; base `9dc56db3ac02c6d4874299b7f5864220c907456e`. Remote main remained at that commit at the initial live check.

## Installation
Commands from project root (use an external temporary path for release tests):

```powershell
py -3.12 -m venv TEMP_ENV
TEMP_ENV/Scripts/python.exe -m pip install -r requirements.txt -c constraints-tested.txt
TEMP_ENV/Scripts/python.exe -m pip check
TEMP_ENV/Scripts/python.exe scripts/verify_pipeline.py
```

Install exit 0; pip check: `No broken requirements found`. No installation failure occurred in this new run. The previously interrupted environment was not reused. PowerShell classified pip's upgrade notice on stderr as NativeCommandError in the redirected log; this was a notice, not a failed installation (exit 0 and successful downstream checks).

Direct analysis packages: numpy 1.26.4, pandas 2.2.2, scipy 1.13.1, statsmodels 0.14.2, matplotlib 3.8.4, requests 2.32.3; notebook packages nbformat 5.10.4, nbclient 0.10.2, ipykernel 6.29.5, jupyterlab 4.2.5. Full actual transitive versions: [fresh environment freeze](verification_20261119/installed-freeze-windows-py312.txt). The root Windows lock records the earlier environment and is retained, not silently replaced by this fresh freeze.

## Fresh execution
The source was copied outside the repository. The verifier created its own temporary build, removed derived data/results/database there and executed saved snapshots with requests disabled. All four notebooks passed (14 + 24 + 9 + 2 = 49 original code cells). All 19 CSV comparisons passed at 1e-9 tolerance; all three SQLite tables matched, integrity check passed, and four SQL queries returned 3, 2108, 3 and 2 rows. Four figures were regenerated; this checks generation and filenames, not pixel equivalence. All six automated tests passed. No regenerated input-byte differences were reported. [Machine-readable reproduction evidence](verification_20261119/reproduction.json).

All 24 sensitivity scenarios, model coefficients, fit and descriptive outputs were regenerated and compared. Counts remain 2268 raw rows, 2255 distinct tariff rows, 2254 municipality/operator values, 2108 municipalities and 551 operators. Main joint p = 0.5584182183, weighted in-sample R-squared = 0.3899700430 and RMSE = 2.5078559943 Rp./kWh. No statistical conclusion changed. Fit remains explanatory/in-sample, not predictive validation or causal evidence.

## Preservation and presentation
27 original tracked files other than the intentionally edited README are byte-identical to the baseline checkout. No original notebooks, data, SQLite, SQL, analysis code or numerical outputs were modified. [Artifact checks](verification_20261119/artifact_checks.json).

All four presentation delivery hashes match the previously fully rendered and visually verified v3 files. The PPTX has 14 slides; key counts and p-value were checked again. Boxplot group sizes and quartiles were recalculated from municipality_values.csv and agree. This review did not redo the unchanged deck's full visual rendering; see the historical [visual QA](../presentation/v3/QUALITY_REPORT_v3.md). PPTX, PDF and notes remain unchanged. Their automated rebuild is machine-specific; this does not prevent editing the canonical PPTX.

## Documentation and file selection
README damaged ranges and R-squared character repaired; AI log now explicitly records the current prohibition on commits/pushes. Historical completion statements in integration/comparison documentation were updated. README links resolve. Existing .gitignore excludes caches, virtual environments, secrets and presentation build/renders; it does not exclude canonical delivery files or analysis figures. Ignored historical preparation documents remain locally preserved. See [exact GitHub selection](GITHUB_FILE_REVIEW.md).

## Remaining limits
No fresh online API collection was needed or run; reproducibility is for the saved, harmonized snapshot. No Linux/macOS install certification. Group scientific acceptance, individual AI reflection, speaker agreement/rehearsal and Moodle submission remain open. No technical blocker was found for preparing the selected feature changes for GitHub after explicit commit/push approval.

Detailed installation/execution logs and the disposable environment remain outside the repository in `C:/Users/kevin/Documents/Codex/group05_release_20261119_resume`.
