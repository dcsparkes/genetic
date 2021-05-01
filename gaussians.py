"""
Experiment to use Pillow to create Gaussians and help populate the stored distributions
"""

from patternedimage import PatternedImage
from shared import shared

if __name__ == '__main__':
    dims = (1080, 1080)
    img = PatternedImage.new(PatternedImage.gaussian, dims=dims, colours=[(0, 0, 0), (255, 255, 255), (0, 0, 0)]) # shared.randomRGBContrasting(2)) #  [(209, 123, 193), (123, 193, 209)])
    img.show()

