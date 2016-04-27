#!/usr/bin/env python
"""
Create bitmaps for 2D Matrix font to be used with kodak DP5220 inkjet printer.
"""

import os.path
from PIL import Image

dot = Image.new('RGB', (2, 2), "black")
DIRNAME = "bmp"

os.makedirs(DIRNAME, 0o755, True)

for halfchar in range(0, 16):
    img = Image.new('RGB', (2, 8), "white")
    for bit in range(0, 4):
        bits = str(bin(halfchar))[2:].zfill(4)[::-1]
        if bits[bit] == '1':
            img.paste(dot, (0, (2*bit)))

    img.save("%s/%s.bmp" % (DIRNAME, chr(halfchar + ord('A'))))
