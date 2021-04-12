"""
Shared helper functions
"""
from shared import shared
from vector import vector
import random


# Set of pattern functions
def _patternBlank(dims, colour=None):
    x, y = dims
    if colour is None:
        colour = 255  # default = white
    return [[Pixel(colour) for j in range(x)] for i in range(y)]


def _patternCheckerboard(dims, checksize, colour1=0, colour2=255):
    pixels = []
    x, y = dims
    for j in range(y):
        pixels.append([])
        for i in range(x):
            if ((i % (2 * checksize)) >= checksize) ^ ((j % (2 * checksize)) >= checksize):
                pixels[-1].append(Pixel(colour1))
            else:
                pixels[-1].append(Pixel(colour2))
    return pixels


def _diamondSizes(sizeInfo):
    """
    Calculate the sizes for the tessellated parallelogram pattern.  Default to equidistant if second size is not
    provided.

    :param sizeInfo: size information
    :return: tuple pair of sizes.
    """
    sizes = []

    if type(sizeInfo) is int or type(sizeInfo) is float:
        sizes.append(sizeInfo)
    elif sizeInfo is not None:
        sizes = sizeInfo[:2]

    if not len(sizes):
        sizes.append(7)  # arbitrary magic number
    if len(sizes) == 1:
        sizes.append(sizes[0])
    return sizes


def _diamondVectors(angleInfo):
    """
    Calculate the unit vectors for the tessellated parallelogram pattern.  Default to orthogonal if second angle is not
    provided.

    :param angleInfo: angle information
    :return: tuple pair of 2D Vectors.
    """
    angs = []

    if type(angleInfo) is int or type(angleInfo) is float:
        angs.append(angleInfo)
    elif angleInfo is not None:
        angs = angleInfo[:2]

    if not len(angs):
        angs.append(0)
    if len(angs) == 1:
        angs.append(angs[0] + 90)
    return [vector.Vector2D.unit(a) for a in angs]


def _patternDiamonds(dims, angles=None, sizes=None, colour1=(0, 0, 0), colour2=(255, 255, 255)):
    pixels = []
    vUnitH, vUnitV = _diamondVectors(angles)
    sizeH, sizeV = _diamondSizes(sizes)
    vOrigin = vector.Vector(vector.radialIntersection(dims, vUnitH.phaseAngle()))

    x, y = dims
    for n in range(y):
        pixels.append([])
        for m in range(x):
            vPosition = vector.Vector2D([m, n]) - vOrigin

            distanceAlongHorizontal = vector.dotProduct(vPosition, vUnitH)
            distanceAlongVertical = vector.dotProduct(vPosition, vUnitV)
            distThroughPatternHorizontal = distanceAlongHorizontal % (2 * sizeH)
            distThroughPatternVertical = distanceAlongVertical % (2 * sizeV)

            if (distThroughPatternHorizontal < sizeH) ^ (distThroughPatternVertical >= sizeV):
                baseColour = colour1
                mixColour = colour2
            else:
                baseColour = colour2
                mixColour = colour1

            mixRateH = [1]
            if distThroughPatternHorizontal < 1:
                mixRateH = [1 - distThroughPatternHorizontal, distThroughPatternHorizontal]
            elif sizeH < distThroughPatternHorizontal < sizeH + 1:
                distIntoNextColour = distThroughPatternHorizontal - sizeH
                mixRateH = [1 - distIntoNextColour, distIntoNextColour]

            mixRateV = [1]
            if distThroughPatternVertical < 1:
                mixRateV = [1 - distThroughPatternVertical, distThroughPatternVertical]
            elif sizeV < distThroughPatternVertical < sizeV + 1:
                distIntoNextColour = distThroughPatternVertical - sizeV
                mixRateV = [1 - distIntoNextColour, distIntoNextColour]

            # First implementation : Mix proportions as if diamonds are square: this might make points ill-defined!
            # Probably should add some kind of cos theta element.
            proportions = [pH * pV for pH in mixRateH for pV in mixRateV]

            # print("{} = {}".format(proportions, sum(proportions)))
            if len(proportions) == 1:
                c = baseColour
            if len(proportions) == 2:
                c = _rgbBlend(baseColour, mixColour, proportions[0])
            if len(proportions) == 4:
                c = _rgbBlend(baseColour, mixColour, proportions[0] + proportions[3])
            pixels[-1].append(Pixel(c))
    return pixels


