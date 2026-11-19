# Harmonized explanatory analysis
Approved by Kevin on 19 November 2026. Group 5: Leyla Erikci, Sharuya Kenkanathan, Kevin Thurnes.

## Data and estimand
Keep the original data collection, preparation and database notebooks unchanged. Read their outputs. The snapshot contains 2268 tariff rows; harmonize 17 historical identifiers, consolidate 12 identical municipality/operator/tariff combinations and exclude one missing tariff: 2255 distinct tariff rows. Average distinct tariffs within municipality/operator: 2254 operator values. Average operators equally: 2108 municipalities, 551 operators; 133 municipalities have multiple operators. The BFS register contains 2110 municipalities; Augst and Nuernensdorf lack valid tariffs. No imputation.

Official 2026 municipality boundaries, including Moutier in Jura, define the unit and canton. The 17 mapping sources remain in data/processed/municipality_number_mapping.csv. Root retains CKW tariffs 25.153 and 25.414 before averaging to 25.2835. Herznach-Ueken retains operator 356 at 24.047 and operator 5 at 27.892 before averaging to 25.9695. The current AEW municipality ID does not identify its precise historical service territory.

These are standardized comparison values, not paid household averages. Equal weights for distinct tariffs, operators, then municipalities are modeling choices; official municipality changes do not prescribe these weights. Historical source rows remain in tariff_provenance.csv.

## Model
The unit of regression is a municipality/operator comparison value. WLS weights are 1 / number of operators in that municipality, recalculated in every subset. Their sum is 1 per municipality. They are target weights, not asserted inverse error variances. Outcome: H4 standard total tariff 2026, Rp./kWh excluding VAT. Predictors: categorical municipality type (Urban reference) and canton. Fit canton-only and type-only models as comparisons.

Inference uses two-way cluster covariance by municipality and operator, finite-sample corrections, t intervals, and a joint F test of the two type terms. This allows shared operator dependence but does not eliminate omitted variables or all spatial dependence. Coefficients are descriptive adjusted associations, not causal effects. Individual p-values and Holm adjustments are exported. Model fit is weighted in-sample R-squared and RMSE at the municipality/operator observation level, not at the level of municipality means; neither is out-of-sample forecast performance. Do not compare R-squared across different outcome aggregations as if they measured identical targets.

## Sensitivities
Root: both distinct endpoints and exclusion. Herznach-Ueken: both endpoint outcomes with the original operator membership held fixed, plus separate scenarios retaining ONLY operator 356 or ONLY operator 5 with reweighting. The endpoint scenarios are stress tests, not claims that both operators actually charge that value. Also test all four joint endpoint combinations and exclusion of both municipalities. Moutier exclusion, municipality minimum/maximum, single-operator municipalities, omission of the ten largest absolute residual municipalities, and separate omission of each of the five operators covering most municipalities are supplementary checks.

Minimum/maximum scenarios assign each municipality's endpoint to its operator rows, preserving the original cluster membership. They change the estimand and are not independently observed tariffs or causal counterfactuals. Exclusion scenarios change the population. Stability means stability within these specified scenarios; failure to reject is not proof of equality. Coefficient signs may vary in large-operator omissions.

## Reproduction
Use Python 3.12 with `python -m pip install -r requirements.txt -c constraints-tested.txt`. The Windows lock is platform-specific. Then run `python -m unittest discover -s tests -v`, `python -m src.analysis`, and `python scripts/verify_pipeline.py` from the root. Notebook 04 is a thin, executable presentation of the same analysis module. Existing notebooks are run in a temporary copy with network disabled. No source tables are overwritten by verification. A fresh install from these requirements remains a distinct check from reproduction in the existing verified environment.

Numerical reproducibility uses tolerances 1e-9. Raw files and source notebooks are hashed. Regenerated CSV bytes may differ in float serialization while values agree; differences are listed explicitly. All three database tables and four SQL queries are checked. WLS point estimates are independently checked with numpy least squares. The automated tests cover distinct-tariff deduplication, normalization after operator removal, duplicate keys and missing values.

## AI assistance and ownership
Leyla's existing notebooks and AI documentation are retained unchanged. Codex added analysis code, tests, reproduction tooling, figures and integration documentation on the local feature branch. The group must review the methodology, outputs and presentation. No group review or personal reflection is presumed complete.
