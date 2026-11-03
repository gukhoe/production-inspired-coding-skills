# Actual A/B/C Rocket Coding Comparison

Each independent agent received the same request. Its English translation is: **“Write code that draws a rocket, run it, and save the resulting image.”** The original Korean request and common administrative instructions remain unchanged in each group's `TASK.md` and `ADMIN.md`; see the [English input translations](INPUTS_EN.md).

No group-specific style, complexity, quality level, or visual components were prescribed. Each agent wrote and executed drawing code. These images were not produced by an image-generation model.

## Rendered output

| A · No additional skill | B · Verification skill | C · Manufacturing process skills |
|---|---|---|
| ![A rocket](A/rocket.png) | ![B rocket](B/rocket.png) | ![C rocket](C/rocket.png) |
| [Code](A/draw_rocket.py) · [Checks](A/verify_output.py) · [Report](A/REPORT.md) | [Code](B/draw_rocket.py) · [Checks](B/verify_output.py) · [Report](B/REPORT.md) | [Code](C/draw_rocket.py) · [Check results](C/verification.json) · [Report](C/REPORT.md) |

All three render a recognizable rocket body, window, fins, and exhaust. A uses a dark teal background and an orange planet. B uses a paper-colored border, grain, and a lunar foreground. C uses a dark background and a curved teal planetary horizon. These are observed design choices, not established stylistic effects of the skills.

## Conditions and actual use

| Item | A | B | C |
|---|---|---|---|
| Skills provided | None | verification-before-completion | 16 manufacturing process skills and an index |
| Skills read and applied, as reported by the agents | None | verification-before-completion | standard-work only |
| Environment | Python 3.11.15 / Pillow 11.3.0 | Same | Same |
| Image dimensions | 1400×1800 | 1400×1800 | 1200×1600 |
| Renderer source lines | 146 | 153 | 150 |
| Separate verifier source lines | 18 | 22 | 0; checks are embedded in the renderer |
| Verification structure | Separate script | Separate script | Reopen the saved file, validate it, and write JSON evidence |
| Renderer exit code | 0 | 0 | 0 |
| Coordinator's independent rerun | Identical PNG hash | Identical PNG hash | Identical PNG hash |
| Image bytes | 265,518 | 762,753 | 213,648 |

Line counts include comments and blank lines. C's 150 lines include validation and JSON recording, so the counts do not fairly rank rendering code size alone. Resolution and texture also differ; image size is not an efficiency ranking.

## Differences observed in the code

**A** defines `draw_poster()` and reusable shape/font helpers, with a separate `verify_output.py`. It creates `random.Random(41)` inside the rendering function and falls back to a default font when Arial is unavailable. It performs execution, file checks, and visual inspection without an additional skill.

**B** uses `main()` and shared drawing helpers, plus a separate `verify_output.py`. It uses seed 47 and 175,000 pixel-grain operations. Its recorded execution, PNG checks, and visual inspection are consistent with the verification skill, but the observed evidence does not establish substantially stronger validation than A in this task. Arial is required without a fallback.

**C** uses local drawing helpers inside `main()`. After rendering, it reopens the saved PNG and checks dimensions, mode, format, and channel range. It writes `verification.json` containing SHA-256, file size, and a timestamp. It specifies a Windows Segoe UI path, so font handling elsewhere requires further verification. This structure was observed; the skill did not mandate that exact implementation.

All three render at twice the final resolution and downsample. All three check the serialized output, regardless of whether checks are separate or embedded. Successful execution and PNG decoding do not automatically prove that an image depicts a rocket; the coordinator opened all three images to inspect that requirement.

## What this comparison supports

- All three conditions fulfilled the request to write code, execute it, and save a rocket drawing.
- Code structure and visual design differ, but no progression from careless A to accurate B to perfect C was observed.
- C selected only `standard-work`, consistent with the original guidance to load relevant skills selectively. This task does not establish the effects of PFMEA, Poka-Yoke, MSA, or the entire collection.
- All three conditions were capable of this simple generation task. One observation per group cannot separate skill effects from generation variability.
- The improvement target is effective risk handling, verification, and change control when needed, rather than requiring C to produce more documentation.

## Reproduction and checks

Run `python draw_rocket.py` in a group's directory to regenerate its `rocket.png`. A/B provide `python verify_output.py`; C checks its output during rendering. The observed Pillow version is recorded in [requirements.txt](requirements.txt). Different font environments may change the rendered image.

To recheck in temporary copies without overwriting submissions, run from the repository root:

```sh
python -X utf8 scripts/recheck_rocket.py
```

The script executes each renderer and any supplied standalone verifier, decodes the PNG, and compares its hash with the submission. See the [results](verification/results.json) and complete rerun logs for [A](verification/A.log), [B](verification/B.log), and [C](verification/C.log).

## Experiment records and limitations

- Inputs were prepared before generation: [protocol.json](protocol.json) and each group's identical TASK.md/ADMIN.md. Their matching SHA-256 values were verified.
- Fresh agent task names: `/root/rocket_a`, `/root/rocket_b`, `/root/rocket_c`. All used `fork_turns=none`, without model or reasoning overrides.
- Work date: November 2, 2026, America/Chicago. UTC logs are dated November 3, 2026.
- All agents reported no drawing-code failure or revision. All encountered the F: drive launcher issue and used the same permitted host-execution fallback.
- Conversation contexts and working directories were separated, but shared-filesystem read isolation was not enforced by the OS. Full tool transcripts are not preserved here; skill-read accounts come from agent reports.
- A still received platform instructions and the common recordkeeping requirements. It is a condition without an additional task skill, not a model without instructions.
- Recorded start times exclude earlier instruction reads and launcher failures. Shared resources also affect concurrent execution, so no development-time ranking is reported.
- Exact internal model revision, token usage, and cost were unavailable. This is one descriptive pilot per group, not a controlled study with a preregistered numerical score.
- English agent reports are translations of preserved [original Korean reports](../../evidence/rocket-code-original-reports/). Frozen prompts and raw logs were not translated in place.