def _patternDiamonds2(dims, angles=(0, 90), sizes=(7, 7), colour1=(0, 0, 0), colour2=(255, 255, 255)):
    p = Pixel(1)
    stripeDensities = [[p.rgb[0] for row in _patternStripe(dims, stripewidth=sizes[i], angle=angles[i],
                                                           colour1=(0, 0, 0), colour2=(255, 255, 255))
                        for p in row] for i in range(2)]

    pixels = [Pixel(_rgbBlend(colour1, colour2, abs(a - b) / 255)) for a, b in zip(*stripeDensities)]

    rows = []
    while pixels:
        row = pixels[:dims[0]]
        rows.append(row)
        pixels = pixels[dims[0]:]
    return rows


def _patternGaussian(dims, colour=(0, 0, 0), mus=None, sigmas=None, delta=1, terminal=255):
    xmax, ymax = dims
    if mus:
        xmu, ymu = mus
    else:
        xmu = xmax / 2
        ymu = ymax / 2

    if sigmas:
        xsigma, ysigma = mus
    else:
        xsigma = xmax / 4
        ysigma = ymax / 4

    terminal = shared.clipValue(terminal)

    pixelColours = [[list(Pixel(colour).rgb) for j in range(xmax)] for i in range(ymax)]

    terminalReached = not delta  # if delta == 0, don't start the loop
    colourIndex = 0
    while not terminalReached or colourIndex:
        # for i in range(9000000):
        x = round(random.gauss(xmu, xsigma))
        y = round(random.gauss(ymu, ysigma))
        if 0 <= x < xmax and 0 <= y < ymax:
            newValue = shared.clipValue(pixelColours[y][x][colourIndex] + delta)
            pixelColours[y][x][colourIndex] = newValue
            # if (delta > 0 and channel >= terminal) or (delta < 0 and channel <= terminal):
            if (terminal - newValue) * delta <= 0:  # newValue lies beyond the terminal
                # print("Terminal reached, iteration({})".format(i))
                terminalReached = True
        colourIndex = (colourIndex + 1) % 3  # cycle through RGB

    return [[Pixel(colour) for colour in row] for row in pixelColours]


def _patternGradient(dims, angle=45, colour1=0, colour2=255):
    pixels = []
    vUnit = vector.Vector2D.unit(angle)
    vOrigin = vector.Vector(vector.radialIntersection(dims, angle - 180))
    vTerminus = vector.Vector(vector.radialIntersection(dims, angle))
    distanceTotal = (vTerminus - vOrigin).magnitude()

    x, y = dims
    for n in range(y):
        pixels.append([])
        for m in range(x):
            vPosition = vector.Vector2D([m, n]) - vOrigin
            distanceAlongDirection = vector.dotProduct(vPosition, vUnit)
            colour = _rgbBlend(colour1, colour2, distanceAlongDirection / distanceTotal)
            pixels[-1].append(Pixel(colour))
    return pixels


def _patternStripe(dims, stripewidth, angle=45, colour1=0, colour2=255, interpolated=True):
    pixels = []
    vUnit = vector.Vector2D.unit(angle)
    vOrigin = vector.Vector(vector.radialIntersection(dims, angle - 180))
    # print("{}: {}".format(vUnit, vOrigin))

    x, y = dims
    for n in range(y):
        pixels.append([])
        for m in range(x):
            vPosition = vector.Vector2D([m, n]) - vOrigin
            distanceAlongDirection = vector.dotProduct(vPosition, vUnit)
            distancethroughPattern = distanceAlongDirection % (2 * stripewidth)
            if interpolated and distancethroughPattern < 1:
                c = _rgbBlend(colour2, colour1, distancethroughPattern)
            elif interpolated and stripewidth - 1 < distancethroughPattern < stripewidth:
                c = _rgbBlend(colour2, colour1, stripewidth - distancethroughPattern)
            elif distancethroughPattern >= stripewidth:
                c = colour2
            else:
                c = colour1
            pixels[-1].append(Pixel(c))
    return pixels


def _patternStripeHorizontal(dims, stripewidth, colour1=(0, 0, 0), colour2=(255, 255, 255)):
    xmax, ymax = dims
    pixels = []
    for n in range(ymax):
        pixels.append([])
        distancethroughPattern = n % (stripewidth * 2)
        if distancethroughPattern < 1:
            c = _rgbBlend(colour1, colour2, distancethroughPattern)
        elif stripewidth - 1 < distancethroughPattern < stripewidth:
            c = _rgbBlend(colour2, colour1, distancethroughPattern + 1 - stripewidth)
        elif distancethroughPattern >= stripewidth:
            c = colour2
        else:
            c = colour1
        print("row: {}, colour:{}".format(n, c))
        for m in range(xmax):
            pixels[-1].append(Pixel(c))
    return pixels


