"""
Create a new generation from a couple of bitmaps.
"""
from bitmap import bitmap
from bitmap import mutator

import itertools
import random

gaussians = [bitmap.Bitmap.gaussian((540, 540), colour=(0, 0, 11), delta=3, terminal=250),
             bitmap.Bitmap.gaussian((540, 540), colour=(255, 255, 244), delta=-3, terminal=2)]


def arbitraryPattern():
    choice = random.randint(0, 9)
    colour1 = (random.randint(0, 127), random.randint(0, 127), random.randint(0, 127))
    colour2 = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
    if choice <= 1:
        return gaussians[choice]
    elif choice <= 3:
        angle1 = random.randint(0, 89)
        angle2 = angle1 + random.randint(15, 104)
        return bitmap.Bitmap.diamonds((540, 540), sizes=(random.randint(3, 63), random.randint(3, 63)),
                                      angles=(angle1, angle2), colour1=colour1, colour2=colour2)
    elif choice <= 5:
        return bitmap.Bitmap.stripes((540, 540), random.randint(5, 175), random.randint(7, 15), colour1, colour2)
    elif choice <= 7:
        return bitmap.Bitmap.checkerboard((540, 540), random.randint(12, 175), colour1, colour2)
    elif choice <= 9:
        bitmap.Bitmap.gradient((540, 540), angle=random.randint(-19, 17), colour1=colour1, colour2=colour2)


def main():
    print("Generating generation 0")
    genPrev = [
        bitmap.Bitmap.diamonds((540, 540), sizes=(16, 16), angles=(10, 70),
                               colour1=(218, 205, 255), colour2=(96, 15, 96)),
        bitmap.Bitmap.stripes((540, 540), random.randint(13, 63), random.randint(7, 15), (255, 255, 128), (96, 0, 8)),
        bitmap.Bitmap.checkerboard((540, 540), 54, (224, 255, 255), (31, 0, 0)),
        bitmap.Bitmap.stripes((540, 540), 71, 23.4, (255, 224, 255), (0, 15, 0)),
        bitmap.Bitmap.checkerboard((540, 540), 45, (224, 255, 224), (0, 48, 0)),
        gaussians[0],
        bitmap.Bitmap.gradient((540, 540), angle=-25, colour1=(108, 31, 133), colour2=(129, 106, 255)),
        gaussians[1],
        bitmap.Bitmap.stripes((540, 540), stripewidth=14, angle=100, colour1=(221, 237, 7), colour2=(7, 96, 192)),
        bitmap.Bitmap.gradient((540, 540), angle=random.randint(-19, 17),
                               colour1=(random.randint(96, 158), random.randint(0, 140), random.randint(128, 255)),
                               colour2=(random.randint(0, 95), random.randint(128, 255), random.randint(0, 101)))
    ]
    genID = 0
    count = 0
    print("Writing generation 0: ", end='')
    for bmp in genPrev:
        count += 1
        print("{}, ".format(count), end='')
        bmp.writeBMP("generations\gen{}_{}".format(genID, count))

    for genID in range(1, 11):
        genNext = []
        print("\nGenerating generation {} (monogamous): ".format(genID), end='')
        random.shuffle(genPrev)
        for i in range(5):  # 5 breedings, purely luck
            print("{}, ".format(i), end='')
            fit = mutator.FullImageTranscriber.multiple(genPrev[2 * i], genPrev[2 * i + 1],
                                                        crossoverChance=random.randint(1, 7) / (540 ** 2)
                                                        )  # ~1-7 crossovers per pair
            genNext.extend(fit.transcribe())

        count = 0
        print("\nWriting generation 1: ", end='')
        for bmp in genNext:
            count += 1
            print("{}, ".format(count), end='')
            bmp.writeBMP("generations\gen{}_{}".format(genID, count))

        genNext.extend(random.sample(genPrev, 2))  # select images from previous generation
        genNext.append(arbitraryPattern())

        genPrev = genNext

    # print("\nDeleting generation 0.", end='')
    # del gen0
    #
    # gen2 = []
    # print("\nGenerating generation 2: ", end='')
    # i = 0
    # for pair in tuple(itertools.combinations(gen1[::3], 2)):
    #     i += 1
    #     print("{}, ".format(i), end='')
    #     fit = mutator.FullImageTranscriber.double(*pair)
    #     gen2.extend(fit.transcribe())
    #
    # print("\nDeleting generation 1.", end='')
    # del gen1
    #
    # i = 0
    # print("\nWriting generation 2: ", end='')
    # for bmp in gen2:
    #     i += 1
    #     print("{}, ".format(i), end='')
    #     bmp.writeBMP("generations\gen2_{}".format(i))
    #
    # gen3 = []
    # print("\nGenerating generation 3: ", end='')
    # i = 0
    # for pair in tuple(itertools.combinations(gen2[::5], 2))[::3]:
    #     i += 1
    #     print("{}, ".format(i), end='')
    #     fit = mutator.FullImageTranscriber.multiple(*pair)
    #     gen3.extend(fit.transcribe())
    #
    # print("\nDeleting generation 2.", end='')
    # del gen2
    #
    # i = 0
    # print("\nWriting generation 3: ", end='')
    # for bmp in gen3:
    #     i += 1
    #     print("{}, ".format(i), end='')
    #     bmp.writeBMP("generations\gen3_{}".format(i))


if __name__ == '__main__':
    main()
