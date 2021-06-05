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

import math
import random


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


def crossWholeArea(images, mutations=[]):
    pair = [img.copy() for img in images[:2]]
    for area in wholeArea(images):
        regions = [img.crop(area) for img in pair]
        for mutation in mutations:
            regions = mutation(regions)
        pair[0].paste(regions[0], box=area)
        pair[1].paste(regions[1], box=area)
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


def _calculateTranscriptionAreas():
    pass


def mutationRandomSwap(regions):
    random.shuffle(regions)
    return regions


def mutationTranscription(regions, crosses=None):
    # print(regions)
    width, height = regions[0].size
    pixelCount = width * height

    if crosses is None:
        crossoverChance = random.randint(1, 7) / pixelCount
    else:
        crossoverChance = crosses / pixelCount

    pair = [img.copy() for img in regions[:2]]

    crossoverPositions = []
    for i in range(pixelCount):
        if random.random() < crossoverChance:
            crossoverPositions.append((i, i // width, i % width))
    crossoverPositions.append((pixelCount, height - 1, width - 1))

    # print(crossoverPositions)
    for i in range(len(crossoverPositions) // 2):
        (iStart, rowStart, colStart), (iEnd, rowEnd, colEnd) = crossoverPositions[:2]
        del crossoverPositions[:2]

        if rowStart == rowEnd:
            areas = [(colStart, rowStart, colEnd, rowEnd)]
        elif rowStart == rowEnd - 1:
            areas = [(colStart, rowStart, width, rowStart),
                     (0, rowEnd, colEnd, rowEnd)
                     ]
        else:
            areas = [(colStart, rowStart, width, rowStart),
                     (0, rowStart + 1, width, rowEnd - 1),
                     (0, rowEnd, colEnd, rowEnd)
                     ]

        # print (areas)
        for area in areas:
            # print(area)
            cut0 = pair[0].crop(area)
            cut1 = pair[1].crop(area)
            pair[0].paste(cut1, box=area)
            pair[1].paste(cut0, box=area)

    return pair
