"""
Use Pillow to create PNGs that 'match' the original transcription errors of the Bitmap object
"""
import datetime
import os
import random

from imagecrosser import ImageCrosser
from patternedimage import PatternedImage
from shared import shared

if __name__ == '__main__':
    dims = (1440, 1440)

    currentGen = [PatternedImage.new(dims=dims) for i in range(10)]

    now = datetime.datetime.now()
    folder = now.strftime("generations\%Y%m%d_%H%M%S")
    os.mkdir(folder)

    for genID in range(12):
        print("\nWriting generation {}: ".format(genID), end='')
        count = 0
        for img in currentGen:
            print("{}, ".format(count), end='')

            # img.save("{}\gen{}_{}.jpg".format(folder, genID, count))
            img.save("{}\gen{}_{}.png".format(folder, genID, count))
            count += 1

        random.shuffle(currentGen)
        nextGen = []
        for i in range(len(currentGen) // 2):
            nextGen.extend(ImageCrosser.crossWholeArea([currentGen[2 * i], currentGen[2 * i + 1]],
                                                       mutations=[ImageCrosser.mutationTranscription]))
        currentGen = nextGen
