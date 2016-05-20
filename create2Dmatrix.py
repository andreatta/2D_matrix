#!/usr/bin/env python
"""
Create 2D Matrix bitmpap from Ferag String.
"""

import re
import os.path
import argparse
import codecs
from PIL import Image

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

        img.save("bmp/%c.bmp" % chr(halfchar + ord('A')))
        FONT.append(img)

"""
Read a file given as parameter or just try to open file with default name.
"""
if os.path.exists(args.file):
    print("converting Matrix '%s'" % (args.file))
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
with open(args.file, 'rb') as matrixfile:
#with codecs.open(args.file, 'r', 'utf-8') as matrixfile:
    matrixstr = matrixfile.read()
    #print(matrixstr)
    #m = re.search(PATTERN, matrixstr.decode('utf-8'))

    if (matrixstr[0] == ord('{') and matrixstr[-2] == ord('}')):
        content = matrixstr.split(b'|')
        #print(content)
        length = int(content[1])
        height = int(content[2])
        width = int(content[3])
        # get data bytes remove '}\n' at the end
        data = content[4:]
        data = b''.join(data)[:-2]

    #if m is not None and len(m.groups()) == 4:
        #data = m.group(4)
        #width = int(m.group(3))
        #height = int(m.group(2))
        #length = int(m.group(1))
        print("length %d height %d width %d" % (length, height, width))
        print(data)
        matrix = Image.new('RGB', (2*width, 2*height), "white")

        top_line = ""
        bot_line = ""

        # create list with separated rows to draw
        # a row consists of 'width' characters
        matrixrowlist = [data[i:i+width] for i in range(0, length, width)]
        #matrixrowlist = [data[i:i+height] for i in range(0, length, height)]

        for offset, row in enumerate(matrixrowlist):
            #print(len(row))
            #print(row)
            for i, char in enumerate(row):
                # first line of row
                top = char & 0x0f
                bot = (char >> 4) & 0x0f
                top_line += chr(top + ord('A'))
                bot_line += chr(bot + ord('A'))
                #print("%c %d %d" % (char, top, bot))
                matrix.paste(FONT[top], (2*i, 16*offset))
                matrix.paste(FONT[bot], (2*i, 16*offset + 8))

            print(top_line)
            print(bot_line)
            top_line = ""
            bot_line = ""

        matrix.save(args.file.replace('.bin', '.bmp'))

    else:
        print('Wrong format')
        print('Ferag String has to be in format: {SK|<LEN>|<HEIGHT>|<WIDTH>|<BYTE DATA>}')

