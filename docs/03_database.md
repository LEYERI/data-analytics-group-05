# 3. SQLite storage and SQL queries

The [database notebook](../notebooks/03_database.ipynb) stores the processed tables in SQLite and runs SQL queries directly from Python.

## 3.1 Build the database

The notebook uses Python's `sqlite3` module and pandas' `to_sql()` to build [the database](../data/electricity_tariffs.sqlite).

| Table | Contents | Rows |
|---|---|---:|
| `municipalities` | BFS reference data with official names, cantons and municipality types | 2,110 |
| `tariffs` | Cleaned individual tariff values | 2,255 |
| `municipality_values` | One comparison tariff per covered municipality | 2,108 |

All three tables use `municipality_number` as their join key. The `municipalities` table stores names, cantons and municipality types centrally. Before writing, Python checks that keys are present and unique in the reference and comparison tables and that all tariff and comparison keys exist in the reference table. The schema relies on these Python checks for key validation.

Rerunning the notebook replaces the three tables using the processed CSVs as inputs.

## 3.2 Run SQL from Python

The notebook runs each query with `pd.read_sql_query()` and returns a pandas DataFrame.

| Query | Purpose |
|---|---|
| [Table counts](../sql/01_table_counts.sql) | Check the counts of all three tables with `COUNT(*)` and `UNION ALL` |
| [Municipality values join](../sql/02_municipality_values_join.sql) | Attach reference details to municipality values with an `INNER JOIN` |
| [Tariffs by municipality type](../sql/03_tariffs_by_municipality_type.sql) | Use `GROUP BY`, `AVG`, `MIN` and `MAX` to summarize comparison tariffs |
| [Municipalities without tariffs](../sql/04_municipalities_without_tariffs.sql) | Find municipalities without a comparison value using a `LEFT JOIN` and `IS NULL` |

The inner join returns 2,108 rows, each with a unique municipality number. The type summary gives each municipality one observation. It is unadjusted, and the planned regression will account for canton. `ROUND()` displays the summary statistics to three decimal places. The database stores the full comparison values.

## 3.3 Municipalities without comparison tariffs

The left join identifies Augst in Basel-Landschaft and Nürensdorf in Zürich, matching the preparation results. The 2,108 municipalities with comparison values and the two without them account for all 2,110 BFS records.

## 3.4 Saved results

- [Table counts](../results/sql/table_counts.csv)
- [Tariffs by municipality type](../results/sql/tariffs_by_municipality_type.csv)
- [Municipalities without comparison tariffs](../results/sql/municipalities_without_tariffs.csv)

## 3.5 AI assistance

The group used ChatGPT to help write and explain Python and SQL code and document the workflow. The group ran the queries and checked the table counts, municipality-type summary and missing municipalities against the preparation results.
