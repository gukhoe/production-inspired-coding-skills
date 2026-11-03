# Final code completeness rubric v1 — English edition

Original freeze time: 2026-11-02T23:48:00Z. This English edition describes the historical rubric; the hash-bound Korean original is in [historical-originals.zip](../../sources/historical-originals.zip). Translation does not create a new pre-experiment freeze.

This is a post-experiment static review, not an independent generation trial. Do not change original code. Do not deduct for unrequested GUI/API/deployment/database features or reward line count, document volume or class count.

**Mandatory request fulfillment (M):** runnable Python using supplied input and performing the requested calculation, selection, ranking or output. Record PASS/PARTIAL/FAIL from existing execution evidence and static inspection. Do not combine this judgment with optional maintenance ratings.

**Optional maintenance readiness:** each dimension is 0/1/2. Zero means no evidence of the improvement or a clear defect; one is the basic level appropriate to a small task; two is demonstrated additional usefulness within scope. A low rating does not mean the original request failed. Record evidence and function/file locations; do not produce a summed score.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| S: structure/readability | Flow, naming or coupling clearly obstructs understanding | Concise, understandable procedures/functions | Calculations separated from examples/I/O, with clear naming and policy explanations |
| R: reuse | Changing input/calculation requires editing logic | Callable calculation or independently replaceable data | Inputs as arguments, returned results, no example side effects on import |
| E: errors/boundaries | Incorrect result or unexplained failure on objectively invalid input, or no validation evidence | Some relevant handling or explicit policy | Major objective errors handled explainably and valid boundaries addressed |
| T: self-tests | No assertions with independent expectations; example output only | Assertions establish normal calculations | Normal checks plus meaningful boundaries, invariants or error-policy checks |
| D: usage/execution documentation | Execution or input/output meaning is hard to determine | Names, example and main structure establish basic use | Brief explicit execution instructions or argument/result/unit/policy documentation improves reuse |

Complex abstraction earns no credit without useful effect. JSON CLI and README files are not mandatory. Error review considers zero denominators, invalid dates, inappropriate types and missing fields. Unspecified policies for negative values, overpayments or early completion may accept or reject inputs without automatic deduction; overly restrictive valid-input contracts should be identified separately. Test meaning matters more than counts. Copied implementation logic or an incorrect oracle should be flagged.

Hide group labels as far as possible while reading code. Style can reveal skill use and the reviewer knew prior aggregates, so do not claim full blinding. The original rubric proposed task/group dimension summaries after independent artifact ratings; the published completeness review explicitly treats labels qualitatively and does not use a total ranking. This is post-hoc analysis of 10 small arithmetic tasks, with no claim of statistical significance or general causal effect.
