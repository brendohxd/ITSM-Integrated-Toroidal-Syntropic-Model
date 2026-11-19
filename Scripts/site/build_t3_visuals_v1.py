"""Build the original T3 periodic-cell identity and public diagram exports.

These are coordinate illustrations, not physical geometry or simulation data.
Requires the installed PyMuPDF and Pillow packages for raster exports.
"""
from pathlib import Path
from io import BytesIO
import hashlib
import json
import pymupdf as fitz
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
DOCS=ROOT/'docs'
OUT=DOCS/'assets/atlas'
BACK=ROOT/'.local/t3-atlas-20261119/preimages'
COLORS={'x':'#72d7cd','y':'#e6ba7b','z':'#b7a0eb'}

def save(path,data):
    if path.exists():
        previous=BACK/path.relative_to(ROOT)
        if not previous.exists():
            previous.parent.mkdir(parents=True,exist_ok=True)
            previous.write_bytes(path.read_bytes())
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data)

def point(x,y,z):
    return (340+170*x-150*y,300+82*x+93*y-200*z)

def pts(points):
    return ' '.join(f'{x:.2f},{y:.2f}' for x,y in points)

def cell_group():
    vertices={(x,y,z):point(x,y,z) for x in (0,1) for y in (0,1) for z in (0,1)}
    faces={
        'x':[(1,0,0),(1,1,0),(1,1,1),(1,0,1)],
        'y':[(0,1,0),(1,1,0),(1,1,1),(0,1,1)],
        'z':[(0,0,1),(1,0,1),(1,1,1),(0,1,1)]}
    parts=[]
    # Reference cells suggest repeated coordinates, not additional universes.
    for dx,dy,opacity in [(170,82,'.10'),(-150,93,'.08')]:
        parts.append(f'<g transform="translate({dx} {dy})" opacity="{opacity}" fill="none" stroke="#80b5c2" stroke-width="1">')
        for axis,face in faces.items():
            parts.append(f'<polygon points="{pts([vertices[v] for v in face])}"/>')
        parts.append('</g>')
    for axis,face in faces.items():
        parts.append(f'<polygon points="{pts([vertices[v] for v in face])}" fill="{COLORS[axis]}" fill-opacity=".075" stroke="{COLORS[axis]}" stroke-opacity=".75" stroke-width="1.6"/>')
    parts.append('<g stroke="#b8d2d8" stroke-width=".7" opacity=".18" fill="none">')
    for f in (.25,.5,.75):
        for a,b in [((f,0,1),(f,1,1)),((0,f,1),(1,f,1)),((1,f,0),(1,f,1)),((1,0,f),(1,1,f)),((f,1,0),(f,1,1)),((0,1,f),(1,1,f))]:
            parts.append(f'<polyline points="{pts([point(*a),point(*b)])}"/>')
    parts.append('</g>')
    parts.append('<g fill="none" stroke="#809ba8" stroke-width="1.1" stroke-dasharray="4 6" opacity=".45">')
    for a,b in [((0,0,0),(1,0,0)),((0,0,0),(0,1,0)),((0,0,0),(0,0,1))]:
        parts.append(f'<polyline points="{pts([point(*a),point(*b)])}"/>')
    parts.append('</g>')
    paths=[('x',(0,.45,.45),(1,.45,.45)),('y',(.55,0,.62),(.55,1,.62)),('z',(.32,.68,0),(.32,.68,1))]
    for axis,start,end in paths:
        a,b=point(*start),point(*end);color=COLORS[axis]
        parts.append(f'<path d="M {a[0]:.2f} {a[1]:.2f} L {b[0]:.2f} {b[1]:.2f}" fill="none" stroke="{color}" stroke-width="2.1" stroke-dasharray="3 7"/>')
        for x,y in (a,b):
            parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5.5" fill="#0a141c" stroke="{color}" stroke-width="2.3"/>')
    for label,(x,y),color in [('x',(500,350),COLORS['x']),('y',(205,345),COLORS['y']),('z',(350,155),COLORS['z'])]:
        parts.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="17" fill="{color}">{label}</text>')
    return ''.join(parts)

