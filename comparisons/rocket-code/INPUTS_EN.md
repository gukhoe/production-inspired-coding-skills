# English Translation of the Frozen Experiment Inputs

These translations are provided for readers. The agents actually received the original Korean `TASK.md` and `ADMIN.md` files in their respective directories. Those files and the recorded protocol remain unchanged so their hashes and experimental provenance remain valid.

## Common task

> Write code that draws a rocket, run it, and save the resulting image.

## Common administrative instructions

This comparison performs the same task under different skill conditions.

Do not read project code outside your working directory, other groups' results, evaluation material, or existing rocket images. Draw directly with code without network reference material or image-generation tools. Use installed runtimes; do not change system settings or global packages.

No visual style, components, or complexity level is specified. When relevant, selectively use only the skills provided in this directory. If no skills are provided, proceed without additional skills. Do not create other agents.

In `REPORT.md`, briefly record the skills actually used, start and completion UTC timestamps, commands executed, exit codes, checks, failures, revisions, and artifact paths. Preserve raw execution output in `logs/` where possible. Do not record unexecuted checks as passing. The maximum working time is eight minutes.

If the default command launcher fails to start because of an F: drive I/O error, the same command may be run in host PowerShell using `require_escalated`.

## Treatment mapping

- A: no additional skill files.
- B: the original study's `verification-before-completion` snapshot.
- C: the 16 original manufacturing process coding skills and their index, with selective loading.

Only the skill treatment and working-directory path differed. See [protocol.json](protocol.json) and the [input hash checks](verification/results.json) for the original records.
