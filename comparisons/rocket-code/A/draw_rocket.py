"""Draw a reproducible rocket poster using only Python and Pillow.
Run: python draw_rocket.py. Output is always beside this script.
"""
from pathlib import Path
import math
import random
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H, S = 1400, 1800, 2
NAVY = '#102e41'
CREAM = '#f6e7c7'
RED = '#e35f42'
TEAL = '#62afb0'


def canvas(size, color):
    return Image.new('RGBA', (size[0] * S, size[1] * S), color)


def poly(draw, points, fill):
    draw.polygon([(round(x*S), round(y*S)) for x, y in points], fill=fill)


def ellipse(draw, box, fill, outline=None, width=1):
    draw.ellipse(tuple(round(v*S) for v in box), fill=fill, outline=outline, width=width*S)


def line(draw, points, fill, width=1):
    draw.line([(round(x*S), round(y*S)) for x,y in points], fill=fill, width=width*S)


def curve(start, segments):
    """Sample cubic Bezier segments, producing a reusable polygon contour."""
    points = [start]
    x0, y0 = start
    for (x1,y1), (x2,y2), (x3,y3) in segments:
        for i in range(1, 49):
            t = i/48
            u = 1-t
            points.append((u**3*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t**3*x3,
                           u**3*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t**3*y3))
        x0,y0=x3,y3
    return points


def font(size, bold=False):
    try:
        return ImageFont.truetype('arialbd.ttf' if bold else 'arial.ttf', size*S)
    except OSError:
        return ImageFont.load_default(size=size*S)


def text(draw, pos, content, size, fill=CREAM, bold=False):
    draw.text((pos[0]*S, pos[1]*S), content, font=font(size,bold), fill=fill)


