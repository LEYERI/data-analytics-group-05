# English speaker notes - Group 5 - v3

Planned presentation: 24 November 2026. Ten main slides, four reserve slides. Approximately 1082 spoken words plus chart explanations, pauses and transitions. Timing target: 600 seconds; rehearse aloud.

Proposed allocation (not agreed): Leyla slides 1-4, 3:40; Sharuya slides 5-7, 3:05; Kevin slides 8-10, 3:15. Names may be exchanged. Aim to explain freely, using these paragraphs as rehearsal guidance rather than reading them verbatim.

## Slide 1: Where you live and what electricity costs
Target: 30 seconds. Suggested speaker: Leyla (proposal).

Hello everyone. We are Leyla Erikci, Sharuya Kenkanathan and Kevin Thurnes, Group 5. Our project compares household electricity tariffs across Swiss municipalities. We ask whether urban, intermediate and rural municipalities differ, and what remains when we account for the canton. We will introduce the data and comparison rules, show two preliminary findings, and explain the work that remains.

Sources: Project definition and group information supplied by the group.

## Slide 2: Research question and relevance
Target: 65 seconds. Suggested speaker: Leyla (proposal).

Electricity tariffs make a familiar cost difference measurable. We use the official H4 consumption profile of 4,500 kilowatt-hours per year and the standard product for 2026. Holding that profile constant gives us a common basis for comparison. A difference of one Swiss cent per kilowatt-hour corresponds to 45 francs per year at that consumption level. These are standardised costs, excluding VAT, rather than a prediction of any individual household's bill. Our question is: how do household tariffs differ between urban, intermediate and rural municipalities, and which differences remain after accounting for the canton? This is relevant to households comparing locations and to municipalities discussing local costs. We examine associations. We do not claim that a municipality's type causes its tariff.

Sources: ElCom, Frequently asked questions on electricity tariffs (2026 H4 profile): https://www.elcom.admin.ch/de/faq-stromtarife . Standardised annual conversion: tariff in Rp./kWh x 45. Project scope: analysis.py and README.md.

## Slide 3: Two official sources, one matching key
Target: 60 seconds. Suggested speaker: Leyla (proposal).

We combine two official sources. ElCom supplies the 2026 H4 standard tariffs through the LINDAS SPARQL interface. The Federal Statistical Office supplies municipality identifiers, canton and the urban-rural classification for the boundaries of January 2026. We join on the BFS municipality number. The repository contains Python collection code, timestamped responses from 17 November, and the exact query. A separate live retrieval was checked on 18 November. For this version, all four notebooks ran again from the saved responses with network access disabled. Their regenerated tables matched. This separates collection evidence from reproducibility. The remaining group task is to review and explain the workflow together. We retrieve total tariffs and identifiers here; we do not claim to analyse tariff components.

Sources: Harmonized project: docs/04_analysis.md; data/processed/; results/analysis/; official sources in appendices. API retrieval evidence: raw metadata and separate 18 November retrieval report.

## Slide 4: Integration has a traceable audit trail
Target: 65 seconds. Suggested speaker: Leyla (proposal).

The ElCom snapshot contains 2,268 tariff rows, while the BFS reference lists 2,110 municipalities. Seventeen tariff rows use historical identifiers. We reconcile them with official municipality changes, including Moutier moving to Jura. We keep those original identifiers in a provenance table. After harmonization, twelve rows repeat an identical municipality, operator and tariff combination. We consolidate those combinations and exclude one row with a missing total tariff. The result is 2,255 distinct tariff rows covering 2,108 municipalities and 551 operators. Augst and Nuernensdorf have no valid tariff in this snapshot. These are coverage gaps, not zero tariffs. The existing SQLite database and SQL summaries remain part of the reproducible workflow.

Sources: Harmonized project: docs/04_analysis.md; data/processed/; results/analysis/; official sources in appendices. API retrieval evidence: raw metadata and separate 18 November retrieval report.

## Slide 5: Every municipality receives equal weight
Target: 55 seconds. Suggested speaker: Sharuya (proposal).

Our comparison gives every municipality equal overall weight. We first average distinct tariff values for the same municipality and operator. Root illustrates why: CKW reports two different values for its current territory. We keep both before taking their mean. We then give each operator equal weight within the municipality. This produces 2,254 municipality-operator observations. Of the covered municipalities, 133 have more than one operator. In regression, each operator observation receives one divided by its municipality's operator count, so the total weight is one. Descriptive charts use the resulting municipality mean. Customer and consumption shares are unavailable. This is a transparent comparison convention, not the tariff paid by the average household.

Sources: Harmonized project: docs/04_analysis.md; data/processed/; results/analysis/; official sources in appendices. API retrieval evidence: raw metadata and separate 18 November retrieval report.

## Slide 6: Pilot tariffs overlap strongly across groups
Target: 60 seconds. Suggested speaker: Sharuya (proposal).

The boxplot shows one comparison tariff for each municipality. The line in each box is the median. The box covers the middle half of observations, and points beyond the whiskers show more extreme values. We have 508 urban, 579 intermediate and 1,021 rural municipalities. Their medians are approximately 27.70, 27.89 and 27.90 Swiss cents per kilowatt-hour. The central distributions overlap substantially. Rural municipalities also include particularly low and high observations. These are descriptive pilot results based on the harmonized data. They do not account for the distribution of municipality types across cantons. We therefore use a regression model to distinguish the raw group comparison from the comparison adjusted for canton.

Sources: Harmonized project: docs/04_analysis.md; data/processed/; results/analysis/; official sources in appendices. API retrieval evidence: raw metadata and separate 18 November retrieval report.

