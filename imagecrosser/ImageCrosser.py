"""
Crossbreed images using a number of techniques:
    1. Linear transcription with crossing.
    2. Rotational/Transpositional transformation
    3. Bitwise operations

Scopes:
    1: Entire Image
    2: Subrectangle
    3: Tesselated

Ultimately a set of tessera can encapsulate each of these scopes.  For 1 & 2 this would be a single 'tile', for 3 a 2D
number.
"""

import random


def cross(images):
    pass


def crossSubImage(images):
    pair = [img.copy() for img in images[:2]]
    for area in selectSubRegion(images):
        region0 = pair[0].crop(area)
        region1 = pair[1].crop(area)
        pair[0].paste(region1, box=area)
        pair[1].paste(region0, box=area)
    return pair


def crossTesselated(images, counts=(3, 3)):
    pair = [img.copy() for img in images[:2]]
    for area in tessellatedAreas(images, counts):
        if random.choice([0, 1]):
            region0 = pair[0].crop(area)
            region1 = pair[1].crop(area)
            pair[0].paste(region1, box=area)
            pair[1].paste(region0, box=area)
    return pair


def calculateOverlap(images):
    sizes = [img.size for img in images]
    return [min(dims) for dims in zip(*sizes)]


def selectSubRegion(images):
    overlap = calculateOverlap(images)
    yield [overlap[0] // 4, overlap[1] // 4, 3 * overlap[0] // 4, 3 * overlap[1] // 4]


def tessellatedAreas(images, counts):
    overlap = calculateOverlap(images)
    for n in range(counts[1]):
        y1 = (n * overlap[1]) // counts[1]
        y2 = ((n + 1) * overlap[1]) // counts[1]
        for m in range(counts[0]):
            x1 = (m * overlap[0]) // counts[0]
            x2 = ((m + 1) * overlap[0]) // counts[0]
            yield (x1, y1, x2, y2)


def wholeArea(images):
    yield [0, 0, *calculateOverlap(images)]