def _patternStripeVertical(dims, stripewidth, colour1=(0, 0, 0), colour2=(255, 255, 255)):
    xmax, ymax = dims
    return list(zip(*_patternStripeHorizontal((ymax, xmax), stripewidth, colour1=colour1, colour2=colour2)))


def _rgbBlend(c1, c2, proportion):
    """
    Blend with proportion: 0.0 = pure colour1, 1.0 = pure colour2
    :param c1: colour1
    :param c2: colour2
    :return: blended colour
    """
    prop = shared.clipValue(proportion, lower=0.0, upper=1.0)
    return tuple([round(a * (1 - prop) + b * prop) for a, b in zip(c1, c2)])


def _normaliseProportions(proportionss, count=2):
    props = tuple(proportionss[:count])
    total = sum(props)
    icount = len(props)
    if count > icount:
        remainder = max(0, (1 - total) / (count - icount))
        props = tuple(props) + (remainder,) * (count - icount)
        total = sum(props)  # recalculate total, should be >= 1

    return [p / total for p in props]


# def _rgbBlend2(cs, proportions):
#     """
#     Blend with proportion: 0.0 = pure colour1, 1.0 = pure colour2
#     :param c1: colour1
#     :param c2: colour2
#     :return: blended colour
#     """
#     prop = shared.clipValue(proportion, lower=0.0, upper=1.0)
#     return tuple([round(a * (1 - prop) + b * prop) for a, b in zip(c1, c2)])


