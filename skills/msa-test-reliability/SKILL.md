---
name: msa-test-reliability
description: Use for flaky tests, conflicting AI reviews, weak oracles or suspected false passes; measure the inspection system before trusting its verdict.
metadata:
  version: "2.0"
---
# Msa Test Reliability

1. Start with labeled good/bad cases and a passing control. Perturb one condition; require the corresponding assertion to fail for the intended reason.
2. Use mutation tests and known-bad sentinels to measure detection bias. Separate product failure, environment failure and equivalent/surviving mutants; never majority-vote away a real failure.
3. For AI reviewers, record model/version/prompt and blinded labeled decisions. Report confusion matrix, false-pass/false-fail rates and Cohen kappa where defined; keep one-class/degenerate kappa unavailable.
4. Complete when results identify what the oracle can discriminate. Unrun paired model trials remain UNVERIFIED; test counts and instruction quality do not prove improved coding outcomes.

## Output and evidence

Use [the blank output form](assets/output-template.md) for this workflow and [the portable record](assets/review-record.json) when transferring it to the auditor. Fill only observed facts; link raw evidence rather than copying logs into the conversation. A completed form is a document, not execution evidence or an automatic supported score.
