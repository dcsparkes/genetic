"""
Experiment to use Pillow to create JPEGS
"""
import datetime
import os

from patternedimage import PatternedImage
from shared import shared

if __name__ == '__main__':
    dims = (1080, 1080)
    # img = PatternedImage.new(PatternedImage.diamonds, dims=dims, colours=[(209, 123, 193), (123, 193, 209), (12, 19, 29)])
    # img = PatternedImage.new(PatternedImage.stripedMulti, dims=dims, colours=shared.randomRGBContrasting(5))
    # img = PatternedImage.new(PatternedImage.diamonds, dims=dims, colours=shared.randomRGBPair())

    gen0 = [PatternedImage.new(dims=dims) for i in range(50)]

    now = datetime.datetime.now()
    folder = now.strftime("generations\%Y%m%d_%H%M%S")
    os.mkdir(folder)
    genID = 0
    count = 0

    print("\nWriting images: ")
    for img in gen0:
        print("{}, ".format(count), end='')

        # img.save("{}\gen{}_{}.jpg".format(folder, genID, count))
        img.save("{}\gen{}_{}.png".format(folder, genID, count))
        count += 1
