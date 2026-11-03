# Software Assurance Audit Report

Template: 1.0 | Standard: 0.2.0

Outcome: **incomplete**

Scope: Blank standard form; no project has been audited
Revision: `UNASSESSED-SNAPSHOT`

Evidence hashes verify artifact identity, not truth or adequacy. Supported means a named reviewer attested to evidence for this scope/revision. Graph freshness and runtime behavior are not established by a graph export. Scores describe reviewed evidence maturity, not safety certification.

## Scope issues

- scope_completeness_unverified
- process_inventory_empty

## Evidence maturity scores

Scores describe reviewed evidence maturity, not failure probability or release authorization. Unknowns lower coverage; their zero contribution to the achievement lower bound is not a defect verdict.

| Stage | Observed score % | Weighted coverage % | Achievement lower bound % | Scored / total |
|---|---|---|---|---|
| overall | None | 0.0 | 0.0 | 0 / 72 |
| change | None | 0.0 | 0.0 | 0 / 3 |
| dependencies | None | 0.0 | 0.0 | 0 / 3 |
| design | None | 0.0 | 0.0 | 0 / 6 |
| diagnosis | None | 0.0 | 0.0 | 0 / 6 |
| handoff | None | 0.0 | 0.0 | 0 / 3 |
| implementation | None | 0.0 | 0.0 | 0 / 6 |
| improvement | None | 0.0 | 0.0 | 0 / 6 |
| operations | None | 0.0 | 0.0 | 0 / 6 |
| prevention | None | 0.0 | 0.0 | 0 / 6 |
| release | None | 0.0 | 0.0 | 0 / 6 |
| requirements | None | 0.0 | 0.0 | 0 / 6 |
| risk | None | 0.0 | 0.0 | 0 / 3 |
| scope | None | 0.0 | 0.0 | 0 / 3 |
| verification | None | 0.0 | 0.0 | 0 / 9 |

## Controls

| Control | Stage | Status / score | Review, finding and improvement |
|---|---|---|---|
| REQ-01 | requirements | unverified / None | Requirements have measurable acceptance criteria: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| REQ-02 | requirements | unverified / None | Critical scenarios and exclusions are explicit: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| DES-01 | design | unverified / None | Components have defined inputs, outputs and ownership: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| DES-02 | design | unverified / None | Cross-component contracts and failure modes are reviewed: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| SUP-01 | dependencies | unverified / None | External dependencies and supplier changes are controlled: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| IMP-01 | implementation | unverified / None | Changes trace to requirements and reviewed source: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| IMP-02 | implementation | unverified / None | Input, authorization and state invariants are enforced: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| VER-01 | verification | unverified / None | Tests exercise acceptance criteria and meaningful oracles: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| VER-02 | verification | unverified / None | Negative paths and interface failures are exercised: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| VER-03 | verification | unverified / None | Test environment, source revision and results are traceable: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| REL-01 | release | unverified / None | Release artifacts and configuration are reproducible: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| REL-02 | release | unverified / None | Migration, compatibility and rollback are verified: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| OPS-01 | operations | unverified / None | Failures are observable and actionable: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| OPS-02 | operations | unverified / None | Recovery and degraded operation are exercised: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| CHG-01 | change | unverified / None | Change impact covers connected processes and consumers: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| RSK-01 | risk | unverified / None | Failure modes, impact and missing controls are documented: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| CAP-01 | improvement | unverified / None | Corrective actions have ownership and verification: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| MAP-01 | scope | unverified / None | Process and interface inventory completeness is reviewed: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| PRE-01 | prevention | unverified / None | Invalid actions are prevented before harmful state changes: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| PRE-02 | prevention | unverified / None | Detected failures stop or contain affected work safely: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| GAT-01 | handoff | unverified / None | Stage transitions have reviewed entry and exit evidence: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| DIA-01 | diagnosis | unverified / None | Failure reproduction distinguishes observations from hypotheses: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| DIA-02 | diagnosis | unverified / None | Root-cause claims survive discriminating counterexamples: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |
| CAP-02 | improvement | unverified / None | Corrections prevent recurrence without breaking adjacent behavior: Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.. Finding: . Improvement: .  |

