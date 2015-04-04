#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image


def img2txt(image_raw):
    # grayscale
    color = "MNHQ$OC?7>!:-;. "

    with Image.open(image_raw) as im:
        width, height = im.size
        rate = 100.0 / max(width, height)
        width = int(rate * width)
        height = int(rate * height)

        resized_img = im.resize((width, height))

        pixel = resized_img.load()

        line = ''
        for h in xrange(height):
            for w in xrange(width):
                rgb = pixel[w, h]
                line += color[int(rgb / 3.0 / 256.0 * 16)]
            line += "\n"
        return line
    return None
