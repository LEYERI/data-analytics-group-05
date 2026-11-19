# Presentation v3 - quality report
Stand: 19 November 2026. Group 5. Local delivery only, not approved by the whole group and not submitted.

## Official concept rubric
Source: Moodle_Projektanforderungen.pdf, pages 2-3, course capture 18 September 2026. Eight separately graded criteria; this report assesses coverage, not a promised grade.

| Official criterion | Evidence | Assessment |
|---|---|---|
| 1 Structure & outline | Slide 1 title/names; spoken introduction gives route; question, data, methods, pilot, next steps | Covered; ten main slides, logical sequence |
| 2 Background & problem | Slide 2 standardized household tariff comparison and annual cost scale | Covered |
| 3 Objective & research question | Explicit question on slide 2, repeated in interpretation | Covered |
| 4 Data | Slides 3-5, appendices 12 and 14; sources, keys, losses, units and weights | Covered |
| 5 Methods | Slide 7 and methods appendix; justified explanatory WLS and two-way clustering | Covered; limitations explicit |
| 6 Expected results | Slides 8-10 distinguish reproduced pilot and intended contribution | Covered; no causal or predictive overclaim |
| 7 Language: freely spoken | English notes, timed blocks and proposed distribution | Prepared, but cannot be confirmed until the group rehearses/delivers |
| 8 Scientific presentation quality | Units, uncertainty, source references; native editable plots and tables; rendered slide review | Checked; no visual clipping observed |

## Numerical and technical checks
- 2108 municipalities; 2255 distinct tariff rows; 2254 municipality/operator model observations; 551 operators. These are different counts, not contradictions.
- Adjusted differences: Intermediate -0.0399 and Rural -0.1628 Rp./kWh. Joint p=0.5584, weighted R-squared=0.38997 and RMSE=2.50786.
- In-sample fit is defined at the weighted municipality/operator level. Customer-weighted actual bills and causal effects are explicitly excluded.
- Boxplot geometry recomputed directly from municipality_values.csv, including all outliers. Coefficient positions and confidence intervals read from current coefficient CSV. Sensitivity table read from current sensitivity CSV.
- All 14 slides rendered in PowerPoint and visually inspected. No text-height overflow warnings. Original visual language, dimensions, typefaces and palette retained.
- PowerPoint contains native text, tables and editable vector chart marks, no raster slide images. Charts are editable shapes, not Excel-linked chart objects.
- PDF exported directly from the same PowerPoint using PowerPoint's PDF exporter. Fourteen pages. Main-slide extracted text matches the PPTX; source-page extraction repeats hyperlink text, a PDF extraction artifact checked separately. All 14 PDF pages were also rendered and visually compared with the PowerPoint render; no content/layout discrepancies observed.
- Protected original presentation and analysis CSV hashes unchanged. No original data or prior presentations overwritten.
- Notes are embedded in the PPTX and provided separately. About 1082 spoken words, plus explanations and pauses; 600-second target. Actual timing and free delivery require rehearsal.

## Collection evidence versus open work
Repository Python/API code and saved responses dated 17 November are available. Separate local archive evidence records the successful 18 November live collection. The harmonized notebooks were reproduced offline. This deck does not claim a new API collection in this phase or completed group review.

## Proposed speaker allocation (not agreed)
Leyla: slides 1-4, 3:40. Sharuya: slides 5-7, 3:05. Kevin: slides 8-10, 3:15. The group can exchange these blocks. Four reserve slides are outside the ten-minute allocation.

## Remaining decisions and actions
Group scientific approval, speaker allocation, timed rehearsal, and personal AI reflection. Confirm the assigned 24 November slot and actual Moodle upload logistics. No upload, push, merge or PR created. The local Python environment's clean installation on another system remains a project-level open check, not a claimed presentation achievement.

## Changes from the previous English deck
Historical IDs are now harmonized rather than excluded. Counts and two-stage weighting updated. Boxplots and regression geometry regenerated. Old coefficients, p=0.578 and old ANOVA results removed. New Root/Herznach sensitivities replace the old appendix. Collection/reproduction/group-review statuses separated. Full relevant BFS source appendix added. Existing original files preserved.