## Standard checkpoint results

| ID | Checkpoint | Status | Score / 4 | Evidence IDs | Reviewer / rationale | Finding | Improvement | Owner | Due | Evidence issues |
|---|---|---|---|---|---|---|---|---|---|---|
| REQ-01.1 | Identify the user-visible outcome | unverified | unscored |  | :  |  |  |  |  |  |
| REQ-01.2 | Define observable acceptance limits before implementation | unverified | unscored |  | :  |  |  |  |  |  |
| REQ-01.3 | Trace each selected requirement to a verification scenario | unverified | unscored |  | :  |  |  |  |  |  |
| REQ-02.1 | State critical use and misuse scenarios | unverified | unscored |  | :  |  |  |  |  |  |
| REQ-02.2 | Record exclusions and affected users | unverified | unscored |  | :  |  |  |  |  |  |
| REQ-02.3 | Define unacceptable data/state outcomes | unverified | unscored |  | :  |  |  |  |  |  |
| DES-01.1 | Name inputs and outputs | unverified | unscored |  | :  |  |  |  |  |  |
| DES-01.2 | Identify accountable owner and consumer | unverified | unscored |  | :  |  |  |  |  |  |
| DES-01.3 | Define state and lifetime invariants | unverified | unscored |  | :  |  |  |  |  |  |
| DES-02.1 | Review both sides of each selected interface | unverified | unscored |  | :  |  |  |  |  |  |
| DES-02.2 | Specify error, timeout and cancellation behavior | unverified | unscored |  | :  |  |  |  |  |  |
| DES-02.3 | Trace shared-state and version compatibility assumptions | unverified | unscored |  | :  |  |  |  |  |  |
| SUP-01.1 | Identify external services and version/configuration dependencies | unverified | unscored |  | :  |  |  |  |  |  |
| SUP-01.2 | Review change and outage handling | unverified | unscored |  | :  |  |  |  |  |  |
| SUP-01.3 | Record provenance and replacement/recovery strategy | unverified | unscored |  | :  |  |  |  |  |  |
| IMP-01.1 | Link source changes to acceptance requirements | unverified | unscored |  | :  |  |  |  |  |  |
| IMP-01.2 | Review changed and shared paths | unverified | unscored |  | :  |  |  |  |  |  |
| IMP-01.3 | Preserve source identity and review rationale | unverified | unscored |  | :  |  |  |  |  |  |
| IMP-02.1 | Reject invalid or unauthorized actions before mutation | unverified | unscored |  | :  |  |  |  |  |  |
| IMP-02.2 | Handle duplicate/stale observations | unverified | unscored |  | :  |  |  |  |  |  |
| IMP-02.3 | Test protected data and other-user isolation | unverified | unscored |  | :  |  |  |  |  |  |
| VER-01.1 | Use observable assertions tied to requirements | unverified | unscored |  | :  |  |  |  |  |  |
| VER-01.2 | Show the oracle rejects an incorrect result | unverified | unscored |  | :  |  |  |  |  |  |
| VER-01.3 | Explain fixture limitations and untested behaviors | unverified | unscored |  | :  |  |  |  |  |  |
| VER-02.1 | Exercise malformed/failed inputs | unverified | unscored |  | :  |  |  |  |  |  |
| VER-02.2 | Exercise delay, cancellation and partial completion | unverified | unscored |  | :  |  |  |  |  |  |
| VER-02.3 | Verify the downstream state after failure and recovery | unverified | unscored |  | :  |  |  |  |  |  |
| VER-03.1 | Bind results to source and environment | unverified | unscored |  | :  |  |  |  |  |  |
| VER-03.2 | Retain exact commands and raw outputs | unverified | unscored |  | :  |  |  |  |  |  |
| VER-03.3 | Distinguish fresh runs from historical claims | unverified | unscored |  | :  |  |  |  |  |  |
| REL-01.1 | Identify reproducible build inputs and output artifacts | unverified | unscored |  | :  |  |  |  |  |  |
| REL-01.2 | Verify configuration and dependency provenance | unverified | unscored |  | :  |  |  |  |  |  |
| REL-01.3 | Distinguish candidate from installed and live evidence | unverified | unscored |  | :  |  |  |  |  |  |
| REL-02.1 | Test backward/forward compatibility as applicable | unverified | unscored |  | :  |  |  |  |  |  |
| REL-02.2 | Interrupt a migration or installation safely | unverified | unscored |  | :  |  |  |  |  |  |
| REL-02.3 | Verify rollback restores a consistent usable state | unverified | unscored |  | :  |  |  |  |  |  |
| OPS-01.1 | Detect failed and stalled work | unverified | unscored |  | :  |  |  |  |  |  |
| OPS-01.2 | Provide actionable diagnostics without sensitive leakage | unverified | unscored |  | :  |  |  |  |  |  |
| OPS-01.3 | Distinguish healthy service response from useful workflow progress | unverified | unscored |  | :  |  |  |  |  |  |
| OPS-02.1 | Bound recovery and retries | unverified | unscored |  | :  |  |  |  |  |  |
| OPS-02.2 | Test degraded mode and cancellation | unverified | unscored |  | :  |  |  |  |  |  |
| OPS-02.3 | Verify progress resumes without harming adjacent users | unverified | unscored |  | :  |  |  |  |  |  |
| CHG-01.1 | Trace callers and downstream consumers | unverified | unscored |  | :  |  |  |  |  |  |
| CHG-01.2 | Check shared data/configuration/process boundaries | unverified | unscored |  | :  |  |  |  |  |  |
| CHG-01.3 | Exercise an affected neighboring workflow | unverified | unscored |  | :  |  |  |  |  |  |
| RSK-01.1 | State failure and user impact | unverified | unscored |  | :  |  |  |  |  |  |
| RSK-01.2 | Identify prevention, detection and containment gaps | unverified | unscored |  | :  |  |  |  |  |  |
| RSK-01.3 | Preserve unknown likelihood and unresolved severe effects | unverified | unscored |  | :  |  |  |  |  |  |
| CAP-01.1 | Assign corrective action owner and due date | unverified | unscored |  | :  |  |  |  |  |  |
| CAP-01.2 | Link action to a specific finding | unverified | unscored |  | :  |  |  |  |  |  |
| CAP-01.3 | Require effectiveness evidence before closure | unverified | unscored |  | :  |  |  |  |  |  |
| MAP-01.1 | Map intended workflows and development stages | unverified | unscored |  | :  |  |  |  |  |  |
| MAP-01.2 | Compare the map to actual source and interfaces | unverified | unscored |  | :  |  |  |  |  |  |
| MAP-01.3 | Explain sampling, missing links and exclusions | unverified | unscored |  | :  |  |  |  |  |  |
| PRE-01.1 | Identify a harmful action before it occurs | unverified | unscored |  | :  |  |  |  |  |  |
| PRE-01.2 | Place a fail-safe admission guard at the actual boundary | unverified | unscored |  | :  |  |  |  |  |  |
| PRE-01.3 | Challenge the guard with invalid, stale or competing inputs | unverified | unscored |  | :  |  |  |  |  |  |
| PRE-02.1 | Define a stop/containment trigger | unverified | unscored |  | :  |  |  |  |  |  |
| PRE-02.2 | Preserve recoverable state and isolate affected work | unverified | unscored |  | :  |  |  |  |  |  |
| PRE-02.3 | Exercise safe stop and controlled resumption | unverified | unscored |  | :  |  |  |  |  |  |
| GAT-01.1 | Record stage entry/exit criteria | unverified | unscored |  | :  |  |  |  |  |  |
| GAT-01.2 | Identify versioned handoff inputs and outputs | unverified | unscored |  | :  |  |  |  |  |  |
| GAT-01.3 | Have the receiving owner review unresolved exceptions | unverified | unscored |  | :  |  |  |  |  |  |
| DIA-01.1 | Define expected versus observed behavior | unverified | unscored |  | :  |  |  |  |  |  |
| DIA-01.2 | Reproduce or explicitly retain reproduction as unknown | unverified | unscored |  | :  |  |  |  |  |  |
| DIA-01.3 | Separate observations from competing explanations | unverified | unscored |  | :  |  |  |  |  |  |
| DIA-02.1 | Propose a cause and a falsifying experiment | unverified | unscored |  | :  |  |  |  |  |  |
| DIA-02.2 | Compare affected and unaffected conditions | unverified | unscored |  | :  |  |  |  |  |  |
| DIA-02.3 | Confirm the cause through the actual failing path | unverified | unscored |  | :  |  |  |  |  |  |
| CAP-02.1 | Replay the original failure condition after correction | unverified | unscored |  | :  |  |  |  |  |  |
| CAP-02.2 | Exercise recurrence prevention and adjacent regressions | unverified | unscored |  | :  |  |  |  |  |  |
| CAP-02.3 | Update the durable control/test and preserve residual risk | unverified | unscored |  | :  |  |  |  |  |  |

