# English publication and evidence provenance

Public documentation, installation instructions, questionnaires, report templates and example reports use English. MCP instructions, the criteria catalog and the optional audit skill direct AI reviewers to write scope, rationale, findings, improvements and summaries in English. The deterministic report renderer does not call a translation service: it preserves supplied assessment text. Translate narrative before evaluation when using an existing non-English manifest; never alter source evidence to make it English.

Evidence identifiers, file paths, hashes and verbatim quotations retain their exact form. Explain non-English quotations in English. This permits an English audit of a project whose source documents use another language without falsifying evidence.

## Historical records

Earlier commits included Korean review documents and frozen experiment inputs. Reader-facing editions are now English. Original bytes are preserved in `sources/historical-originals.zip`; `sources/historical-originals.json` records archive/member SHA-256 values and original paths. The original attachments remain unchanged. Structured historical JSON/CSV, participant code and original archives are research data rather than current product documentation; their language and bytes are retained.

The original `sources/manifest.json`, study freeze records and rocket protocol still identify historical inputs. `scripts/historical_sources.py` resolves an archived path before a current reading edition and verifies both archive and member hashes. Evidence/rocket recheck scripts therefore test the actual historical bytes, not a later translation. English editorial editions identify themselves and do not claim to have been frozen before the original experiment. The 16 original skill files are unchanged.

Private project reviews and evidence under `.process-audit/` are excluded from publication. The public populated example is a synthetic program with an intentional duplicate-event defect, not a private project report or a production-readiness claim.