def svg(width,height,body,title,desc):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{title}</title><desc>{desc}</desc>{body}</svg>'

def png(body,width):
    doc=fitz.open(stream=body.encode('utf-8'),filetype='svg')
    page=doc[0]
    return page.get_pixmap(matrix=fitz.Matrix(width/page.rect.width,width/page.rect.width),alpha=False).tobytes('png')

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    intro='<rect width="680" height="600" rx="12" fill="#0a141c"/><path d="M 34 64 H 646 M 34 528 H 646" stroke="#28404d"/>'
    intro+='<text x="34" y="40" fill="#c4d2d5" font-family="Arial,sans-serif" font-size="12" letter-spacing="2">SPATIAL TOPOLOGY / T3</text>'
    intro+='<text x="34" y="563" fill="#a7bbc5" font-family="Arial,sans-serif" font-size="13">Three spatial identifications. One connected space.</text>'
    intro+='<text x="34" y="585" fill="#7f97a5" font-family="Arial,sans-serif" font-size="11">Fundamental-cell schematic; shape and scale are illustrative.</text>'
    cell=svg(680,600,intro+cell_group(),'T3 periodic-coordinate cell','Three independent spatial identifications. Matching colored endpoints are identified across opposite cell faces. This chart is not a box surrounding space or a doughnut surface. It does not fix the physical cell size or shape.')
    save(OUT/'t3-periodic-cell_v1.svg',cell.encode())
    save(OUT/'t3-periodic-cell_v1.png',png(cell,1360))
    guide='<rect width="1000" height="660" fill="#0a141c"/><text x="56" y="65" fill="#eef1e9" font-family="Georgia,serif" font-size="36">Three directions. Three identifications.</text><text x="56" y="101" fill="#a7bbc5" font-family="Arial,sans-serif" font-size="16">A coordinate guide to T3 = S1 x S1 x S1</text>'
    rows=[('x','(0, y, z)','(Lx, y, z)','Keep y and z unchanged.'),('y','(x, 0, z)','(x, Ly, z)','Keep x and z unchanged.'),('z','(x, y, 0)','(x, y, Lz)','Keep x and y unchanged.')]
    for i,(axis,left,right,note) in enumerate(rows):
        y=151+i*142;c=COLORS[axis]
        guide+=f'<rect x="56" y="{y}" width="888" height="118" rx="5" fill="#111f29" stroke="#29424e"/><rect x="56" y="{y}" width="4" height="118" fill="{c}"/><text x="82" y="{y+42}" fill="{c}" font-family="Arial,sans-serif" font-size="18">{axis.upper()} PAIR</text><text x="265" y="{y+43}" fill="#eef1e9" font-family="Arial,sans-serif" font-size="23">{left}</text><path d="M 484 {y+34} H 561 m -8 -6 8 6 -8 6 M 561 {y+48} H 484 m 8 -6 -8 6 8 6" stroke="{c}" stroke-width="2" fill="none"/><text x="600" y="{y+43}" fill="#eef1e9" font-family="Arial,sans-serif" font-size="23">{right}</text><text x="265" y="{y+83}" fill="#a7bbc5" font-family="Arial,sans-serif" font-size="15">{note}</text>'
    guide+='<text x="56" y="617" fill="#a7bbc5" font-family="Arial,sans-serif" font-size="14">Opposite faces are identified by translations. No physical wall is introduced.</text><text x="56" y="642" fill="#7f97a5" font-family="Arial,sans-serif" font-size="12">The rectangular chart is illustrative; topology does not select Lx, Ly, Lz or the local metric.</text>'
    guide=svg(1000,660,guide,'T3 face-pair coordinate guide','Three pairs of opposite faces are identified independently with no reversal of the other coordinates. Time is not included among these spatial identifications.')
    save(OUT/'t3-face-pairs_v1.svg',guide.encode());save(OUT/'t3-face-pairs_v1.png',png(guide,1600))
    markbody='<rect width="128" height="128" rx="26" fill="#0a141c"/><g stroke-linejoin="round" fill="none" stroke-width="3.3"><path d="M 64 23 104 44 64 66 24 44 Z" stroke="#b7a0eb"/><path d="M 24 44 V 86 L 64 108 104 86 V 44 M 64 66 V 108" stroke="#94acb6"/><path d="M 64 66 104 44 V 86 L 64 108" stroke="#72d7cd"/><path d="M 24 44 64 66 V 108 L 24 86 Z" stroke="#e6ba7b"/></g><path d="M 64 23 V 65 L 24 86 M 64 65 104 86" fill="none" stroke="#7e99a6" stroke-width="1.2" stroke-dasharray="3 4"/>'
    mark=svg(128,128,markbody,'ITSM periodic-cell mark','A stylized coordinate cell with three colored spatial identifications; not an embedded torus surface.')
    save(DOCS/'favicon.svg',mark.encode());save(OUT/'itsm-periodic-mark_v1.svg',mark.encode())
    image=Image.open(BytesIO(png(mark,512))).convert('RGB')
    for size,name in [(16,'favicon-16x16.png'),(32,'favicon-32x32.png'),(180,'apple-touch-icon.png'),(192,'android-chrome-192x192.png'),(512,'android-chrome-512x512.png')]:
        data=BytesIO();image.resize((size,size),Image.Resampling.LANCZOS).save(data,format='PNG');save(DOCS/name,data.getvalue())
    for size in (192,512):
        canvas=Image.new('RGB',(size,size),'#0a141c');inner=image.resize((round(size*.78),round(size*.78)),Image.Resampling.LANCZOS);canvas.paste(inner,((size-inner.width)//2,(size-inner.height)//2));data=BytesIO();canvas.save(data,format='PNG');save(DOCS/f'android-chrome-maskable-{size}x{size}.png',data.getvalue())
    ico=BytesIO();image.save(ico,format='ICO',sizes=[(16,16),(32,32),(48,48)]);save(DOCS/'favicon.ico',ico.getvalue())
    share='<rect width="1200" height="630" fill="#0a141c"/><path d="M 64 88 H 1136 M 64 557 H 1136" stroke="#29424e"/><text x="64" y="64" fill="#72d7cd" font-family="Arial,sans-serif" font-size="15" letter-spacing="3">ITSM / COSMOLOGY RESEARCH</text><text x="64" y="225" fill="#f2f0e6" font-family="Georgia,serif" font-size="58">An active vacuum.</text><text x="64" y="295" fill="#e6ba7b" font-family="Georgia,serif" font-size="58">A connected universe.</text><text x="64" y="367" fill="#becdd3" font-family="Arial,sans-serif" font-size="20">Finite-density vacuum. Three periodic directions.</text><text x="64" y="404" fill="#becdd3" font-family="Arial,sans-serif" font-size="20">A programme of physical tests.</text><text x="64" y="526" fill="#93a9b6" font-family="Arial,sans-serif" font-size="15">Integrated Toroidal-Syntropic Model / Brendon Boyd</text><text x="64" y="594" fill="#93a9b6" font-family="Arial,sans-serif" font-size="14">itsm-cosmology.com  |  Research proposal; physical viability remains under investigation.</text><g transform="translate(585 20) scale(.93)">'+cell_group()+'</g>'
    share=svg(1200,630,share,'ITSM research identity','A schematic three-dimensional periodic cell accompanies the ITSM research proposal. It is not a donut-shaped universe or a physical simulation.')
    save(OUT/'itsm-research-share_v1.svg',share.encode());save(OUT/'itsm-research-share_v1.png',png(share,1200))
    files=sorted([p for p in OUT.iterdir() if p.is_file()])
    print(json.dumps({'vector_and_raster_exports':len(files),'model':'three independent spatial identifications','historical_images_modified':False},indent=2))

if __name__=='__main__':main()
