"""
A refactoring of the Bitmap object to use Pillow Images
"""

from PIL import Image
import numpy as np

import random

from shared import shared
from vector import vector


def _parseColours(colours=None):
    """
    Take 'any' input and return a list of colour tuples.

    :param colours: The colour description(s)
    :return:
    """
    if colours is None:
        print("None")
        return [(255, 255, 255)]
    elif type(colours) is int or type(colours) is float:
        print("Number")
        return [shared.fillOutTuple(colours, 3)]
    elif type(colours) is tuple:
        return [shared.fillOutTuple(colours, 3)]
    else:
        return [shared.fillOutTuple(c, 3) for c in colours]


def new(dims=(1080, 1080), pattern=None, colours=None):
    """
    Generate a new Image with a pattern.  Assume that all patterns are generated

    :return: an Image with a pattern conforming to the requested.
    """
    img = Image.new(mode="RGB", size=dims, color=colours[0])

    if pattern is None:
        return img


def Striped(dims=(1080, 1080), colours=[0, 255], stripewidth=None, angle=None):
    """
    :param dims:
    :param colours:
    :return:
    """

    cols = _parseColours(colours)

    img = Image.new(mode="RGB", size=dims, color=cols[0])
    if stripewidth is None:
        maxstripewidth = min(dims) // 3
        stripewidth = random.randint(5, maxstripewidth)

    if angle is None:
        angle = random.randint(-87, 83)

    vUnit = vector.Vector2D.unit(angle)
    vOrigin = vector.Vector(vector.radialIntersection(dims, angle - 180))
    # print("{}: {}".format(vUnit, vOrigin))

    xmax, ymax = dims
    colour1 = cols[0]
    colour2 = cols[1]
    for y in range(ymax):
        for x in range(xmax):
            vPosition = vector.Vector2D([x, y]) - vOrigin
            distanceAlongDirection = vector.dotProduct(vPosition, vUnit)
            distancethroughPattern = distanceAlongDirection % (2 * stripewidth)
            if distancethroughPattern < 1:
                c = shared.rgbBlend(colour2, colour1, distancethroughPattern)
            elif stripewidth - 1 < distancethroughPattern < stripewidth:
                c = shared.rgbBlend(colour2, colour1, stripewidth - distancethroughPattern)
            elif distancethroughPattern >= stripewidth:
                c = colour2
            else:
                c = colour1
            img.putpixel((x, y), c)
    return img
