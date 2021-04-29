"""
Create a new generation from a couple of bitmaps.
"""
from bitmap import bitmap, crosser

import datetime
import itertools
import os
import random

def main():
    dims = (540, 540)
    print("Generating generation 0")
    breeder = crosser.CrosserMonogamous(dims=dims)

    now = datetime.datetime.now()
    folder = now.strftime("generations\%Y%m%d_%H%M%S")
    os.mkdir(folder)

    genID = 0
    for generation in breeder:
        count = 0
        print("Writing generation {}: ".format(genID), end='')
        for bmp in generation:
            count += 1
            print("{}, ".format(count), end='')
            bmp.writeBMP("{}\gen{}_{}".format(folder, genID, count))
        genID += 1
        if genID > 23:
            break

    # for genID in range(1, 12):  # 10 images per row, 6 rows per contact sheet
    #     genNext = []
    #     print("\nGenerating generation {} (monogamous): ".format(genID), end='')
    #     random.shuffle(genPrev)
    #     for i in range(5):  # 5 breedings, purely luck
    #         print("{}, ".format(i), end='')
    #         fit = crosser.FullImageTranscriber.multiple(genPrev[2 * i], genPrev[2 * i + 1],
    #                                                     crossoverChance=random.randint(1, 7) / (540 ** 2)
    #                                                     )  # ~1-7 crossovers per pair
    #         genNext.extend(fit.transcribe())
    #
    #     count = 0
    #     print("\nWriting generation 1: ", end='')
    #     for bmp in genNext:
    #         count += 1
    #         print("{}, ".format(count), end='')
    #         bmp.writeBMP("{}\gen{}_{}".format(folder, genID, count))
    #
    #     genNext.extend(random.sample(genPrev, 2))  # select images from previous generation
    #     genNext.append(bitmap.Bitmap.arbitrary(dims))
    #
    #     genPrev = genNext

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
