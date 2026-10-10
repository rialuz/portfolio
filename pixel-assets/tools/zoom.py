"""Zoomed, gridded crops of several sprites side by side, with pixel coordinates on the axes.
usage: zoom.py <out.png> <x0,y0,x1,y1> <scale> <png>..."""
import os, sys
from PIL import Image, ImageDraw
out, box, k, paths = sys.argv[1], tuple(int(v) for v in sys.argv[2].split(",")), int(sys.argv[3]), sys.argv[4:]
w, h = (box[2] - box[0]) * k, (box[3] - box[1]) * k
sheet = Image.new("RGB", (len(paths) * (w + 26) + 6, h + 34), (251, 233, 229))
d = ImageDraw.Draw(sheet)
for i, p in enumerate(paths):
    im = Image.open(p).convert("RGBA")
    crop = im.crop(box).resize((w, h), Image.NEAREST)
    x0, y0 = 26 + i * (w + 26), 26
    sheet.paste(crop, (x0, y0), crop)
    for gx in range(box[0], box[2] + 1):
        d.line([x0 + (gx - box[0]) * k, y0, x0 + (gx - box[0]) * k, y0 + h], fill=(236, 214, 210))
        if gx % 2 == 0 and gx < box[2]: d.text((x0 + (gx - box[0]) * k + 2, 13), str(gx), fill=(90, 80, 100))
    for gy in range(box[1], box[3] + 1):
        d.line([x0, y0 + (gy - box[1]) * k, x0 + w, y0 + (gy - box[1]) * k], fill=(236, 214, 210))
        if gy < box[3]: d.text((x0 - 16, y0 + (gy - box[1]) * k + 2), str(gy), fill=(90, 80, 100))
    d.text((x0, 1), os.path.basename(p), fill=(40, 40, 60))
sheet.save(out); print(sheet.size)
