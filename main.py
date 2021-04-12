"""
Create a new generation from a couple of bitmaps.
"""
from bitmap import bitmap
from bitmap import mutator

import itertools


def main():
    print("Generating generation 0")
    gen0 = [
        bitmap.Bitmap.stripes((540, 405), 38, 13, (255, 255, 128), (96, 0, 8)),
        bitmap.Bitmap.checkerboard((540, 540), 54, (224, 255, 255), (31, 0, 0)),
        bitmap.Bitmap.stripes((540, 540), 71, 23, (255, 224, 255), (0, 15, 0)),
        bitmap.Bitmap.checkerboard((405, 540), 45, (224, 255, 224), (0, 48, 0)),
        bitmap.Bitmap.gaussian((405, 405), colour=(10, 10, 10), delta=3, terminal=250),
        bitmap.Bitmap.gradient((540, 540), angle=-25, colour1=(108, 31, 133), colour2=(129, 106, 255))
    ]
    i = 0
    print("Writing generation 0: ", end='')
    for bmp in gen0:
        i += 1
        print("{}, ".format(i), end='')
        bmp.writeBMP("generations\gen0_{}".format(i))

    gen1 = []
    print("\nGenerating generation 1: ", end='')
    i = 0
    for pair in itertools.combinations(gen0, 2):
        i += 1
        print("{}, ".format(i), end='')
        fit = mutator.FullImageTranscriber.single(*pair)
        gen1.extend(fit.transcribe())

    i = 0
    print("\nWriting generation 1: ", end='')
    for bmp in gen1:
        i += 1
        print("{}, ".format(i), end='')
        bmp.writeBMP("generations\gen1_{}".format(i))

    print("\nDeleting generation 0.", end='')
    del gen0

    gen2 = []
    print("\nGenerating generation 2: ", end='')
    i = 0
    for pair in tuple(itertools.combinations(gen1[::3], 2))[::3]:
        i += 1
        print("{}, ".format(i), end='')
        fit = mutator.FullImageTranscriber.double(*pair)
        gen2.extend(fit.transcribe())

    print("\nDeleting generation 1.", end='')
    del gen1

    i = 0
    print("\nWriting generation 2: ", end='')
    for bmp in gen2:
        i += 1
        print("{}, ".format(i), end='')
        bmp.writeBMP("generations\gen2_{}".format(i))

    gen3 = []
    print("\nGenerating generation 3: ", end='')
    i = 0
    for pair in tuple(itertools.combinations(gen2[::5], 2))[::3]:
        i += 1
        print("{}, ".format(i), end='')
        fit = mutator.FullImageTranscriber.multiple(*pair)
        gen3.extend(fit.transcribe())

    print("\nDeleting generation 2.", end='')
    del gen2

    i = 0
    print("\nWriting generation 3: ", end='')
    for bmp in gen3:
        i += 1
        print("{}, ".format(i), end='')
        bmp.writeBMP("generations\gen3_{}".format(i))


if __name__ == '__main__':
    main()
