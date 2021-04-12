""" Crossbreed and mutate bitmaps.
Possible mutations:
    Channel swap
    Boolean:    XOR/XNOR
                AND/NAND
                OR/NOR

Mutation areas:
    Polygons
    linear

Can we select the area and the mutation separately.
"""
from bitmap import bitmap
import random


class FullImageTranscriber:
    """
    Transcribe the complete image with some crossover and mutations.
    """

    def __init__(self, parent1: bitmap.Bitmap, parent2: bitmap.Bitmap, crossoverChance=0, crossoverPositions=[]):
        self.xmax = min(parent1.dims[0], parent2.dims[0])
        self.ymax = min(parent1.dims[1], parent2.dims[1])
        pixelCount = self.ymax * self.xmax
        self.crossoverPositions = crossoverPositions + [pixelCount]
        if crossoverChance:
            for i in range(pixelCount):
                if random.random() < crossoverChance:
                    self.crossoverPositions.append(i)

        self.crossoverPositions = [round(p) for p in sorted(self.crossoverPositions, reverse=True)]
        self.psParent1 = [p for row in parent1.pixels[:self.ymax] for p in row[:self.xmax]]
        self.psParent2 = [p for row in parent2.pixels[:self.ymax] for p in row[:self.xmax]]
        # print("p1:{}, p2:{}".format(len(self.psParent1), len(self.psParent2)))

    @staticmethod
    def _chop(pixels, rowLen):
        rows = []
        while pixels:
            row = pixels[:rowLen]
            rows.append(row)
            pixels = pixels[rowLen:]
        return rows

    def transcribe(self):
        """Include possible mutations as dict/tuple with funcs and concomitant probabilities?"""
        psOffspring1 = []
        psOffspring2 = []
        # print(self.crossoverPositions)

        currentStartPos = 0
        crossed = True
        while self.crossoverPositions:
            # print("p1:{}, p2:{}".format(len(psOffspring1), len(psOffspring2)))
            pos = self.crossoverPositions.pop()
            excerpt1 = self.psParent1[currentStartPos:pos]
            excerpt2 = self.psParent2[currentStartPos:pos]
            # mutate excerpts here? #
            if crossed:
                psOffspring2.extend(excerpt1)
                psOffspring1.extend(excerpt2)
            else:
                psOffspring1.extend(excerpt1)
                psOffspring2.extend(excerpt2)
            crossed = not crossed
            currentStartPos = pos

        # print("p1:{}, p2:{}".format(len(psOffspring1), len(psOffspring2)))
        return [bitmap.Bitmap((self.xmax, self.ymax), self._chop(psOffspring1, self.xmax)),
                bitmap.Bitmap((self.xmax, self.ymax), self._chop(psOffspring2, self.xmax))]

    @classmethod
    def double(cls, bmp1: bitmap.Bitmap, bmp2: bitmap.Bitmap, positions=None):
        xmax = min(bmp1.dims[0], bmp2.dims[0])
        ymax = min(bmp1.dims[1], bmp2.dims[1])
        pixelCount = ymax * xmax
        if not positions:
            positions = [random.gauss(mu=pixelCount / 3, sigma=pixelCount * 0.066)]
        if len(positions) < 2:
            centre = pixelCount - positions[0] / 2
            deviation = pixelCount * 0.066
            positions.append(random.gauss(mu=centre, sigma=deviation))
        return cls(bmp1, bmp2, crossoverPositions=positions)

    @classmethod
    def multiple(cls, bmp1: bitmap.Bitmap, bmp2: bitmap.Bitmap, crossoverChance=0.001):
        return cls(bmp1, bmp2, crossoverChance=crossoverChance)

    @classmethod
    def single(cls, bmp1: bitmap.Bitmap, bmp2: bitmap.Bitmap, position=None):
        if position is None:
            xmax = min(bmp1.dims[0], bmp2.dims[0])
            ymax = min(bmp1.dims[1], bmp2.dims[1])
            pixelCount = ymax * xmax
            centre = pixelCount / 2
            deviation = pixelCount * 0.1
            position = random.gauss(mu=centre, sigma=deviation)
        return cls(bmp1, bmp2, crossoverPositions=[position])
