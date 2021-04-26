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


def _breedMonogamousRandom(currentGen, setcount=None, setsize=2):
    """
    From a generation randomly select monogamous partnerships.

    :param currentGen:  A list of Bitmap objects
    :param setcount:    Total number of 'pairings'
    :param setsize:     How big is a breeding 'couple'?

    :return: breeding 'pairs' as tuples.
    """
    if setcount is None:
        iters = len(currentGen) // setsize
    else:
        iters = min(setcount, len(currentGen) // setsize)

    random.shuffle(currentGen)
    for i in range(iters):  # purely luck
        yield tuple(currentGen[:setsize])
        currentGen = currentGen[setsize:]



class Breeder:
    def __init__(self, breedPatternFunc, breedPatternParams=None, dims=None, genSize=10, gen0=None):
        if gen0:
            self.currentGen = gen0
            self.dims = gen0[0].dims

        else:
            self.currentGen = []
            self.dims = dims
            for i in range(genSize):
                self.currentGen.append(bitmap.Bitmap.arbitrary(dims))

        self.breedPatternFunc = breedPatternFunc
        self.breedPatternParams = breedPatternParams

    def __iter__(self):
        yield self.currentGen
        while (True):
            genNext = []
            for pair in self.breedPatternFunc(self.currentGen, **self.breedPatternParams):
                fit = FullImageTranscriber.multiple(*pair, crossoverChance = random.randint(1, 7) / (540 ** 2))  # ~1-7 crossovers per pair
                genNext.extend(fit.transcribe())
            yield genNext
            genNext.extend(random.sample(self.currentGen, 2))  # select images from previous generation
            genNext.append(bitmap.Bitmap.arbitrary(self.dims))
            self.currentGen = genNext


    @classmethod
    def firstSet(cls, dims=(540, 540)):
        gs = bitmap.GaussianStore(dims)
        gen0 = [
            bitmap.Bitmap.diamonds(dims, sizes=(16, 16), angles=(10, 70),
                                   colour1=(218, 205, 255), colour2=(96, 15, 96)),
            bitmap.Bitmap.stripes(dims, random.randint(13, 63), random.randint(7, 15), (255, 255, 128), (96, 0, 8)),
            bitmap.Bitmap.checkerboard(dims, 54, (224, 255, 255), (31, 0, 0)),
            bitmap.Bitmap.stripes(dims, 71, 23.4, (255, 224, 255), (0, 15, 0)),
            bitmap.Bitmap.checkerboard(dims, 45, (224, 255, 224), (0, 48, 0)),
            gs.get(dims, 0),
            bitmap.Bitmap.gradient(dims, angle=-25, colour1=(108, 31, 133), colour2=(129, 106, 255)),
            gs.get(dims, 1),
            bitmap.Bitmap.stripes(dims, stripewidth=14, angle=100, colour1=(221, 237, 7), colour2=(7, 96, 192)),
            bitmap.Bitmap.gradient(dims, angle=random.randint(-19, 17),
                                   colour1=(random.randint(96, 158), random.randint(0, 140), random.randint(128, 255)),
                                   colour2=(random.randint(0, 95), random.randint(128, 255), random.randint(0, 101)))
        ]
        return cls(breedPatternFunc=_breedMonogamousRandom, breedPatternParams={"setcount":5},
                   dims=dims, gen0=gen0, genSize=10)


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

    @staticmethod
    def _listMutationReverse(self, pixels):
        """Transcription mutation that reverses the list."""
        return list(pixels.reversed())

    @staticmethod
    def _listMutationRotate(self, pixels, rotation=None):
        """Transcription mutation that bytewise rotates the list."""
        cutoff = random.randint(1, len(pixels) - 2)
        return pixels[cutoff:] + pixels[:cutoff]

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
