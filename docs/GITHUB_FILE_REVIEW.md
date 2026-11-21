# GitHub file selection - 19 November 2026

> Historical snapshot: 19 November 2026, before the first publication. For the current 20 November correction status see [review follow-up](REVIEW_FOLLOWUP_20261120.md).
Branch: `feat/harmonized-analysis`. This is an explicit proposed selection, not staged or committed. No commit/push is authorized yet. No new branch is required.

## Proposed changed/new files

The list below is the complete candidate set after documentation repair. Existing unchanged baseline files are already tracked and must not be replaced. The full analysis/results and canonical presentation are retained. Historical reference comparison and reproduction outputs are retained as dated evidence; the fresh test evidence lives under docs/verification_20261119.

- `.gitignore`
- `AI_Log.md`
- `README.md`
- `constraints-tested.txt`
- `docs/04_analysis.md`
- `docs/GITHUB_FILE_REVIEW.md`
- `docs/INTEGRATION_STATUS.md`
- `docs/RELEASE_VERIFICATION.md`
- `docs/RESULT_COMPARISON.md`
- `docs/verification_20261119/artifact_checks.json`
- `docs/verification_20261119/installed-freeze-windows-py312.txt`
- `docs/verification_20261119/reproduction.json`
- `notebooks/04_analysis.ipynb`
- `presentation/v3/QUALITY_REPORT_v3.md`
- `presentation/v3/presentation_concept_group_05_EN_v3.pdf`
- `presentation/v3/presentation_concept_group_05_EN_v3.pptx`
- `presentation/v3/speaker_notes_group_05_EN_v3.md`
- `requirements-lock-windows-py312.txt`
- `requirements.txt`
- `results/analysis/analysis_report.json`
- `results/analysis/coefficients_canton.csv`
- `results/analysis/coefficients_type.csv`
- `results/analysis/coefficients_type_canton.csv`
- `results/analysis/descriptive_summary.csv`
- `results/analysis/diagnostics.csv`
- `results/analysis/figures/01_types.png`
- `results/analysis/figures/02_cantons.png`
- `results/analysis/figures/03_coefficients.png`
- `results/analysis/figures/04_residuals.png`
- `results/analysis/model_metrics.csv`
- `results/analysis/reference_comparison.csv`
- `results/analysis/reference_comparison.json`
- `results/analysis/reproduction.json`
- `results/analysis/sensitivity.csv`
- `scripts/compare_reference.py`
- `scripts/verify_pipeline.py`
- `src/analysis.py`
- `tests/test_analysis.py`

## Excluded and preserved locally

- `.git`, virtual environments, Python caches and notebook checkpoints.
- `presentation/v3/build/`: machine-specific builder, redundant renders/contact sheets, intermediate QA inputs. Canonical PPTX/PDF/notes/QA report are included.
- `docs/INTEGRATION_PLAN.md` and `docs/CONCEPT_UPDATE_EN.md`: historical local planning notes, retained locally; current status and method documents are included.
- Temporary test copies, installation logs, backups and environments live outside this repository.
- `.env` and `.env.*` excluded, `.env.example` explicitly allowed. A targeted private-key/GitHub-token/MongoDB-credential pattern scan found no matches in candidate text files; this is not a claim of universal secret detection.

.gitignore required no additional change: it already preserves all required code, notebook, source data, analysis figures, result tables and delivery files. No deletion of ignored files was performed.

## Reviewable grouping

1. Environment and documentation: requirements/constraints/lock, .gitignore, README, AI log, fresh verification evidence.
2. Analysis: src, notebook 04, tests, scripts, results, method/comparison documentation. The complete verifier requires notebook 04; do not publish it as an independently runnable baseline-only change before analysis dependencies exist.
3. Presentation: canonical v3 delivery files and QA. No redundant renders or previous decks.

If split into PRs later, make dependency/order explicit. Refresh main before any eventual publication and review README conflicts. Current original data/notebooks/SQL remain unchanged. A named feature branch is not a remote backup: all added work remains uncommitted until approval.
