# Old and harmonized results - Group 5

Local feature branch: feat/harmonized-analysis. Base: 9dc56db. No push, merge or publication.

Both old and new coefficients were recalculated with the same explanatory analysis implementation. Old coefficients, confidence intervals, p-values and fit metrics match the archived reference within 1e-8 relative / 1e-9 absolute tolerance.

| Measure | Old | Harmonized | Difference |
|---|---:|---:|---:|
| municipalities | 2105.000000 | 2108.000000 | +3.000000 |
| operator_values | 2250.000000 | 2254.000000 | +4.000000 |
| operators | 549.000000 | 551.000000 | +2.000000 |
| joint_p | 0.578248 | 0.558418 | -0.019830 |
| r2_in_sample | 0.390238 | 0.389970 | -0.000268 |
| rmse_in_sample | 2.506738 | 2.507856 | +0.001118 |
| Intermediate_estimate | -0.039282 | -0.039948 | -0.000666 |
| Intermediate_ci_low | -0.339836 | -0.338343 | +0.001492 |
| Intermediate_ci_high | 0.261272 | 0.258448 | -0.002824 |
| Intermediate_p_value | 0.797482 | 0.792673 | -0.004809 |
| Rural_estimate | -0.157729 | -0.162807 | -0.005079 |
| Rural_ci_low | -0.488271 | -0.492425 | -0.004154 |
| Rural_ci_high | 0.172814 | 0.166811 | -0.006003 |
| Rural_p_value | 0.349003 | 0.332366 | -0.016637 |

The main model still provides no statistically clear additional municipality-type association after canton adjustment. This is not an equivalence test or evidence that tariffs are identical. Both type confidence intervals include zero. R-squared and RMSE refer to weighted municipality/operator observations, not municipality averages.

Root/Herznach endpoint, operator-selection and exclusion scenarios have joint p-values from 0.551215 to 0.564679. Both type intervals include zero in every one of these cases. Effects of these two cases are small relative to model uncertainty. No pre-specified substantive equivalence margin was available; do not describe this as a formal equivalence result.

Larger operator omission scenarios sometimes reverse coefficient signs. The robust conclusion is uncertainty about an additional type association, not a firmly established negative direction. Complete results: sensitivity.csv.

Data: 2268 raw rows; 17 historical identifiers harmonized; 12 identical combinations consolidated; one missing tariff excluded; 2255 tariff rows, 2254 operator values, 2108 municipalities, 551 operators, 133 multi-operator municipalities. No source raw data, preparation notebook or existing SQLite file changed.

Checks: all four notebooks freshly executed without network in a temporary copy after removing derived outputs; 19 CSV tables, all three SQLite tables, four SQL queries and four regenerated figures checked. Six unit/integration tests include independent least-squares point estimates and a manually constructed two-way cluster sandwich. See reproduction.json.

Historical comparison was produced in the existing Python 3.12.4 environment. A fresh isolated Windows installation and full reproduction subsequently passed on 19 November 2026; see RELEASE_VERIFICATION.md. Presentation v3 is available and consistent with these results. Group approval and rehearsal remain open.