# AI assistance log

## Feature analysis prepared before this publication

Based on the existing integration review dated 19 November 2026: Codex assisted the explanatory analysis module, Notebook 04, tests, reproduction scripts, figures, method documentation and concept presentation v3. Leyla's original notebooks 01–03 and method documents 01–03 retain their original AI declarations unchanged. This entry records tool assistance, not sole human authorship or completed individual reflection.

## Historical: 19 November 2026 - preparation before publication

The interrupted preparation left local changes only. The current instruction authorizes local technical corrections and isolated tests on `feat/harmonized-analysis` only. No commit, push, PR, merge or publication is authorized; explicit approval is required after the final report.

Codex inspected the prior change review and file inventory, checked the remote base, reviewed file selection, consolidated README/status information and prepared publication checks. Numerical verification results and dependency-install limits are recorded in `docs/RELEASE_VERIFICATION.md`. The scientific model and original data preparation were not changed during this publication pass.

Checks distinguish technical reproduction from scientific/group acceptance. The original review noted that exact floating-point JSON equality was unsuitable across execution environments; existing checks use numerical tolerances. No causal, equivalence or out-of-sample prediction claim follows from the reported results.

Still open: Leyla and Sharuya's scientific review, each member's own account of AI use and learning, agreement on presentation roles, rehearsal and Moodle submission. No personal reflection is fabricated by this log.

## Historical: controlled resumption, 19 November 2026

Codex checked the interrupted documentation changes, repaired damaged characters, and prepared a new isolated Windows installation and full saved-snapshot verification. Actual outcomes are recorded in docs/RELEASE_VERIFICATION.md. Source notebooks, data, models and presentation artifacts are preserved. No commit or push is performed.

## 20 November 2026 - reviewer feedback and corrective work

The first feature publication is complete: cb3a894 (environment), fd57400 (analysis), a7a9497 (documentation/presentation) were committed and pushed on 19 November. Kevin now authorizes targeted correction commits and a push to the same feature branch; no main push, force-push or merge is authorized.

Leyla reported independent Mac review and a KeyError for Windows-style manifest paths. Codex verified the platform-dependent key construction, added four regression tests (first observed failing), implemented POSIX output keys and normalization of legacy Windows keys, and retained checks for missing/conflicting paths. This corrects provenance plumbing; no regression formula, weights or harmonization rule changed.

Notebook 04 was executed and saved with metric/coefficient tables and one EDA graphic. AI assistance includes earlier code construction, raw/processed data checks, explanatory WLS and sensitivity implementation, debugging, numerical reproduction and native-editable slide preparation. The repository URL and the final-video duration clarification were added to the existing deck.

Observed limitations/failures: OS-specific manifest keys escaped the earlier Windows-only tests; earlier exact floating-point equality required tolerances; SQLite connections required explicit closure on Windows; a verification run during this correction correctly rejected concurrently edited presentation files. Final verification must use an immutable isolated copy. These are technical observations, not invented personal experiences.

Each member should answer in their own words:
1. Which AI tools did I actually use, and for which tasks?
2. Which suggestion did I verify independently, and how?
3. What did AI help me understand or save time on?
4. Which incorrect or unsuitable output did I encounter, and how was it corrected?
5. Which data/method/result can I now explain without AI?
6. What limitations and responsibilities remain, and what would I do differently?

Do not claim that any member has answered or approved this reflection until they do. The final slides and video must summarize the group's actual advantages, disadvantages and failed attempts.

## 20 November 2026 - line-ending follow-up

Leyla reported a remaining CRLF/LF hash failure after the path correction. Codex compared 17 input files against Git blobs, verified newline-only differences, added explicit Git attributes, retained historical byte hashes, and added narrow text-normalized hashes plus five regression tests. Two fresh Git-index checkout pipelines passed on Windows. No native Mac success is asserted. This records a concrete missed cross-platform assumption and its correction, not any member's personal reflection. See docs/LINE_ENDING_VERIFICATION.md.

## 22 November 2026 - concept presentation revision and map (Sharuya)

Sharuya used Claude (Anthropic) to review concept presentation v3 against the Moodle criteria and the lecture notes of 17 November, and to revise it into the final concept version (presentation/presentation_concept_group_05.pptx and .pdf). Claude added an outline, background and closing slide, a data excerpt with data types, the workflow and the reason for using regression, three hypotheses with their tests, clearer wording of the results (no causal language, R² 0.002 instead of 0.00) and speaker notes in simple English with a fair split between the three members. All numbers were taken from the existing files in data/processed and results/analysis; no new analysis was run.

Claude also wrote the map notebook maps/05_map.ipynb (municipality boundaries 2026 from BFS, GEOSTAT via swiss-maps 4.7.0, joined on the BFS number).

Problems found while using AI: some first suggestions were too strong or not supported by our data (for example "tariffs often change at cantonal borders") and were corrected after a second review. A first placement of the map notebook in notebooks/ would have changed the input hash manifest of src/analysis.py, so it was moved to maps/. A PowerPoint rendering difference (a table column not shown) was only found by checking the exported PDF.

Sharuya's personal reflection on AI use follows for the final submission.