## Stage transition review

| Gate | Transition | State | Producer / receiver | Input / output evidence | Reviewer / rationale | Blockers |
|---|---|---|---|---|---|---|
| G1 | requirements → design | blocked |  /  |  /  | :  | handoff_review_not_supported, producer_and_receiver_required, input_evidence_required, output_evidence_required, control:REQ-01, control:REQ-02, control:RSK-01, no_applicable_supported_control |
| G2 | design → implementation | blocked |  /  |  /  | :  | handoff_review_not_supported, producer_and_receiver_required, input_evidence_required, output_evidence_required, control:DES-01, control:DES-02, control:SUP-01, control:GAT-01, no_applicable_supported_control |
| G3 | implementation → verification | blocked |  /  |  /  | :  | handoff_review_not_supported, producer_and_receiver_required, input_evidence_required, output_evidence_required, control:IMP-01, control:IMP-02, control:PRE-01, control:CHG-01, no_applicable_supported_control |
| G4 | verification → release | blocked |  /  |  /  | :  | handoff_review_not_supported, producer_and_receiver_required, input_evidence_required, output_evidence_required, control:VER-01, control:VER-02, control:VER-03, control:PRE-02, control:REL-01, control:REL-02, no_applicable_supported_control |
| G5 | release → operations | blocked |  /  |  /  | :  | handoff_review_not_supported, producer_and_receiver_required, input_evidence_required, output_evidence_required, control:OPS-01, control:OPS-02, control:CAP-01, control:CAP-02, no_applicable_supported_control |