## Slide 7: Regression separates type and canton associations
Target: 70 seconds. Suggested speaker: Sharuya (proposal).

We fit three explanatory models: canton alone, municipality type alone, and both together. The main model uses the total tariff as the outcome and treats municipality type and canton as categories. Urban municipalities are the reference group. The two type coefficients describe adjusted differences from that reference. We keep equal total weight for each municipality. Because observations can share an operator or a municipality, we allow the uncertainty calculation to cluster along both dimensions. This does not account for every geographical dependency or unobserved factor. Weighted R-squared and RMSE describe in-sample fit to municipality-operator observations. They do not measure performance on future years or new operators. Our question concerns associations in this cross-section, not causal effects.

Sources: Harmonized project: docs/04_analysis.md; data/processed/; results/analysis/; official sources in appendices. API retrieval evidence: raw metadata and separate 18 November retrieval report.

## Slide 8: Pilot adjusted differences remain uncertain
Target: 80 seconds. Suggested speaker: Kevin (proposal).

The intermediate coefficient is about minus 0.040 Swiss cents per kilowatt-hour, and the rural coefficient about minus 0.163. Both 95-percent confidence intervals cross zero. The joint test of both type terms gives a p-value of 0.5584. Our conclusion is therefore cautious: this model does not show a statistically clear additional type association after accounting for canton. That is not proof that the groups are equal. At the H4 consumption level, the rural point estimate corresponds to roughly seven francs per year, but its uncertainty spans negative and positive differences. R-squared is about 0.390 and weighted RMSE about 2.508 Swiss cents per kilowatt-hour. Adding type to the canton-only model changes fit very little. These are in-sample statistics, not forecasts or percentages of causes explained.

Sources: Harmonized project: docs/04_analysis.md; data/processed/; results/analysis/; official sources in appendices. API retrieval evidence: raw metadata and separate 18 November retrieval report.

## Slide 9: Open checks define the next stage
Target: 65 seconds. Suggested speaker: Kevin (proposal).

We checked whether special aggregation choices drive the conclusion. For Root and Herznach-Ueken, we tested tariff endpoints and exclusions. For Herznach-Ueken, we also retained each operator separately and recalculated the weights. Across these special-case checks, joint p-values range from about 0.551 to 0.565, and both type intervals always include zero. The cautious main interpretation remains unchanged. Across all 24 scenarios, we also examined alternative aggregation and influential observations or operators. Omitting large operators can change coefficient signs, so we do not claim a reliable negative direction. The general limitations remain one year, standard products, unknown customer shares and unobserved local factors. Group review and personal AI reflection are still open.

Sources: Harmonized project: docs/04_analysis.md; data/processed/; results/analysis/; official sources in appendices. API retrieval evidence: raw metadata and separate 18 November retrieval report.

## Slide 10: Expected contribution and next deliverables
Target: 50 seconds. Suggested speaker: Kevin (proposal).

Our contribution is a transparent comparison of raw and canton-adjusted tariff differences, including the uncertainty and limits of that comparison. We have collected official data, documented integration, stored them in SQLite and reproduced the pilot analysis. Before the final submission, we will review the results together, agree on the interpretation and complete the individual AI reflections. We also need to prepare the final PDF, materials package and fifteen-minute final video, five minutes per person; this concept talk remains ten minutes. AI supported code, debugging and slide preparation. We document its contributions and failures, while remaining responsible for explaining the work ourselves. For this concept presentation, we welcome feedback on the comparison rule and the scope of our conclusions.

Sources: Harmonized project: docs/04_analysis.md; data/processed/; results/analysis/; official sources in appendices. API retrieval evidence: raw metadata and separate 18 November retrieval report.

## Reserve slide 11
Reserve only. These scenarios test specific choices, not equivalence. Endpoint stress tests hold cluster membership fixed; operator-selection scenarios remove the unselected operator. Complete 24 scenarios: results/analysis/sensitivity.csv.

## Reserve slide 12
Reserve only. ElCom and BFS official API sources are shown. Exact query and timestamps are in raw metadata. Snapshot dated 17 November. Separate live retrieval verified 18 November. Four notebooks reproduced offline for harmonized analysis.

## Reserve slide 13
Reserve only. Methods, reproducibility and official course rubric. Group review and personal AI reflection remain open. The concept presentation is planned for 24 November 2026. Confirm the assigned slot and Moodle upload logistics with the group.

## Reserve slide 14
Official municipality changes: BFS notices 3990, 3969, 3999, 3997 and 4000. These establish geographical mappings, not customer weights. Full mapping table: data/processed/municipality_number_mapping.csv.

## Source and evidence index
- ElCom tariff information: https://www.elcom.admin.ch/de/tarifdaten-und-visualisierungen
- H4 profile: https://www.elcom.admin.ch/de/faq-stromtarife
- SPARQL endpoint: https://ld.admin.ch/query
- BFS reference: https://www.agvchapp.bfs.admin.ch/api/communes/levels?date=01-01-2026
- All historical mappings and official links: ../../data/processed/municipality_number_mapping.csv
- Methods: ../../docs/04_analysis.md
- Results and numerical evidence: ../../results/analysis/
- Separate live collection evidence: finalisation_group05_20261118/evidence/live_api/retrieval_report.json in the preserved local project archive.
- Official concept rubric: Moodle_Projektanforderungen.pdf, pages 2-3; local course capture dated 18 September 2026.
- WLS: https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.WLS.html
- Two-way cluster covariance: https://www.statsmodels.org/stable/generated/statsmodels.stats.sandwich_covariance.cov_cluster_2groups.html