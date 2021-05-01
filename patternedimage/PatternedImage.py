"""
A refactoring of the Bitmap object to use Pillow Images
"""

from PIL import Image
import numpy as np

import json
import random

from shared import shared
from vector import vector

import pathlib


def _parseColoursList(colours=None):
    """
    Take 'any' input and return a list of colour tuples.

    :param colours: The colour description(s)
    :return:
    """
    if colours is None:
        # print("None")
        return [(255, 255, 255)]
    elif type(colours) is int or type(colours) is float:
        # print("Number")
        return [shared.fillOutTuple(colours, 3)]
    elif type(colours) is tuple:
        return [shared.fillOutTuple(colours, 3)]
    else:
        return [shared.fillOutTuple(c, 3) for c in colours]


def new(pattern=None, dims=(1080, 1080), colours=None, **kwargs):
    """
    Generate a new Image with a pattern.  Assume that all patterns are generated

    :return: an Image with a pattern conforming to the requested.
    """

    if pattern is None:  # Return arbitrary pattern
        f = random.choice([checkerboard, diamonds, gaussian, gradient, striped, stripedMulti])
        if f == stripedMulti:
            colours = shared.randomRGBContrasting(random.randint(3, 7))
        elif f == gaussian:
            choice = random.randrange(4)
            if choice == 0:
                colours = [(0, 0, 0), (255, 255, 255)]
            elif choice == 1:
                colours = [(255, 255, 255), (0, 0, 0)]
            else:
                colours = shared.randomRGBContrasting(2)
        elif colours is None:
            if random.choice([0, 1]):
                colours = shared.randomRGBContrasting(2)
            else:
                colours = shared.randomRGBPair()
    else:
        f = pattern

    # return Image.new(mode="RGB", size=dims, color=colours[0])
    return f(dims=dims, colours=colours, **kwargs)


