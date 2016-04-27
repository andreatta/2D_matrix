#!/usr/bin/env python
"""
Create 2D Matrix bitmpap from Ferag String.
"""

import re
import os.path
import argparse
from PIL import Image

MATRIXFILE = "2DMatrix.bmp"
PATTERN = r"\{SK\|(\d+)\|(\d+)\|(\d+)\|([\s\S]+)\}"
FONT = []

parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', default='2DMatrix.bin')
args = parser.parse_args()

"""
Create a list of bitmaps that represent a font.
This font has 16 characters wich each represent half a character
received from the Ferag String.
"""
def create_font():
    dot = Image.new('RGB', (2, 2), "black")

    for halfchar in range(0, 16):
        img = Image.new('RGB', (2, 8), "white")
        for bit in range(0, 4):
            bits = str(bin(halfchar))[2:].zfill(4)[::-1]
            if bits[bit] == '1':
                img.paste(dot, (0, (2*bit)))

        FONT.append(img)

"""
Read a file given as parameter or just try to open file with default name.
"""
if os.path.exists(args.file):
    print("converting Matrix '%s' to '%s'" % (args.file, MATRIXFILE))
else:
    print("file '%s' does not exist" % args.file)
    quit()

create_font()

"""
Read file and parse Ferag String to create a 2D Matrix bitmap.
Each module (1 square of the 2D Matrix) consists of 4 drops.

Ferag String format for 2D Matrix:
{SK|<LEN>|<HEIGHT>|<WIDTH>|<BYTE DATA>}
"""
with open(args.file, 'rt') as matrixfile:
    matrixstr = matrixfile.read()
    matrixfile.close()
    m = re.search(PATTERN, matrixstr)

    if m is not None and len(m.groups()) == 4:
        data = m.group(4)
        width = int(m.group(3))
        height = int(m.group(2))
        length = int(m.group(1))
        print("width %d height %d length %d" % (width, height, length))
        matrix = Image.new('RGB', (2*width, 2*height), "white")

        # create list with separated rows to draw
        # a row consists of 'width' characters
        matrixrowlist = [data[i:i+height] for i in range(0, length, height)]

        for offset, row in enumerate(matrixrowlist):
            for i, char in enumerate(row):
                # first line of row
                low = ord(char) & 0x0f
                # second line of row
                high = (ord(char) >> 4) & 0x0f
                #print("c=%s low=%d high=%d" % (c, low, high))
                matrix.paste(FONT[low], (2*i, 16*offset))
                matrix.paste(FONT[high], (2*i, 16*offset + 8))

        matrix.save(MATRIXFILE)

    else:
        print('Wrong format')
        print('Ferag String has to be in format: {SK|<LEN>|<HEIGHT>|<WIDTH>|<BYTE DATA>}')

