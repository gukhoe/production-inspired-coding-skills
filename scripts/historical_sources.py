"""Read immutable study inputs after reader-facing documents were translated."""
import hashlib
import json
from pathlib import Path
import zipfile


def original_bytes(root, relative):
    root = Path(root)
    relative = Path(relative).as_posix()
    index = json.loads((root / 'sources/historical-originals.json').read_text(encoding='utf-8'))
    records = {item['path']: item for item in index['files']}
    if relative not in records:
        if relative.startswith('skills/'):
            manifest = json.loads((root/'sources/manifest.json').read_text(encoding='utf-8'))
            baseline = next((row for row in manifest['files'] if row['path'] == relative), None)
            if baseline:
                archive = root/'sources'/baseline['archive']
                expected = next(row['sha256'] for row in manifest['archives'] if row['path'] == archive.relative_to(root).as_posix())
                if hashlib.sha256(archive.read_bytes()).hexdigest() != expected:
                    raise ValueError('Original skill archive hash mismatch')
                with zipfile.ZipFile(archive) as source:
                    data = source.read(baseline['entry'])
                if hashlib.sha256(data).hexdigest() != baseline['sha256']:
                    raise ValueError('Original skill entry hash mismatch')
                return data
        return (root / relative).read_bytes()
    archive = root / index['archive']
    if hashlib.sha256(archive.read_bytes()).hexdigest() != index['sha256']:
        raise ValueError('Historical archive hash mismatch')
    with zipfile.ZipFile(archive) as source:
        data = source.read(relative)
    if hashlib.sha256(data).hexdigest() != records[relative]['sha256']:
        raise ValueError('Historical entry hash mismatch: ' + relative)
    return data
