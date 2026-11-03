from pathlib import Path
import ast
import hashlib
from PIL import Image, ImageStat
root = Path(__file__).resolve().parent
source = root / 'draw_rocket.py'
ast.parse(source.read_text(encoding='utf-8-sig'))
print('PASS: Python source parses successfully')
file = root / 'rocket.png'
with Image.open(file) as image:
    assert image.format == 'PNG', image.format
    image.verify()
print('PASS: PNG integrity verification')
with Image.open(file) as image:
    image.load()
    assert image.size == (1400, 1800), image.size
    assert image.mode == 'RGB', image.mode
    extrema = image.getextrema()
    assert all(high - low > 100 for low, high in extrema), extrema
    print(f'PASS: image dimensions={image.size}, mode={image.mode}, extrema={extrema}')
print('SHA256:', hashlib.sha256(file.read_bytes()).hexdigest())
print('FAILURES: 0')
