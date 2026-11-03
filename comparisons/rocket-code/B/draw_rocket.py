"""Draw an original rocket poster with Pillow. Run: python draw_rocket.py"""
from pathlib import Path
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
W, H, S = 1400, 1800, 2
random.seed(47)
PAPER = '#f3e8cf'
NAVY = '#142f3e'
CORAL = '#e86c49'
GOLD = '#f6bf62'


def font(size, bold=False):
    name = 'arialbd.ttf' if bold else 'arial.ttf'
    return ImageFont.truetype(name, size * S)


def path(points, steps=35):
    """Sample a path: initial point followed by line or cubic tuples."""
    out = [points[0]]
    for segment in points[1:]:
        p0 = out[-1]
        if len(segment) == 2:
            out.append(segment)
        else:
            x1, y1, x2, y2, x3, y3 = segment
            for j in range(1, steps + 1):
                t = j / steps
                u = 1 - t
                out.append((u**3*p0[0]+3*u*u*t*x1+3*u*t*t*x2+t**3*x3,
                            u**3*p0[1]+3*u*u*t*y1+3*u*t*t*y2+t**3*y3))
    return out


def poly(d, points, fill, outline=None, width=3):
    coords = [(round(x*S), round(y*S)) for x,y in points]
    d.polygon(coords, fill=fill)
    if outline:
        d.line(coords+[coords[0]], fill=outline, width=width*S, joint='curve')


def ellipse(d, box, fill=None, outline=None, width=1):
    d.ellipse(tuple(round(v*S) for v in box), fill=fill, outline=outline, width=width*S)


def line(d, pts, fill, width=1):
    d.line([(int(x*S),int(y*S)) for x,y in pts], fill=fill, width=width*S)


def text(d, xy, value, size, fill, bold=False):
    d.text((xy[0]*S,xy[1]*S), value, font=font(size,bold), fill=fill)


