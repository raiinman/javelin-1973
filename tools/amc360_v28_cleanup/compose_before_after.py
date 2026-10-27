import sys, os
from PIL import Image, ImageDraw, ImageFont
views = ['review_camera', 'front', 'front_closeup', 'front_quarter', 'rear_quarter', 'manifold_right', 'manifold_right_low', 'manifold_left']
notes = {'front_closeup': 'fan blades rebuilt as cambered stamped blades; satin black replaces mirror-gloss enamel',
         'front': 'front "glob" shine removed: flat-shaded blobs -> crisp satin blades and pulleys',
         'manifold_right': 'manifold rebuilt: pads on the head face, primaries sweep rearward into one filleted log, outlet from the underside',
         'manifold_right_low': 'open flange bore on the original throat; alternator clearance kept',
         'manifold_left': 'same construction on the driver side'}
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
except Exception:
    font = ImageFont.load_default()
for v in views:
    a, b = Image.open(f'views/before_{v}.png').convert('RGB'), Image.open(f'views/after_{v}.png').convert('RGB')
    b = b.resize(a.size)
    W, H = a.size
    out = Image.new('RGB', (W * 2 + 12, H + 70), (12, 14, 18))
    out.paste(a, (0, 70)); out.paste(b, (W + 12, 70))
    d = ImageDraw.Draw(out)
    d.text((14, 10), 'BEFORE  (Astra V28 as delivered)', fill=(235, 235, 235), font=font)
    d.text((W + 26, 10), 'AFTER  (Claude cleanup)', fill=(235, 235, 235), font=font)
    d.text((14, 40), notes.get(v, 'same camera and lighting; scale, origin, fit position and parts unchanged'), fill=(170, 190, 205), font=font)
    out.save(f'compare/beforeafter_{v}.png')
    print('compare', v)
