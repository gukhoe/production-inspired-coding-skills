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
        return (root / relative).read_bytes()
    archive = root / index['archive']
    if hashlib.sha256(archive.read_bytes()).hexdigest() != index['sha256']:
        raise ValueError('Historical archive hash mismatch')
    with zipfile.ZipFile(archive) as source:
        data = source.read(relative)
    if hashlib.sha256(data).hexdigest() != records[relative]['sha256']:
        raise ValueError('Historical entry hash mismatch: ' + relative)
    return data
