# Software Assurance Auditor 0.2.0: release validation

Validation date: November 3, 2026. Initial public source release; manifest schema 2, standard 0.2.0, report template 1.0. CLI requires Python 3.11+; MCP extra pins SDK 2.3.0.

## Executed checks

| Check | Observed result |
|---|---|
| `python -m unittest discover -s tests -v` in the installed MCP environment | 47 tests discovered: 46 passed, one skipped because Windows symlink creation was unavailable |
| Actual stdio MCP connection to the installed package | Eight tools listed and exercised; questionnaire, English narrative policy, 72-row report, path bounds and invalid-input responses checked |
| Package build and installation | Wheel built and installed successfully; MCP integration used installed code |
| Standalone synthetic duplicate-event example | Deliberate target exit 1 reproduced; audit outcome `needs_attention`, with gap/unknowns preserved |
| Original study evidence recheck | PASS: hashes, 90-row consistency, benchmark reproduction and sample tests |
| Rocket reproduction | PASS: all three renderers reproduced original image hashes; original input hashes verified from archived bytes |
| English documentation and examples | Public Markdown/HTML/text reading editions checked for remaining Korean text; fixed output and example narrative are English |
| Privacy scope | Private project reports and source evidence under `.process-audit/` excluded from the public commit |

The language scan is a publication check, not a general natural-language detector. Raw historical archives and structured research evidence preserve their original bytes and language. See [language/provenance policy](LANGUAGE_AND_PROVENANCE.md).

## Limits

The suite verifies tool behavior against fixtures; it does not establish the reliability of an arbitrary audited system. The populated example is synthetic. Hashes establish file identity, not the semantic adequacy or authenticity of logs. Scores describe assessed evidence maturity; coverage is not execution coverage, and neither metric authorizes a release. Real hosted AI-client configuration was not changed; the tested connection was an actual standalone stdio client/server exchange.

Install `.[mcp]` before running the suite to include real MCP tests. Environments without that dependency skip integration testing. Symlink escape checks exist but the symlink test needs OS permissions. Preserve skipped-test reasons when reproducing validation.
