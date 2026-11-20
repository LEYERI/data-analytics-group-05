# Where You Live and What You Pay for Electricity

A Data Analytics module project on household electricity tariffs in Swiss municipalities.

## Research question

How do electricity tariffs differ between urban, intermediate and rural Swiss municipalities after accounting for canton?

## Scope

| Item | Definition |
|---|---|
| Tariff year | 2026 |
| Household profile | H4, with annual consumption of 4,500 kWh |
| Product | Standard product |
| Outcome | Municipality comparison tariff in Swiss centimes (Rp.) per kWh |
| Comparison target | Equally weighted municipality |
| Regression observation | Municipality/operator comparison value |
| Grouping | BFS urban–rural typology 2020 |
| Municipality reference date | January 1, 2026 |
| Additional explanatory variable | Canton |

The analysis describes statistical associations. Estimating causal effects is outside its scope.

## Data sources

- The Federal Electricity Commission (ElCom) publishes electricity tariffs through [LINDAS SPARQL](https://ld.admin.ch/query). [ElCom tariff information](https://www.elcom.admin.ch/de/tarifdaten-und-visualisierungen)
- The Federal Statistical Office (BFS) provides municipality numbers, official names, cantons and the urban–rural typology. [BFS municipality register for January 1, 2026](https://www.agvchapp.bfs.admin.ch/api/communes/levels?date=01-01-2026)

The original API responses and retrieval metadata are in `data/raw/`.

## Method and project status

| Step | Status |
|---|---|
| 1. Collect data through official APIs | Complete |
| 2. Prepare and integrate the data | Complete |
| 3. Store data in SQLite and run SQL from Python | Complete |
| Exploratory data analysis | Implemented on this feature branch; group review pending |
| Regression and model evaluation | Implemented and technically reproduced; group review pending |
| Final interpretation and presentation | Concept presentation v3 prepared; group approval and rehearsal pending |

We join the sources by BFS municipality number and use official change notices to document municipality number updates.

We first average distinct tariff values within each municipality and operator, then average the operator values within each municipality. This gives each operator equal weight within a municipality and yields one comparison value per municipality. Interpreting it as an average tariff paid by households would require customer or consumption shares, which are unavailable.

## Data coverage

| Measure | Count |
|---|---:|
| ElCom tariff rows in the saved response | 2,268 |
| BFS municipality records | 2,110 |
| Cleaned tariff rows | 2,255 |
| Municipality comparison values | 2,108 |

After harmonizing municipality numbers, we consolidate 12 identical municipality–operator–tariff combinations and exclude one row with a missing total tariff. Augst and Nürensdorf have no matching tariff in the saved snapshot. The original SQL summary compares municipality types descriptively. Notebook 04 adds canton-adjusted explanatory regression without changing the original preparation. It uses 2,254 municipality/operator observations from 551 operators; weights sum to one per municipality.

## Project structure

| Path | Contents |
|---|---|
| `notebooks/` | Jupyter notebooks with code and explanations |
| `data/raw/` | Original API responses and retrieval metadata |
| `data/processed/` | Processed tables and cleaning records |
| `data/electricity_tariffs.sqlite` | SQLite database |
| `sql/` | Saved SQL queries |
| `results/sql/` | Original SQL summaries exported as CSV |
| `src/analysis.py` | Explanatory models, EDA and 24 sensitivity scenarios including the main model |
| `results/analysis/` | Current coefficients, fit metrics, sensitivity results and four figures |
| `tests/`, `scripts/` | Statistical checks and temporary-copy reproduction |
| `presentation/v3/` | Canonical English concept PPTX, PDF, notes and historical visual QA |
| `docs/` | Detailed project documentation |

## Run the notebooks in VS Code

Use Python 3.12. From the repository root, create a virtual environment and install the tested direct dependencies:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -c constraints-tested.txt
.\.venv\Scripts\python.exe -m pip check
```

Select this environment as the VS Code/Jupyter kernel. On other operating systems use the equivalent `python3.12` and `.venv/bin/python` commands; those platforms have not been tested in this release. `requirements-lock-windows-py312.txt` is the complete freeze of the earlier verified Windows environment, not a cross-platform lock. The historical Windows fresh-install evidence and its actual dependency versions are in [release verification](docs/RELEASE_VERIFICATION.md); current corrections are in the [20 November review follow-up](docs/REVIEW_FOLLOWUP_20261120.md).

Run the cells from top to bottom in this order.

1. [Data collection](notebooks/01_data_collection.ipynb) loads and checks the saved responses by default. Set `fetch_new_data = True` to retrieve new, timestamped snapshots over the internet.
2. [Data preparation](notebooks/02_data_preparation.ipynb) integrates the saved responses. If several snapshots exist, explicitly select the files to analyze.
3. [SQLite and SQL](notebooks/03_database.ipynb) rebuilds the three tables from the processed CSVs and exports the query results. `sqlite3` is part of Python's standard library.
4. [EDA and explanatory regression](notebooks/04_analysis.ipynb) consumes those prepared tables; it does not replace notebooks 01–03.

## Verification and results

With the selected environment active, run from the repository root:

```text
python -m unittest discover -s tests -v
python scripts/verify_pipeline.py
```

The verification script removes derived files only in a temporary project copy, executes all four notebooks using saved API snapshots with requests disabled, and checks CSV values, SQLite tables, SQL queries and regenerated figures. It writes `results/analysis/reproduction.json` in the invoking checkout; original notebooks and source data remain unchanged. Run it in a disposable copy if all checkout files must stay byte-identical. Figure generation/count checks do not establish pixel identity or visual quality.

`python -m src.analysis` regenerates only `results/analysis/`. `scripts/compare_reference.py --reference PATH` additionally compares the separately archived earlier project; that archive is not required for the normal four-notebook pipeline.

The main model has joint p = 0.558418, weighted in-sample R² = 0.389970 and RMSE = 2.507856 Rp./kWh at the municipality/operator observation level. This is not held-out predictive performance. There is no statistically clear additional municipality-type association after canton adjustment; this does not establish equality or causality. Operator-omission scenarios can change coefficient signs.

## Documentation

The original project was translated into English with AI assistance. Original methods and calculations in documents 01–03 are retained; the feature analysis is documented separately.

1. [Data collection](docs/01_data_collection.md)
2. [Data preparation and integration](docs/02_data_preparation.md)
3. [SQLite storage and SQL queries](docs/03_database.md)
4. [Harmonized explanatory analysis](docs/04_analysis.md)
5. [Old/new result comparison](docs/RESULT_COMPARISON.md)
6. [Release verification](docs/RELEASE_VERIFICATION.md) and [file selection](docs/GITHUB_FILE_REVIEW.md)
7. [Integration status](docs/INTEGRATION_STATUS.md)

## Concept presentation v3

[Editable PowerPoint](presentation/v3/presentation_concept_group_05_EN_v3.pptx), [PDF](presentation/v3/presentation_concept_group_05_EN_v3.pdf), [speaker notes](presentation/v3/speaker_notes_group_05_EN_v3.md) and [visual QA record](presentation/v3/QUALITY_REPORT_v3.md). The deck uses the harmonized results. It is a review draft, not evidence of group approval or Moodle submission. Speaker allocation and timing need agreement/rehearsal. The local PowerPoint build depends on machine-specific tools and paths and is intentionally not included; edit the canonical PPTX or regenerate analysis figures from Python.

## AI assistance

The group used ChatGPT for code suggestions, explanations, debugging and documentation. The original linked documents describe its use and limitations. Codex assisted the additional analysis, tests, reproduction tooling, documentation and presentation. See [AI_Log.md](AI_Log.md) for this feature branch; personal reflections and group acceptance remain open.

## Project team

Group 5: Leyla Erikci, Sharuya Kenkanathan and Kevin Thurnes.

## Review follow-up (20 November 2026)

The feature additions were committed and pushed on 19 November (cb3a894, fd57400, a7a9497). The path compatibility correction writes POSIX-relative manifest keys and also reads older Windows keys. Ten automated tests now include cross-platform key comparisons; this does not substitute for a native macOS full-pipeline rerun. Notebook 04 includes saved outputs. See [review follow-up](docs/REVIEW_FOLLOWUP_20261120.md) and [optional criteria](docs/ADDITIONAL_CRITERIA.md).

Concept presentation: approximately 10 minutes. Final project video: 5 minutes per member, therefore 15 minutes for Group 5; these are separate deliverables (official course PDF pages 2 and 4).