def main():
    im = Image.new('RGB',(W*S,H*S),PAPER)
    d = ImageDraw.Draw(im)
    # A solid ink field, with subtle atmospheric gradation.
    for y in range(210,1630):
        t = (y-210)/1420
        color = tuple(round(a+(b-a)*t) for a,b in zip((20,47,62),(43,84,92)))
        d.line((60*S,y*S,1340*S,y*S), fill=color, width=S)
    text(d,(64,48),'ORBIT',105,NAVY,True)
    text(d,(1028,79),'NO. 001',38,NAVY,True)
    text(d,(69,167),'A SMALL STEP INTO THE UNKNOWN',17,NAVY)
    line(d,[(990,152),(1338,152)],NAVY,2)
    # Orbital arcs and a quiet distant planet.
    d.arc((160*S,310*S,1550*S,1720*S),195,335,fill='#51777d',width=2*S)
    d.arc((-400*S,250*S,1510*S,2060*S),208,337,fill='#436970',width=S)
    ellipse(d,(215,345,1015,1145),'#36636b')
    ellipse(d,(235,365,995,1125),outline='#608488',width=1)
    # Stars are deterministic so repeated runs produce identical artwork.
    for _ in range(135):
        x,y = random.randint(90,1310),random.randint(245,1515)
        r = random.choice([1,1,1,2,2,3])
        ellipse(d,(x-r,y-r,x+r,y+r),random.choice(['#c3c9b7','#a7b8ad','#7f9b99']))
    for x,y,r in [(178,447,13),(1160,364,12),(1170,1040,16),(276,1070,10),(1000,1290,8)]:
        poly(d,[(x,y-r),(x+3,y-3),(x+r,y),(x+3,y+3),(x,y+r),(x-3,y+3),(x-r,y),(x-3,y-3)],PAPER)
    ellipse(d,(1107,548,1175,616),GOLD)
    ellipse(d,(1125,543,1183,600),'#204552')
    # Build the vehicle upright, then rotate the whole illustration as one object.
    ship=Image.new('RGBA',(700*S,1250*S),(0,0,0,0))
    q=ImageDraw.Draw(ship)
    # Exhaust silhouette, nested flames and engine skirt.
    poly(q,path([(287,745),(230,920,285,1110,350,1210),(375,1100,475,920,413,745)]),CORAL)
    poly(q,path([(303,750),(270,885,325,1035,350,1120),(370,1000,430,875,397,750)]),GOLD)
    poly(q,path([(327,750),(315,830,325,930,350,995),(375,900,385,820,373,750)]),'#fff3ce')
    poly(q,[(283,690),(417,690),(428,755),(272,755)],'#1d3440',PAPER,4)
    poly(q,[(286,706),(414,706),(419,725),(281,725)],'#6a8990')
    # Swept side fins.
    poly(q,path([(270,445),(179,535,155,630,165,743),(213,702,247,677,286,665)]),CORAL,NAVY,5)
    poly(q,path([(430,445),(521,535,545,630,535,743),(487,702,453,677,414,665)]),CORAL,NAVY,5)
    poly(q,[(179,712),(211,592),(264,517),(250,664)],'#b54736')
    poly(q,[(447,510),(496,598),(520,711),(453,665)],'#f89768')
    # Ivory fuselage with a warm shadow along the right edge.
    body=path([(350,120),(243,235,230,425,270,690),(308,711,392,711,430,690),(470,425,457,235,350,120)])
    poly(q,body,PAPER,NAVY,5)
    poly(q,path([(350,120),(416,270,412,495,387,698),(402,699,416,695,430,690),(470,425,457,235,350,120)]),'#d3d0b7')
    # Red nose cap and seam.
    poly(q,path([(350,120),(307,167,281,225,268,279),(318,299,382,299,432,279),(419,225,393,167,350,120)]),CORAL,NAVY,4)
    poly(q,path([(350,137),(373,174,389,224,397,289),(409,287,421,284,432,279),(414,220,390,169,350,137)]),'#c9573f')
    line(q,[(284,648),(416,648)],'#8c9b96',3)
    line(q,[(280,667),(420,667)],'#8c9b96',2)
    # Porthole ring, glass and specular reflection.
    ellipse(q,(283,342,417,476),NAVY)
    ellipse(q,(291,350,409,468),GOLD)
    ellipse(q,(301,360,399,458),'#234d60')
    ellipse(q,(308,367,392,451),'#337386')
    poly(q,path([(314,408),(312,382,337,367,361,373),(340,380,328,394,327,418)]),'#a9d9d2')
    ellipse(q,(362,425,379,442),'#5995a1')
    for a in range(0,360,60):
        x=350+61*math.cos(math.radians(a)); y=409+61*math.sin(math.radians(a))
        ellipse(q,(x-3,y-3,x+3,y+3),NAVY)
    text(q,(306,513),'01',55,NAVY,True)
    # Central stabilizer and small rivets.
    poly(q,path([(350,572),(327,615,329,706,350,747),(371,706,373,615,350,572)]),CORAL,NAVY,3)
    line(q,[(350,589),(350,727)],'#faab78',3)
    for x in (290,410):
        for y in (600,625):
            ellipse(q,(x-2,y-2,x+2,y+2),NAVY)
    ship=ship.rotate(-29,resample=Image.Resampling.BICUBIC,expand=True)
    im.paste(ship,(int(190*S),int(232*S)),ship)
    d=ImageDraw.Draw(im)
    # Foreground lunar horizon; cropped to the ink field.
    terrain=Image.new('RGBA',im.size,(0,0,0,0)); td=ImageDraw.Draw(terrain)
    ellipse(td,(-290,1450,1760,2380),'#91a5a0')
    ellipse(td,(-245,1480,1715,2390),'#b7beb0')
    ellipse(td,(150,1542,420,1602),'#7c9492')
    ellipse(td,(168,1554,408,1602),'#9baba3')
    ellipse(td,(936,1518,1090,1556),'#819995')
    ellipse(td,(949,1528,1084,1556),'#a1b0a7')
    im.paste(terrain.crop((60*S,1450*S,1340*S,1630*S)),(60*S,1450*S),terrain.crop((60*S,1450*S,1340*S,1630*S)))
    d=ImageDraw.Draw(im)
    text(d,(74,1670),'KEEP LOOKING UP.',48,NAVY,True)
    text(d,(1038,1683),'EXPLORATION',18,NAVY,True)
    text(d,(1038,1711),'STARTS HERE',18,NAVY)
    # Very light deterministic paper grain at delivery resolution.
    im=im.resize((W,H),Image.Resampling.LANCZOS)
    pixels=im.load()
    for _ in range(175000):
        x=random.randrange(W); y=random.randrange(H)
        c=pixels[x,y]; v=random.choice([-5,-3,3,5])
        pixels[x,y]=tuple(max(0,min(255,k+v)) for k in c)
    out=ROOT/'rocket.png'
    im.save(out,optimize=True)
    print(f'SAVED {out}')
    print(f'IMAGE size={im.size} mode={im.mode} bytes={out.stat().st_size}')


if __name__=='__main__':
    main()
