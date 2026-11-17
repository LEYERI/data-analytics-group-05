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
| Unit of analysis | Municipality |
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
| Exploratory data analysis | Pending |
| Regression and model evaluation | Pending |
| Final interpretation and presentation | Pending |

We join the sources by BFS municipality number and use official change notices to document municipality number updates.

We first average distinct tariff values within each municipality and operator, then average the operator values within each municipality. This gives each operator equal weight within a municipality and yields one comparison value per municipality. Interpreting it as an average tariff paid by households would require customer or consumption shares, which are unavailable.

## Data coverage

| Measure | Count |
|---|---:|
| ElCom tariff rows in the saved response | 2,268 |
| BFS municipality records | 2,110 |
| Cleaned tariff rows | 2,255 |
| Municipality comparison values | 2,108 |

After harmonizing municipality numbers, we consolidate 12 identical municipality–operator–tariff combinations and exclude one row with a missing total tariff. Augst and Nürensdorf have no matching tariff in the saved snapshot. Canton adjustment is planned for regression. The current SQL summary compares municipality types descriptively.

## Project structure

| Path | Contents |
|---|---|
| `notebooks/` | Jupyter notebooks with code and explanations |
| `data/raw/` | Original API responses and retrieval metadata |
| `data/processed/` | Processed tables and cleaning records |
| `data/electricity_tariffs.sqlite` | SQLite database |
| `sql/` | Saved SQL queries |
| `results/sql/` | SQL summaries exported as CSV |
| `docs/` | Detailed project documentation |

## Run the notebooks in VS Code

Open the repository in VS Code with the Python and Jupyter extensions. Select a Python 3 kernel with `requests` and `pandas` installed. If needed, install them in a notebook cell.

```python
%pip install requests pandas
```

Run the cells from top to bottom in this order.

1. [Data collection](notebooks/01_data_collection.ipynb) loads and checks the saved responses by default. Set `fetch_new_data = True` to retrieve new, timestamped snapshots over the internet.
2. [Data preparation](notebooks/02_data_preparation.ipynb) integrates the saved responses. If several snapshots exist, explicitly select the files to analyze.
3. [SQLite and SQL](notebooks/03_database.ipynb) rebuilds the three tables from the processed CSVs and exports the query results. `sqlite3` is part of Python's standard library.

## Documentation

The project was originally written in German and was translated into English with the help of AI. The analysis uses the original methodology and calculations.

1. [Data collection](docs/01_data_collection.md)
2. [Data preparation and integration](docs/02_data_preparation.md)
3. [SQLite storage and SQL queries](docs/03_database.md)

## AI assistance

The group used ChatGPT for code suggestions, explanations, debugging and documentation. The linked documents describe how it was used, what the group checked and the limitations encountered.

## Project team

The group will add all members' names before submission.
