"""
Experiment to use Pillow to create JPEGS
"""
import datetime
import os

from patternedimage import PatternedImage

if __name__ == '__main__':
    dims = (1080, 1080)
    img = PatternedImage.Striped(dims=dims, colours=[(209, 123, 193), (123, 193, 209), (12, 19, 29)])

    pixels = img.load()
    now = datetime.datetime.now( )
    folder = now.strftime("generations\%Y%m%d_%H%M%S")
    os.mkdir(folder)
    genID = 0
    count = 0

    img.show()

    # img.save("{}\gen{}_{}.jpg".format(folder, genID, count))
