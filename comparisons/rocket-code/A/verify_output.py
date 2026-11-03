from pathlib import Path
import hashlib
import json
from PIL import Image
root = Path(__file__).resolve().parent
source = root / 'draw_rocket.py'
compile(source.read_text(encoding='utf-8-sig'), str(source), 'exec')
path = root / 'rocket.png'
with Image.open(path) as image:
    image.verify()
with Image.open(path) as image:
    image.load()
    assert image.format == 'PNG'
    assert image.size == (1400, 1800)
    assert image.mode == 'RGB'
    extrema = image.getextrema()
    assert all(hi > lo for lo, hi in extrema), 'Unexpected blank image'
    print(json.dumps({'syntax': 'PASS', 'png_decode': 'PASS', 'dimensions': image.size, 'mode': image.mode, 'channel_extrema': extrema, 'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}, indent=2))