def checkerboard(dims, colours=[0, 255], checksize=None):
    if checksize is None:
        minCheckSize = max(4, min(dims) // 128)
        maxCheckSize = min(dims) // 5
        checksize = random.randint(minCheckSize, maxCheckSize)
    cols = _parseColoursList(colours)[:2]
    img = Image.new(mode="RGB", size=dims, color=cols[1])

    xmax, ymax = dims
    for y in range(ymax):
        for x in range(xmax):
            if ((x % (2 * checksize)) >= checksize) ^ ((y % (2 * checksize)) >= checksize):
                img.putpixel((x, y), cols[0])
    return img


def diamonds(dims, colours=[0, 255], angles=None, sizes=None):
    if angles is None:
        angle1 = random.randint(0, 89)
        angles = (angle1, angle1 + random.randint(15, 104))
    vUnitH, vUnitV = shared._diamondVectors(angles)
    vOrigin = vector.Vector(vector.radialIntersection(dims, vUnitH.phaseAngle()))

    if sizes is None:
        sizes = (random.randint(3, dims[0] // 4), random.randint(3, dims[1] // 4))
    sizeH, sizeV = shared.fillOutList(sizes, 2)

    cols = _parseColoursList(colours)[:2]
    img = Image.new(mode="RGB", size=dims, color=cols[1])

    xmax, ymax = dims
    for y in range(ymax):
        for x in range(xmax):
            vPosition = vector.Vector2D([x, y]) - vOrigin

            distanceAlongHorizontal = vector.dotProduct(vPosition, vUnitH)
            distanceAlongVertical = vector.dotProduct(vPosition, vUnitV)
            distThroughPatternHorizontal = distanceAlongHorizontal % (2 * sizeH)
            distThroughPatternVertical = distanceAlongVertical % (2 * sizeV)

            if (distThroughPatternHorizontal < sizeH) ^ (distThroughPatternVertical >= sizeV):
                baseColour = cols[0]
                mixColour = cols[1]
            else:
                baseColour = cols[1]
                mixColour = cols[0]

            mixRateH = [1]
            if distThroughPatternHorizontal < 1:
                mixRateH = [1 - distThroughPatternHorizontal, distThroughPatternHorizontal]
            elif sizeH < distThroughPatternHorizontal < sizeH + 1:
                distIntoNextColour = distThroughPatternHorizontal - sizeH
                mixRateH = [1 - distIntoNextColour, distIntoNextColour]

            mixRateV = [1]
            if distThroughPatternVertical < 1:
                mixRateV = [1 - distThroughPatternVertical, distThroughPatternVertical]
            elif sizeV < distThroughPatternVertical < sizeV + 1:
                distIntoNextColour = distThroughPatternVertical - sizeV
                mixRateV = [1 - distIntoNextColour, distIntoNextColour]

            # First implementation : Mix proportions as if diamonds are square: this might make points ill-defined!
            # Probably should add some kind of cos theta element.
            proportions = [pH * pV for pH in mixRateH for pV in mixRateV]

            # print("{} = {}".format(proportions, sum(proportions)))
            if len(proportions) == 1:
                c = baseColour
            if len(proportions) == 2:
                c = shared.rgbBlend(baseColour, mixColour, proportions[0])
            if len(proportions) == 4:
                c = shared.rgbBlend(baseColour, mixColour, proportions[0] + proportions[3])
            img.putpixel((x, y), c)
    return img


def gradient(dims, colours=[0, 255], angle=None):
    if angle is None:
        angle = random.randint(-87, 83)

    vUnit = vector.Vector2D.unit(angle)
    vOrigin = vector.Vector(vector.radialIntersection(dims, angle - 180))
    vTerminus = vector.Vector(vector.radialIntersection(dims, angle))
    distanceTotal = (vTerminus - vOrigin).magnitude()
    cols = _parseColoursList(colours)[:2]
    img = Image.new(mode="RGB", size=dims, color=cols[0])

    xmax, ymax = dims
    for y in range(ymax):
        for x in range(xmax):
            vPosition = vector.Vector2D([x, y]) - vOrigin
            distanceAlongDirection = vector.dotProduct(vPosition, vUnit)
            colour = shared.rgbBlend(*cols, distanceAlongDirection / distanceTotal)
            img.putpixel((x, y), colour)
    return img


def striped(dims=(1080, 1080), colours=[0, 255], stripewidth=None, angle=None):
    """
    :param dims:
    :param colours:
    :return:
    """

    cols = _parseColoursList(colours)

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


def stripedMulti(dims=(1080, 1080), colours=[0, 255], stripewidth=None, angle=None):
    """
    Multicolour stripes.  Can't figure out why interpolation doesn't work so interpolation is disabled.
    :param dims:
    :param colours:
    :return:
    """

    cols = _parseColoursList(colours)
    colourCount = len(cols)

    img = Image.new(mode="RGB", size=dims, color=cols[0])
    if stripewidth is None:
        maxstripewidth = min(dims) // (colourCount + 1)
        stripewidth = random.randint(5, maxstripewidth)

    if angle is None:
        angle = random.randint(-87, 83)

    # angle = 0
    # stripewidth = 26.6

    vUnit = vector.Vector2D.unit(angle)
    vOrigin = vector.Vector(vector.radialIntersection(dims, angle - 180))
    # print("{}: {}".format(vUnit, vOrigin))

    xmax, ymax = dims
    colour1 = cols[0]
    colour2 = cols[1]
    colourCount = len(cols)
    patternLength = colourCount * stripewidth
    for y in range(ymax):
        for x in range(xmax):
            vPosition = vector.Vector2D([x, y]) - vOrigin
            distanceAlongDirection = vector.dotProduct(vPosition, vUnit)
            distanceThroughPattern = distanceAlongDirection % patternLength
            distanceAcrossStripe = distanceThroughPattern % stripewidth
            colourIndex = int(distanceThroughPattern / stripewidth)
            colour0 = cols[(colourIndex - 1) % colourCount]
            colour1 = cols[colourIndex]
            colour2 = cols[(colourIndex + 1) % colourCount]

            # if distanceAcrossStripe < 1:
            #     c = shared.rgbBlend(colour0, colour1, distanceAcrossStripe)
            # elif stripewidth - 1 < distanceAcrossStripe:
            #     c = shared.rgbBlend(colour1, colour2, stripewidth - distanceAcrossStripe)
            # # elif distanceAcrossStripe >= stripewidth:
            # #     c = colour2
            # else:
            #     c = colour1
            c = colour1
            img.putpixel((x, y), c)
    return img


def _generateGaussianFilename(dims, colours):
    """Deprecated: """
    ds = dims[:2]
    return "gaussians/{0}x{1}/{0}x{1}_{2},{3},{4}_{5},{6},{7}".format(*ds, *colours[0], *colours[1])


def _generateGaussianDistributionFilename(dims, mus=None, sigmas=None, index=0):
    if mus is None:
        musDesc = ""
    else:
        musDesc = "_μs({},{})".format(*mus)

    if sigmas is None:
        sigmasDesc = ""
    else:
        sigmasDesc = "_σs({},{})".format(*sigmas)

    return "{}x{}{}{}_{}.json".format(*dims[:2], musDesc, sigmasDesc, index)


def _generate2DGaussianDistribution(dims, mus=None, sigmas=None, deltaCount=100):
    """
    Generate a statistically normal distribution.  Take small steps from zero to one so that this can be mapped onto a
    colour difference.

    :param dims: Dimensions of the image
    :param mus: Position of mu of normal distribution: essentially the [x, y] coordinate of the centre of the 2D
                distribution.
    :param sigmas: Standard deviation of the distribution - essentially the width of the 'dot'.
    :param deltaCount:  No of steps.
    :return: A list of lists of normalised
    """
    xmax, ymax = dims
    if mus:
        xmu, ymu = mus
    else:  # Default is centre of image
        xmu = xmax / 2
        ymu = ymax / 2

    if sigmas:
        xsigma, ysigma = sigmas
    else:  # Default is centre of image
        xsigma = xmax / 4
        ysigma = ymax / 4

    delta = 1 / deltaCount

    values = [[0.0] * xmax for i in range(ymax)]

    terminalReached = False
    while not terminalReached:
        x = round(random.gauss(xmu, xsigma))
        y = round(random.gauss(ymu, ysigma))
        if 0 <= x < xmax and 0 <= y < ymax:
            values[y][x] += delta
            if values[y][x] >= 1.0:
                values[y][x] = 1.0
                terminalReached = True

    return values


def _get6DGaussianDistribution(dims):
    """Assume default mus and sigmas for now."""
    fileCount = 10  # number of json files stored
    xmax, ymax = dims
    foldername = "gaussiandists/{}x{}/".format(xmax, ymax)
    p = pathlib.Path(foldername)
    p.mkdir(parents=True, exist_ok=True)

    dists = []

    for i in range(3):
        fs = [f for f in p.iterdir() if f.is_file() and f.suffix == '.json']
        choice = random.randrange(fileCount)
        # print(fs)
        # print(choice)
        if choice < len(fs):
            with fs[choice].open(encoding="UTF-8") as source:
                dist = json.load(source)
        else:
            dist = _generate2DGaussianDistribution(dims)
            filepath = p / _generateGaussianDistributionFilename(dims, index=len(fs))
            with filepath.open("w", encoding="UTF-8") as target:
                json.dump(dist, target)
        dists.append(shared.reorient(dist, random.randrange(8)))

    return [list(zip(dists[0][i], dists[1][i], dists[2][i])) for i in range(ymax)]


def gaussian(dims, colours=None):
    """Assume default mus, sigmas and deltas for now."""
    xmax, ymax = dims
    dists = _get6DGaussianDistribution(dims)
    # print(dists)
    # for row in dists:
    #     print(row)
    cols = _parseColoursList(colours)
    colourCount = len(cols)

    img = Image.new(mode="RGB", size=dims, color=cols[0])
    for y in range(ymax):
        for x in range(xmax):
            c = shared.rgbBlendPerChannel(cols[0], cols[1], dists[y][x])
            img.putpixel((x, y), c)


    return img