class Bitmap:
    """
    http://www.ece.ualberta.ca/~elliott/ee552/studentAppNotes/2003_w/misc/bmp_file_format/bmp_file_format.htm

    Each scan line is zero padded to the nearest 4-byte boundary. If the image has a width that is not divisible by
    four, say, 21 bytes, there would be 3 bytes of padding at the end of every scan line.

    Scan lines are stored bottom to top instead of top to bottom.

    RGB values are stored backwards i.e. BGR.
    """

    def __init__(self, dims, pixels=None, fillFunc=None, fillParameters=None):
        """
        :param dims: tuple of (x, y) dimensions in pixels.
        :param pixels: list of pixels, None for self-generated.
        :param fillFunc: selected function to generate fill pattern.
        :param fillParameters: parameters for the fill function.
        """
        if pixels:
            if type(pixels[0][0]) is Pixel:
                self.pixels = pixels
            else:
                raise ValueError("pixels parameter requires 2D iterable of Pixels.")
        elif fillFunc is None:
            self.pixels = _patternBlank(dims)
        elif fillParameters is None:
            self.pixels = fillFunc(dims)
        else:
            self.pixels = fillFunc(dims, **fillParameters)
            # x, y = dims
            # self.pixels = [[(0).to_bytes(res // 8, byteorder='little')] * x for i in range(y)]

        self.dims = dims

    @classmethod
    def fromFile(cls, fileName):
        """
        Read a bitmap from file.  Not yet implemented.
        :param fileName:
        :return:
        """
        # read file, and fill bitmap object from the data
        dims = None
        res = None
        pixels = None
        return NotImplemented
        # return cls(dims, res, pixels)

    @classmethod
    def blank(cls, dims, colour=(255, 255, 255)):
        """Monotone 'pattern'."""
        fillParameters = {"colour": colour}
        return cls(dims, fillFunc=_patternBlank, fillParameters=fillParameters)

    @classmethod
    def checkerboard(cls, dims, checksize, colour1=(0, 0, 0), colour2=(255, 255, 255)):
        """Checkerboard pattern with variable square size and colours."""
        fillParameters = {"checksize": checksize, "colour1": colour1, "colour2": colour2}
        return cls(dims, fillFunc=_patternCheckerboard, fillParameters=fillParameters)

    @classmethod
    def diamonds(cls, dims, angles=(0, 90), sizes=(7, 7), colour1=(0, 0, 0), colour2=(255, 255, 255)):
        """Checkerboard pattern with variable square size and colours."""
        fillParameters = {"angles": angles, "sizes": sizes, "colour1": colour1, "colour2": colour2}
        return cls(dims, fillFunc=_patternDiamonds, fillParameters=fillParameters)

    @classmethod
    def diamonds2(cls, dims, angles=(0, 90), sizes=(7, 7), colour1=(0, 0, 0), colour2=(255, 255, 255)):
        """Checkerboard pattern with variable square size and colours."""
        fillParameters = {"angles": angles, "sizes": sizes, "colour1": colour1, "colour2": colour2}
        return cls(dims, fillFunc=_patternDiamonds2, fillParameters=fillParameters)

    @classmethod
    def gaussian(cls, dims, colour=(0, 0, 0), mus=None, sigmas=None, delta=1, terminal=255):
        fillParameters = {"colour": colour, "delta": delta, "mus": mus, "sigmas": sigmas, "terminal": terminal}
        return cls(dims, fillFunc=_patternGaussian, fillParameters=fillParameters)

    @classmethod
    def gradient(cls, dims, angle=0, colour1=(255, 255, 255), colour2=(0, 0, 0)):
        fillParameters = {"angle": angle, "colour1": colour1, "colour2": colour2}
        return cls(dims, fillFunc=_patternGradient, fillParameters=fillParameters)

    @classmethod
    def stripes(cls, dims, angle=45, stripewidth=4, colour1=(255, 255, 255), colour2=(0, 0, 0), interpolated=True):
        fillParameters = {"colour1": colour1, "colour2": colour2, "angle": angle, "interpolated": interpolated,
                          "stripewidth": stripewidth}
        return cls(dims, fillFunc=_patternStripe, fillParameters=fillParameters)

    @staticmethod
    def createHeader(fileSize, reserved=0, offset=54):
        """
        Create a BMP header (14 bytes):
            signature - 2 bytes: "BM" in ASCII
            fileSize - 4 bytes: File size in bytes - seems to be byte-reversed
            reserved - 4 bytes: 0 - can id app
            dataOffset - 4 bytes - Offset from beginning of file to the beginning of the bitmap data
        :return:
        """
        bSignature = bytes("BM", 'ascii')  # "BM" in ASCII
        bFileSize = fileSize.to_bytes(4, byteorder='little')
        bReserved = (0).to_bytes(4, byteorder='little')
        bDataOffset = offset.to_bytes(4, byteorder='little')

        return bSignature + bFileSize + bReserved + bDataOffset

    def createInfoHeader(self, res=24, offset=54, ppm=250):
        """
        Create a BMP info header. (40 bytes)
        size - 4 bytes: Size of InfoHeader (=40)
        width - 4 bytes: Horizontal width of bitmap in pixels
        height - 4 bytes: Vertical height of bitmap in pixels
        planes      - 2 bytes: Number of Planes (=1)
        bitsPerPixel - 2 bytes - Bits per Pixel used to store palette entry information. This also identifies in an
                indirect way the number of possible colors. Possible values are:
                                1 = monochrome palette. NumColors = 1
                                4 = 4bit palletized. NumColors = 16
                                8 = 8bit palletized. NumColors = 256
                                16 = 16bit RGB. NumColors = 65536
                                24 = 24bit RGB. NumColors = 16M
        compression	- 4 bytes - Type of Compression:
                                0 = BI_RGB   no compression
                                1 = BI_RLE8 8bit RLE encoding
                                2 = BI_RLE4 4bit RLE encoding
        ImageSize   - 4 bytes (compressed) Size of Image.  It is valid to set this =0 if Compression =0
        XpixelsPerM	- 4 bytes	horizontal resolution: Pixels/meter
        YpixelsPerM - 4 bytes	vertical resolution: Pixels/meter
        Colors Used - 4 bytes   Number of actually used colors. For a 8-bit / pixel bitmap this will be 100h or 256.
        Important Colors	4 bytes	0032h	Number of important colors: 0 = all

        :return: valid header in bytes.
        """

        header = (40).to_bytes(4, byteorder='little')  # size
        bWidth, bHeight = [i.to_bytes(4, byteorder='little') for i in self.dims]
        header += bWidth + bHeight
        header += (1).to_bytes(2, byteorder='little')  # planes
        header += res.to_bytes(2, byteorder='little')  # bitsPerPixel
        header += (0).to_bytes(4, byteorder='little')  # compression not supported
        header += (0).to_bytes(4, byteorder='little')  # compression not supported: imagesize irrelevant
        header += ppm.to_bytes(4, byteorder='little')  # XpixelsPerM: use magic number?
        header += ppm.to_bytes(4, byteorder='little')  # YpixelsPerM: use magic number?
        header += (2 ** res).to_bytes(4, byteorder='little')  # colors used... appears to be big byte order?
        header += (0).to_bytes(4, byteorder='little')  # Important Colors = all

        return header

    def writeBMP(self, filename, res=24):
        """
        Each scan line is zero padded to the nearest 4-byte boundary. If the image has a width that is not divisible by
        four, say, 21 bytes, there would be 3 bytes of padding at the end of every scan line.

        :return:
        """

        if res not in [16, 24]:
            msg = "Invalid resolution: {}".format(res)
            raise ValueError(msg)

        lineBytes = (self.dims[0] * res) // 8  # line size = pixels * bits per pixel
        paddingSize = -lineBytes % 4
        imageStorageSize = (lineBytes + paddingSize) * self.dims[1]  # Storage size = line size (bytes) * no. of lines
        headerSize = 14 + 40
        fileSize = headerSize + imageStorageSize
        fileHeader = self.createHeader(fileSize)
        infoHeader = self.createInfoHeader(res)

        paddingBytes = (0).to_bytes(1, 'little') * paddingSize

        with open('{}.bmp'.format(filename), 'wb') as bmp:
            bmp.write(fileHeader)
            bmp.write(infoHeader)
            for line in self.pixels:
                for pixel in line:
                    bmp.write(pixel.to_bytes(res // 8, 'little'))
                bmp.write(paddingBytes)

    def writeJPEG(self, filename):
        pass


class Pixel:
    """
    Representation of a pixel as 24 bit RGB (for now).
    Intent is to decouple pixel from resolution and encapsulate the colour conversions and bitwise crossover.
    Resolution only matters when reading from an existing image or at writeBMP stage.
    """

    def __init__(self, colour=None, res=24):
        """
        Convert i

        :param colour:
        :param res: resolution of input colour, to allow scaling to 24 bit, if necessary
        """
        # self.rgb = None
        self._paint(colour, res)

    def __repr__(self):
        return "{}(colour={})".format(self.__class__.__name__, self.rgb)

    def __str__(self):
        return self.rgb

    @staticmethod
    def _constructTupleFromNumber(value):
        """
        Take a single value and convert it into a 3-dimensional tone.  For YUV this would correspond to Y, while UV
        would be zero.  For RGB assume all components are equal.
        :param value:
        :return:
        """
        return (shared.clipValue(value),) * 3

    @staticmethod
    def _validateTuple(values):
        """
        Construct a valid 24-bit tuple from an existing tuple.  If the tuple is longer then 3 values, assume the
        subsequent values are irrelevant (alpha channel for instance).

        If the tuple is truncated, make the assumption that non-provided values are zero.  This might be better served
        with an exception, particularly for RGB.  With other colour models it might make sense (YUV for instance).  On
        the other hand pseudo-random outcomes are not exactly beyond the project brief.

        :param values: tuple of values, ideally (R, B, G)
        :return: tuple of values (R, B, G)
        """
        return tuple([shared.clipValue(v) for v in (tuple(values) + (0, 0, 0))[:3]])

    def _paint(self, colour, res=24):
        if colour is None:
            colour = 255  # Default is white?

        if type(colour) is int or type(colour) is float:
            colour = int(colour)
            if res == 16:
                colour <<= 3
            self.rgb = self._constructTupleFromNumber(colour)

        elif type(colour) is tuple or type(colour) is list:
            self.rgb = self._validateTuple(colour)

        else:  # notable omissions are 'colours' of types bytes or bytearray, which may be particularly useful.
            msg = "Color '{}' of type '{}' not supported.".format(colour, type(colour))
            raise TypeError(msg)

    def to_bytes(self, length, byteorder):
        """
        Convert the internal value into bits.

        :param length: 2 = 16 bit, 3 = 24 bit
        :param byteorder: in this context: 'big' = RGB, 'little' = BGR
        :return:
        """
        components = []

        if byteorder not in ['little', 'big']:
            msg = "Unrecognised byteorder: '{}'.".format(byteorder)
            raise ValueError(msg)

        if length == 2:  # 16-bit
            if byteorder == 'little':
                components = [x >> 3 for x in self.rgb]
            elif byteorder == 'big':
                components = [x >> 3 for x in self.rgb[::-1]]
            shift = 5

        elif length == 3:  # 24-bit
            components = self.rgb[:]
            shift = 8
        else:
            msg = "Unsupported byte magnitude: '{}'.".format(length)
            raise ValueError(msg)

        retVal = 0
        for c in components:
            retVal <<= shift
            retVal += c

        return retVal.to_bytes(length, byteorder=byteorder)
