"""Draw a deterministic rocket launch poster using only the installed Pillow package.
Run: python draw_rocket.py
Outputs are always written beside this script.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
W, H, S = 1200, 1600, 2
NAVY = (8, 20, 43)
rng = random.Random(42)

def font(size, bold=False):
    path = Path('C:/Windows/Fonts') / ('segoeuib.ttf' if bold else 'segoeui.ttf')
    return ImageFont.truetype(str(path), size*S)

def bezier(points, n=60):
    a,b,c,d = points
    return [((1-t)**3*a[0]+3*(1-t)**2*t*b[0]+3*(1-t)*t*t*c[0]+t**3*d[0],
             (1-t)**3*a[1]+3*(1-t)**2*t*b[1]+3*(1-t)*t*t*c[1]+t**3*d[1])
            for t in (i/n for i in range(n+1))]

def main():
    print('UTC start:', datetime.now(timezone.utc).isoformat())
    im = Image.new('RGB', (W*S,H*S))
    d = ImageDraw.Draw(im)
    for y in range(H*S):
        t=y/(H*S)
        d.line((0,y,W*S,y), fill=(int(8+9*t),int(20+21*t),int(43+27*t)))
    def line(xy, fill, width=1):
        d.line([(x*S,y*S) for x,y in xy], fill=fill,width=width*S)
    def ellipse(box,fill=None,outline=None,width=1):
        d.ellipse(tuple(int(v*S) for v in box),fill=fill,outline=outline,width=width*S)
    def text(x,y,s,size,fill,bold=False):
        d.text((x*S,y*S),s,font=font(size,bold),fill=fill)

    # Quiet starfield; seed is fixed so the image is reproducible.
    for _ in range(175):
        x,y = rng.randrange(65,W-65),rng.randrange(280,1350)
        r = rng.choice([0.7,1.0,1.2,1.8])
        c = rng.choice([(75,116,145),(126,164,184),(190,209,215)])
        ellipse((x-r,y-r,x+r,y+r),c)
    for x,y in [(157,650),(1050,514),(917,1060),(291,972)]:
        line([(x-7,y),(x+7,y)],(168,203,216))
        line([(x,y-7),(x,y+7)],(168,203,216))
    # Wide orbital arcs form a quiet graphic frame around the subject.
    d.arc((160*S,330*S,1240*S,1410*S),185,303,fill=(38,73,99),width=2*S)
    d.arc((-170*S,215*S,1110*S,1495*S),280,353,fill=(38,73,99),width=2*S)
    ellipse((145,365,265,485),(179,195,194))
    ellipse((175,380,257,475),(151,176,180))
    ellipse((166,402,190,426),(137,165,170))
    ellipse((218,439,237,458),(129,158,165))

    # Curved planetary horizon, clipped naturally by the bottom of the canvas.
    ellipse((-290,1275,1490,2425),(27,99,124),outline=(86,180,192),width=6)
    ellipse((-280,1300,1480,2425),(19,65,91))
    d.arc((-240*S,1330*S,1420*S,2380*S),188,340,fill=(31,93,115),width=20*S)
    # Sparse latitude-like bands stay below the main subject.
    d.arc((-160*S,1390*S,1360*S,2320*S),185,350,fill=(38,103,120),width=3*S)

    # Draw the rocket as a single transparent assembly, then rotate it.
    rocket = Image.new('RGBA',(600*S,1100*S))
    q = ImageDraw.Draw(rocket)
    def poly(pts,fill): q.polygon([(round(x*S),round(y*S)) for x,y in pts],fill=fill)
    def oval(box,fill,outline=None,width=1):
        q.ellipse(tuple(round(v*S) for v in box),fill=fill,outline=outline,width=width*S)
    def path(curves,fill):
        pts=[]
        for curve in curves: pts.extend(bezier(curve))
        poly(pts,fill)
    # Exhaust: three nested tapered shapes.
    path([[(246,681),(218,775),(258,937),(300,1055)],
          [(300,1055),(339,929),(385,782),(354,681)]], '#f27743')
    path([[(263,684),(251,797),(285,907),(300,976)],
          [(300,976),(323,900),(348,789),(337,684)]], '#ffc56e')
    path([[(279,686),(275,746),(290,825),(300,875)],
          [(300,875),(315,817),(328,743),(321,686)]], '#fff3c1')
    # Side fins, each outlined by a contrasting edge.
    path([[(230,452),(182,489),(139,567),(128,671)],
          [(128,671),(175,643),(208,619),(243,610)]], '#ed795d')
    path([[(370,452),(418,489),(461,567),(472,671)],
          [(472,671),(425,643),(392,619),(357,610)]], '#b54c47')
    poly([(144,640),(211,589),(225,501),(193,548)], '#ff9a70')
    # Nozzle and hull.
    poly([(245,621),(355,621),(367,687),(233,687)], '#273f54')
    poly([(250,636),(350,636),(353,657),(247,657)], '#71949b')
    path([[(300,105),(225,181),(205,300),(216,458)],
          [(216,458),(220,532),(229,590),(246,631)],
          [(246,631),(276,643),(324,643),(354,631)],
          [(354,631),(371,590),(380,532),(384,458)],
          [(384,458),(395,300),(375,181),(300,105)]], '#e4ede6')
    path([[(300,105),(343,218),(350,408),(327,638)],
          [(327,638),(337,637),(347,634),(354,631)],
          [(354,631),(371,590),(380,532),(384,458)],
          [(384,458),(395,300),(375,181),(300,105)]], '#a8c2be')
    # Coral nose and lower stripe.
    path([[(300,105),(267,139),(244,184),(231,235)],
          [(231,235),(268,248),(332,248),(369,235)],
          [(369,235),(356,184),(333,139),(300,105)]], '#f17b60')
    path([[(300,105),(330,146),(345,193),(349,240)],
          [(349,240),(356,239),(363,237),(369,235)],
          [(369,235),(356,184),(333,139),(300,105)]], '#c65c50')
    poly([(224,537),(376,537),(370,570),(230,570)], '#e67359')
    oval((243,287,357,401),'#496d79')
    oval((251,295,349,393),'#f6f0d8')
    oval((261,305,339,383),'#153b57')
    oval((266,310,330,374),'#236c87')
    q.arc((269*S,315*S,327*S,372*S),190,280,fill='#bce6df',width=5*S)
    oval((314,354,323,363),'#75b5c0')
    # Small hull detail and center fin.
    for y in [438,450,462]: q.line((277*S,y*S,323*S,y*S),fill='#759b9d',width=3*S)
    path([[(300,544),(283,575),(285,654),(300,700)],
          [(300,700),(315,654),(317,575),(300,544)]], '#c95c4c')
    q.line((300*S,560*S,300*S,672*S),fill='#ff9f75',width=3*S)
    rocket=rocket.rotate(-25,resample=Image.Resampling.BICUBIC,expand=True)
    im.paste(rocket,(int(655*S-rocket.width/2),int(765*S-rocket.height/2)),rocket)
    d=ImageDraw.Draw(im)
    text(76,65,'FIELD NOTES   /   SPACE SERIES',18,(130,174,190),True)
    text(72,102,'BEYOND',100,(239,236,219),True)
    text(78,225,'A little curiosity. An infinite sky.',24,(159,191,201))
    line([(80,306),(260,306)],(226,122,92),3)
    text(82,1120,'01',58,(239,236,219),True)
    text(84,1201,'THE ASCENT',18,(159,191,201),True)
    line([(80,1500),(1120,1500)],(78,139,156),1)
    text(80,1520,'EXPLORE FURTHER',17,(177,211,216),True)
    text(930,1520,'EST. 2026',17,(177,211,216))
    output=ROOT/'rocket.png'
    im.resize((W,H),Image.Resampling.LANCZOS).save(output)
    # Validate the actual serialized artifact, not just the in-memory drawing.
    with Image.open(output) as check:
        check.load()
        assert check.size == (W,H),check.size
        assert check.mode == 'RGB',check.mode
        assert check.format == 'PNG',check.format
        extrema=check.getextrema()
        assert all(hi-lo > 100 for lo,hi in extrema),extrema
    result={'output':str(output),'size':[W,H],'format':'PNG','mode':'RGB',
            'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'bytes':output.stat().st_size,'checks':'PASS: reopen, size, mode, format, channel range',
            'utc_complete':datetime.now(timezone.utc).isoformat()}
    (ROOT/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
