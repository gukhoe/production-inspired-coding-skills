"""Generate/check independently installable v2 skill instructions and blank forms."""
import argparse
import json
from pathlib import Path
from skill_catalog import CATALOG

ROOT = Path(__file__).resolve().parents[1]


def outputs():
    for name, (description, steps, fields, targets) in CATALOG.items():
        body = f'---\nname: {name}\ndescription: {description}\nmetadata:\n  version: "2.0"\n---\n# {name.replace("-", " ").title()}\n\n'
        body += '\n'.join(f'{i}. {step}' for i, step in enumerate(steps, 1))
        body += '\n\n## Output and evidence\n\nUse [the blank output form](assets/output-template.md) for this workflow and [the portable record](assets/review-record.json) when transferring it to the auditor. Fill only observed facts; link raw evidence rather than copying logs into the conversation. A completed form is a document, not execution evidence or an automatic supported score.\n'
        form = f'# {name}: review form\n\n- Source revision:\n- Scope and exclusions:\n- Author / reviewer / relationship:\n- Check status: PASS (executed and met expectation), FAIL (executed and violated expectation), BLOCKED (required action prevented), UNVERIFIED (not established).\n\n| Field | Observation / decision | Evidence path and locator | Open action / owner |\n|---|---|---|---|\n'
        form += ''.join(f'| {field} | | | |\n' for field in fields)
        record = {'schema': 'software-skill-record/1', 'skill': name, 'skill_version': '2.0', 'revision': '', 'author': '', 'reviewer': '', 'status': 'UNVERIFIED', 'criterion_targets': targets, 'observations': {field: '' for field in fields}, 'evidence': [], 'open_actions': []}
        yield f'skills/{name}/SKILL.md', body
        yield f'skills/{name}/assets/output-template.md', form
        yield f'skills/{name}/assets/review-record.json', json.dumps(record, indent=2)+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    different = []
    for relative, content in outputs():
        path = ROOT/relative
        if args.check:
            if not path.is_file() or path.read_text(encoding='utf-8') != content:
                different.append(relative)
        else:
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text(content, encoding='utf-8')
    if different:
        raise SystemExit('Generated skill drift: '+', '.join(different))
    print('16 independently installable skills and 32 blank forms checked.' if args.check else 'Generated skill v2 instructions and blank forms.')


if __name__ == '__main__':
    main()