def draw_poster():
    im = canvas((W,H), NAVY)
    d = ImageDraw.Draw(im)
    # A restrained orbital grid, all geometry generated locally.
    for box in [(220,280,1600,1660), (290,350,1530,1590)]:
        d.arc(tuple(v*S for v in box), 174, 320, fill='#25485a', width=2*S)
    line(d, [(90,142),(1310,142)], '#60808a', 1)
    text(d, (90,87), 'ORBITAL EXPLORATION PROGRAM', 23)
    text(d, (1166,87), 'NO. 01', 23)
    text(d, (85,191), 'ONWARD', 128, bold=True)
    text(d, (92,350), 'A SMALL SHIP.  AN INFINITE HORIZON.', 24, TEAL)

    rng = random.Random(41)
    for _ in range(110):
        x, y = rng.uniform(80,1320), rng.uniform(445,1600)
        r = rng.choice([1.2,1.5,2,2.8])
        ellipse(d, (x-r,y-r,x+r,y+r), rng.choice(['#7f9ba4','#b6c7c4','#e6dec3']))
    for x,y in [(220,580),(1120,535),(1135,1210),(360,980),(820,470)]:
        line(d, [(x-10,y),(x+10,y)], CREAM, 2)
        line(d, [(x,y-10),(x,y+10)], CREAM, 2)
        ellipse(d,(x-3,y-3,x+3,y+3),CREAM)

    # The distant moon has hand-placed crater geometry.
    ellipse(d, (1000,650,1190,840), '#7bb4b1')
    ellipse(d, (1023,671,1181,828), '#8fc3bc')
    for x,y,r in [(1050,712,15),(1144,746,23),(1087,795,11)]:
        ellipse(d,(x-r,y-r,x+r,y+r),'#71aaa9')
        d.arc(tuple(int(v*S) for v in (x-r,y-r,x+r,y+r)),30,160,fill='#acd2c5',width=2*S)

    # A cropped ochre planet anchors the launch scene.
    ellipse(d, (600,1270,1630,2300), '#c66c42')
    planet_mask = Image.new('L',im.size,0)
    md = ImageDraw.Draw(planet_mask)
    ellipse(md,(600,1270,1630,2300),255)
    terrain=canvas((W,H),(0,0,0,0)); td=ImageDraw.Draw(terrain)
    for k in range(13):
        y=1320+k*51
        pts=[(x,y+32*math.sin(x/130+k*.65)) for x in range(540,1700,5)]
        line(td,pts, '#d8844c' if k%2 else '#e39b60', 11 if k%3 else 24)
    im.alpha_composite(Image.composite(terrain,canvas((W,H),(0,0,0,0)),planet_mask))

    # Draw in rocket-local coordinates, then rotate the entire craft and exhaust.
    ship=canvas((600,1250),(0,0,0,0)); sd=ImageDraw.Draw(ship)
    flame=curve((251,694), [((210,800),(267,1030),(300,1190)),((330,1040),(401,836),(349,694))])
    poly(sd,flame,'#e57245')
    poly(sd,curve((269,699), [((242,813),(287,971),(300,1053)),((327,931),(365,794),(331,699))]),'#ffc773')
    poly(sd,curve((285,703), [((274,777),(292,858),(301,907)),((319,830),(335,757),(315,703))]),'#fff0b3')
    # Swept fins behind the airframe.
    poly(sd,curve((246,467), [((185,513),(161,618),(162,716)),((185,705),(224,675),(252,627))]),RED)
    poly(sd,[(181,679),(205,573),(241,526),(233,633)],'#f88a5d')
    poly(sd,curve((354,467), [((415,513),(439,618),(438,716)),((415,705),(376,675),(348,627))]),'#ba493a')
    # Engine bell and elongated ivory pressure vessel.
    poly(sd,[(263,655),(337,655),(352,715),(248,715)],'#6e8f98')
    poly(sd,[(271,665),(329,665),(337,704),(263,704)],'#28495b')
    body=curve((300,93), [((226,170),(209,305),(224,520)),((226,585),(245,645),(257,672)),((278,681),(322,681),(343,672)),((365,630),(379,574),(378,520)),((391,306),(374,172),(300,93))])
    poly(sd,body,CREAM)
    poly(sd,curve((300,93), [((340,243),(342,507),(315,676)),((329,677),(337,674),(343,672)),((365,630),(379,574),(378,520)),((391,306),(374,172),(300,93))]),'#cbd4c7')
    poly(sd,curve((300,93), [((266,128),(246,180),(234,239)),((275,251),(327,251),(367,239)),((354,180),(334,127),(300,93))]),RED)
    poly(sd,curve((300,93), [((318,134),(332,192),(335,246)),((347,244),(357,242),(367,239)),((354,180),(334,127),(300,93))]),'#be4b3c')
    # Window rim, glass, highlight, and fasteners.
    ellipse(sd,(246,305,354,413),'#345568')
    ellipse(sd,(255,314,345,404),'#e1ad6b')
    ellipse(sd,(264,323,336,395),'#22516a')
    ellipse(sd,(270,327,330,387),'#428698')
    poly(sd,curve((274,353), [((278,333),(298,330),(315,337)),((300,339),(286,348),(280,370)),((275,369),(272,361),(274,353))]),'#b7ded3')
    for a in range(0,360,60):
        x=300+49*math.cos(math.radians(a));y=359+49*math.sin(math.radians(a))
        ellipse(sd,(x-2,y-2,x+2,y+2),CREAM)
    line(sd,[(230,543),(372,543)],'#829c9a',2)
    line(sd,[(245,618),(357,618)],RED,12)
    poly(sd,[(294,552),(306,552),(313,685),(300,720),(287,685)],RED)
    text(sd,(270,456),'01',37,'#345568',True)
    rotated=ship.rotate(-26, resample=Image.Resampling.BICUBIC,expand=True)
    im.alpha_composite(rotated,(int(238*S),int(376*S)))

    # Bottom caption sits in a solid band for dependable readability.
    d=ImageDraw.Draw(im)
    d.rectangle((0,1630*S,W*S,H*S), fill=NAVY)
    line(d,[(90,1640),(1310,1640)],'#60808a',1)
    text(d,(90,1671),'BEYOND THE FAMILIAR',33,bold=True)
    text(d,(92,1722),'DEEP SPACE  /  FIRST FLIGHT',20,TEAL)
    text(d,(1130,1693),'EST. 2026',20)
    im.convert('RGB').resize((W,H),Image.Resampling.LANCZOS).save(ROOT/'rocket.png')
    print(f'SAVED: {ROOT / "rocket.png"}')
    print(f'CANVAS: {W} x {H}; supersampling: {S}x; seed: 41')


if __name__ == '__main__':
    draw_poster()