## Investigations


## Boundary reviews

| Boundary | Aspect | Status / score | Failure scenario | Evidence | Finding | Improvement | Owner / due |
|---|---|---|---|---|---|---|---|

## Risks and corrective actions

No risks recorded. This is not evidence of absence of risk.

## Graph evidence

```json
null
```

## Graph connections requiring review


## Review queue

- REQ-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- REQ-02 : unverified — Review evidence and document a corrective action for any confirmed gap.
- DES-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- DES-02 : unverified — Review evidence and document a corrective action for any confirmed gap.
- SUP-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- IMP-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- IMP-02 : unverified — Review evidence and document a corrective action for any confirmed gap.
- VER-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- VER-02 : unverified — Review evidence and document a corrective action for any confirmed gap.
- VER-03 : unverified — Review evidence and document a corrective action for any confirmed gap.
- REL-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- REL-02 : unverified — Review evidence and document a corrective action for any confirmed gap.
- OPS-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- OPS-02 : unverified — Review evidence and document a corrective action for any confirmed gap.
- CHG-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- RSK-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- CAP-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- MAP-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- PRE-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- PRE-02 : unverified — Review evidence and document a corrective action for any confirmed gap.
- GAT-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- DIA-01 : unverified — Review evidence and document a corrective action for any confirmed gap.
- DIA-02 : unverified — Review evidence and document a corrective action for any confirmed gap.
- CAP-02 : unverified — Review evidence and document a corrective action for any confirmed gap.

## Evidence register

| ID | Path | Locator | Kind | SHA-256 | Valid |
|---|---|---|---|---|---|
