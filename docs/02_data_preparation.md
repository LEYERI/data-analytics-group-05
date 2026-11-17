# 2. Data preparation and integration

The [data preparation notebook](../notebooks/02_data_preparation.ipynb) joins saved ElCom tariffs to the BFS register to identify each tariff's municipality, canton and urban–rural type.

## 2.1 Prepare the data

We extract the municipality number from the ElCom URI and store it as a nullable integer (`Int64`) in both tables. We convert the total tariff to a numeric type, select and rename the BFS fields, and label the municipality types Urban, Intermediate and Rural. These steps preserve the row counts and retain the missing total tariff for review.

## 2.2 Check the initial join

A left join on the municipality number keeps all ElCom rows. The `validate="many_to_one"` setting checks that each key occurs at most once in the BFS table. The `indicator=True` setting flags matched and unmatched rows.

| Check | Count |
|---|---:|
| ElCom rows before the join | 2,268 |
| Tariff rows after the join | 2,268 |
| Matched tariff rows | 2,251 |
| Unmatched tariff rows | 17 |
| BFS municipalities without a direct match | 5 |

## 2.3 Harmonize municipality numbers

We checked unmatched numbers against official BFS municipality change notices. For 17 tariff rows, we assigned the municipality number in the January 1, 2026 register and retained the original ElCom number. The changes cover mergers, incorporations and Moutier's move from Bern to Jura. ElCom lists Moutier as 700, while the 2026 register lists it as 6831. After harmonization, all 2,268 rows match a BFS municipality.

The mapping table records the original and current numbers, the BFS change notice number and the official source link. In merged municipalities, tariffs recorded for former municipality areas are assigned to the current municipality. Tariffs may still vary across those areas. The analysis uses the BFS typology of the current municipality.

## 2.4 Consolidate identical tariff combinations

After harmonization, 23 rows belong to repeated current municipality–operator pairs. We keep one row for each distinct tariff value within each pair and retain different values separately. This consolidates 12 rows and leaves 2,256 rows. For example, Root retains both 25.414 and 25.153 Rp./kWh. The provenance table preserves all harmonized source rows.

## 2.5 Handle the missing tariff

We exclude one row whose total tariff is missing and record its reason as “Missing total tariff.” The affected municipality has another valid tariff in the dataset. The analysis uses observed tariff values only.

## 2.6 Final counts

| Step | Tariff rows |
|---|---:|
| ElCom raw data | 2,268 |
| After harmonizing municipality numbers | 2,268 |
| Identical rows consolidated | −12 |
| After deduplication | 2,256 |
| Rows excluded due to a missing total tariff | −1 |
| Cleaned tariff rows | 2,255 |

| Coverage | Municipalities |
|---|---:|
| Full BFS register | 2,110 |
| At least one valid tariff | 2,108 |
| No matching tariff in the snapshot | 2 |

Augst and Nürensdorf remain in the BFS reference table. Their absence from the tariff analysis reflects the coverage of the saved snapshot.

## 2.7 Saved tables

| File in `data/processed/` | Contents |
|---|---|
| `cleaned_tariffs.csv` | Matched tariff rows with valid totals |
| `bfs_municipalities_2026.csv` | Selected BFS reference fields |
| `municipality_number_mapping.csv` | Number changes and official sources |
| `tariff_provenance.csv` | All harmonized source rows |
| `excluded_tariffs.csv` | Excluded row and reason |
| `municipalities_without_tariffs.csv` | BFS records without a valid tariff in the snapshot |
| `cleaning_summary.csv` | Row counts and coverage checks |
| `operator_tariff_values.csv` | Mean of distinct tariff values for each municipality and operator |
| `municipality_values.csv` | One comparison tariff for each covered municipality |

## 2.8 Calculate municipality comparison values

1. Average the distinct tariff values within each municipality and operator.
2. Average the resulting operator values within each municipality.

Each operator receives equal weight within a municipality, and each municipality counts once in group comparisons. The table contains 2,108 municipality comparison tariffs with canton and urban–rural type. A paid household average would require customer or consumption shares, which are unavailable. The detailed tariff data remain available for further checks.

## 2.9 AI assistance

The group used ChatGPT to develop and explain the preparation code, look up official municipality change notices and draft documentation. The group ran the code and reviewed the tables, mappings and counts. The harmonization checks showed that several former municipalities can map to the same current municipality and operator. Comparing tariff values before consolidating the rows preserved distinct values.

## Sources

- [BFS municipality register for January 1, 2026](https://www.agvchapp.bfs.admin.ch/api/communes/levels?date=01-01-2026)
- [Official BFS change notices listed in the mapping table](../data/processed/municipality_number_mapping.csv)
- [ElCom tariff information](https://www.elcom.admin.ch/de/tarifdaten-und-visualisierungen)
