# 1. Data collection

We use the Federal Electricity Commission (ElCom) tariff data and the Federal Statistical Office (BFS) municipality register to compare household tariffs by municipality type and canton. Python retrieves the data directly from the official APIs.

## 1.1 ElCom electricity tariffs

| Item | Description |
|---|---|
| Publisher | Federal Electricity Commission (ElCom) |
| Access | [LINDAS SPARQL endpoint](https://ld.admin.ch/query) |
| Retrieval date | November 17, 2026 |
| Method | HTTP POST with a SPARQL query |
| Response format | JSON |
| Filters | 2026, H4 (4,500 kWh per year), standard product |

[ElCom tariff information](https://www.elcom.admin.ch/de/tarifdaten-und-visualisierungen)

SPARQL queries linked data. The notebook uses English query aliases for new requests. The retrieval metadata records the exact query used for the saved snapshot.

| Notebook column | Meaning |
|---|---|
| `municipality_uri` | Municipality identifier as a web address containing its municipality number |
| `operator_uri` | Operator identifier as a web address |
| `total_tariff` | Total tariff in Rp./kWh |

The original snapshot uses the field names `gemeinde`, `betreiber` and `gesamttarif`. Each row represents a municipality and operator for the selected year, profile and product. Municipalities served by several operators can have several valid rows.

| Initial quality check | Count |
|---|---:|
| Tariff rows | 2,268 |
| Distinct municipality URIs | 2,122 |
| Distinct operator URIs | 551 |
| Missing municipality URIs | 0 |
| Missing operator URIs | 0 |
| Missing total tariffs | 1 |
| Identical rows | 0 |
| Duplicate municipality–operator pairs | 0 |

The missing total concerns municipality URI number 3218 and operator URI number 326. It remains missing at collection time.

## 1.2 BFS municipality records

| Item | Description |
|---|---|
| Publisher | Federal Statistical Office (BFS) |
| Access | [Swiss Municipalities Application API](https://www.agvchapp.bfs.admin.ch/api/communes/levels?date=01-01-2026) |
| Retrieval date | November 17, 2026 |
| Method | HTTP GET |
| Response format | CSV |
| Municipality reference date | January 1, 2026 |

The original CSV has 29 columns. We select five fields.

| Source field | Meaning |
|---|---|
| `BfsCode` | BFS municipality number used for joining |
| `Name` | Official municipality name |
| `CantonId` | Canton identifier |
| `Canton` | Official canton name |
| `STALAN2020` | Urban–rural typology 2020 |

The typology version identifies the classification. The municipality reference date identifies the version of the municipality register.

The selected fields are complete, and all 2,110 municipality numbers are unique.

| STALAN2020 | Municipality type | Count |
|---|---|---:|
| 1 | Urban | 509 |
| 2 | Intermediate | 580 |
| 3 | Rural | 1,021 |
| Total | | 2,110 |

## 1.3 Storage and reproducibility

[The data collection notebook](../notebooks/01_data_collection.ipynb) loads the saved snapshots by default. With fresh collection enabled, it writes the API response bytes to `data/raw/` and saves a separate metadata file. File names include a UTC timestamp. Metadata records the source, retrieval time, selection criteria, row count and exact SPARQL query where applicable. Later retrievals may return different data.

## 1.4 Checks carried forward to data preparation

Collection retains every tariff row. The [preparation step](02_data_preparation.md) converts the tariff values to numbers, extracts the municipality numbers from ElCom URIs, handles the missing tariff and reconciles the 2,122 distinct ElCom municipality URIs with the BFS register using official municipality change notices.

## 1.5 AI assistance

The group used ChatGPT to help formulate API queries, write and explain Python code and document the workflow. The group ran the code in VS Code and checked counts, missing values and duplicates.

One debugging example was a `NameError` caused by using `elcom_raw` before running the retrieval cell. Running that cell made the response available for conversion to a table. This highlighted the need to run cells in order and check the resulting outputs.
