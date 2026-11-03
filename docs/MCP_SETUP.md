# Download, install and connect

The coding skills and independent auditor can each be used alone. Install this initial release from the GitHub source checkout. No PyPI release is assumed.

## A. Coding skills only

Download the repository ZIP or clone it. Select any of the original 16 skill folders under skills/ and add the complete selected folder to your AI client's supported skill location. See [the catalog](../skills/README.md). No auditor or MCP server is required.

## B. Independent auditor through MCP

Download a reviewed revision from [GitHub](https://github.com/gukhoe/production-inspired-coding-skills). Pin a reviewed commit/tag for automated installation.

Windows PowerShell:

```powershell
git clone https://github.com/gukhoe/production-inspired-coding-skills.git
cd production-inspired-coding-skills
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".[mcp]"
.\.venv\Scripts\software-audit.exe criteria
```

macOS/Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install '.[mcp]'
.venv/bin/software-audit criteria
```

Add a **stdio** MCP server in your AI client's settings. The settings-file wrapper varies by client; use these command/argument values with real absolute paths:

```json
{
  "command": "C:/tools/production-inspired-coding-skills/.venv/Scripts/software-audit-mcp.exe",
  "args": ["--repo-root", "D:/projects/project-to-audit"]
}
```

On macOS/Linux use /absolute/path/.venv/bin/software-audit-mcp. The client starts the process over stdin/stdout. The audit server needs no network listener, API key, Graphify, model-provider account or coding-skill installation. Your AI host still needs its own model access.

The configured root bounds file access; restart/reconfigure for another project. The service reads files and returns records. It does not modify projects, execute tests, install software or deploy. Outputs can contain source excerpts, so use a host appropriate for the project data.

## Tools

| Tool | Result |
|---|---|
| audit_criteria | All questions, 72 checkpoint IDs, rubric and workflow rules |
| audit_initialize | Empty standalone review |
| audit_inventory | Bounded candidate inventory with explicit exclusions |
| audit_read_file | Bounded UTF-8 excerpt, line numbers and hash |
| audit_evidence | File identity and evidence skeleton |
| audit_investigation | Preventive/corrective investigation steps |
| audit_evaluate | Scored JSON, fixed Markdown report and next actions |
| audit_graph_candidates | Optional Graphify export relationships |

Ask the AI to use the server's criteria, inspect the actual project, preserve unknowns and return the generated standard report. Read scores and coverage together. Authorized tests run through the host's execution tools, with their logs supplied as evidence.

The built-in MCP instructions and questionnaire specify English assessment narrative and reports. Evidence may be in any language; its paths, hashes and exact quotations remain unchanged. The report engine preserves supplied narrative, so an existing non-English manifest must be translated by the reviewing AI before evaluation.

## C. CLI only

Install . instead of .[mcp], then run software-audit. Or run python skills/software-process-audit/scripts/audit.py directly from the downloaded source tree. MCP can be added later without installing skills.

## Reproducibility

Package/standard 0.2.0; manifest schema 2; report template 1.0; MCP SDK 2.3.0. The [official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) implements the protocol. Validation uses an installed package and real stdio handshake. Installation does not change global AI-client configuration.
