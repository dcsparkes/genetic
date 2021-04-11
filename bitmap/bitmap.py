import math


def clipValue(value, lower=0, upper=255):
    """
    Limits input 'value' between minimum and maximum (inclusive) limits.

    :param value: input
    :param lower: lower bound
    :param upper: upper bound
    :return: value clipped to be within range.
    """
    return max(min(value, upper), lower)


def unitVector(direction):
    """
    Calculate the unit vector: 0 = increasing x (or real), 90 = increasing y (or complex)
    Questionable whether it should operate in degrees or radians or some hybrid (e.g. ints=degrees, floats=radians)
    For now everything is in degrees.
    Direction can take a number of forms:
        Numbers (int, float) = angle
        tuple, list, (iterable) = vector
        Complex = 2D vector: treat accordingly
    :param angle:
    :return: tuple of coefficients (float)
    """
    if type(direction) is tuple or type(direction) is list:
        length = _vectorLength(direction)
        return [c / length for c in direction]
    elif type(direction) is int or type(direction) is float:  # Number is angle in degrees
        rad = math.radians(direction)
        return (math.cos(rad), math.sin(rad))
    elif type(direction) is complex:
        return unitVector((direction.real, direction.imag))
    # Check iterable?: https://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-an-object-is-iterable
    return None


def _dotProduct(v1, v2):
    """
    Dot product of two vectors is the sum of the product of the corresponding cartesian coordinates
    :param v1:
    :param v2:
    :return:
    """
    return sum([a * b for a, b in zip(v1, v2)])


def _vectorAngle(v1, v2):
    """
    Calculate angle between two vectors.
    :param v1:
    :param v2:
    :return:
    """
    return math.degrees(math.acos(_dotProduct(v1, v2) / (_vectorLength(v1) * _vectorLength(v2))))


def _vectorLength(v):
    """
    Calculate length of vector using Pythagorus.
    :param v: vector (iterable)
    :return:
    """
    if type(v) is complex:
        return _vectorLength((v.real, v.imag))
    return math.sqrt(sum([i ** 2 for i in v]))


def _radialIntersection(dims, angle):
    """
    :param dims: image dimensions as tuple
    :param angle: 0 = +ve x-axis. 90 = +ve y-axis
    :return: intersection point with a frame of a line drawn from the centre point at the given angle.
    """
    theta = angle % 360
    xdim, ydim = dims
    xmax = xdim - 1
    ymax = ydim - 1
    x = None
    y = None
    if 0 < theta < 180:  # angle uppish, intersection top half
        rads = math.radians(theta - 90)
        x = round((xmax - math.tan(rads) * ymax) / 2)
        if 0 <= x <= xmax:
            return (x, ymax)
    elif 180 < theta:  # angle downish, origin bottom half
        rads = math.radians(theta - 270)
        x = round((xmax + math.tan(rads) * ymax) / 2)
        if 0 <= x <= xmax:
            return (x, 0)

    if 90 < theta < 270:  # angle leftish, origin right half
        rads = math.radians(theta - 180)
        y = round((ymax - math.tan(rads) * xmax) / 2)
        if 0 <= y <= ymax:
            return (0, y)
    elif 270 < theta or theta < 90:  # angle rightish, origin left half
        rads = math.radians((theta + 90) % 360 - 90)
        y = round((ymax + math.tan(rads) * xmax) / 2)
        if 0 <= y <= ymax:
            return (xmax, y)


# def _origin(dims, angle):
#     """
#     :param dims: image dimensions as tuple
#     :param angle: 0 = +ve x-axis. 90 = +ve y-axis
#     :return:    intersection point with a frame of a line drawn from the centre point in the opposite direction.
#                 Probably should rewrite function to just be an intersection calculator and then _call_ it with 180
#                 degree shifted angle to find the 'origin'.
#     """
#     theta = angle % 360
#     xdim, ydim = dims
#     xmax = xdim - 1
#     ymax = ydim - 1
#     x = None
#     y = None
#
#     if 0 < theta < 180:  # angle uppish, origin bottom half
#         rads = math.radians(theta - 90)
#         x = round((xmax + math.tan(rads) * ymax) / 2)
#         if 0 <= x <= xmax:
#             return (x, 0)
#     elif 180 < theta:  # angle downish, origin top half
#         rads = math.radians(theta - 270)
#         x = round((xmax - math.tan(rads) * ymax) / 2)
#         if 0 <= x <= xmax:
#             return (x, ymax)
#
#     if 90 < theta < 270:  # angle leftish, origin right half
#         rads = math.radians(theta - 180)
#         y = round((ymax + math.tan(rads) * xmax) / 2)
#         if 0 <= y <= ymax:
#             return (xmax, y)
#
#     elif 270 < theta or theta < 90:  # angle rightish, origin left half
#         rads = math.radians((theta + 90) % 360 - 90)
#         y = round((ymax - math.tan(rads) * xmax) / 2)
#         if 0 <= y <= ymax:
#             return (0, y)
#     ### Old code where north = +ve y, east = +ve x
#     # if 0 < theta < 180:  # angle uppish, origin left half
#     #     rads = math.radians(theta - 90)
#     #     y = round((ymax + math.tan(rads) * xmax) / 2)
#     #     if 0 <= y <= ymax:
#     #         return (0, y)
#     # elif 180 < theta:  # angle leftish, origin right half
#     #     rads = math.radians(theta - 270)
#     #     y = round((ymax - math.tan(rads) * xmax) / 2)
#     #     if 0 <= y <= ymax:
#     #         return (xmax, y)
#     #
#     # if 90 < theta < 270:  # angle bottomish, origin top half
#     #     rads = math.radians(theta - 180)
#     #     x = round((xmax + math.tan(rads) * ymax) / 2)
#     #     if 0 <= x <= xmax:
#     #         return (x, ymax)
#     #
#     # elif 270 < theta or theta < 90:  # angle uppish, origin bottom half
#     #     rads = math.radians((theta + 90) % 360 - 90)
#     #     x = round((xmax - math.tan(rads) * ymax) / 2)
#     #     if 0 <= x <= xmax:
#     #         return (x, 0)
#     #
#     # # This should never happen!
#     # print ("_origin fell through")  # Implement logging, you muppet!
#     # return _originUnsophisticated(dims, angle)

# def _originUnsophisticated(dims, angle):
#     theta = angle % 360
#     if theta < 180:
#         x = dims[0] - 1
#     else:
#         x = 0
#     if 90 <= theta < 270:
#         y = 0
#     else:
#         y = dims[1] - 1
#     return (x, y)


# Set of pattern functions
def _patternBlank(dims, colour):
    x, y = dims
    if not colour:
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


def _patternGradientFillHorizontal(dims, colour1=0, colour2=255):
    pixels = []
    x, y = dims

    colourStart = Pixel(colour1).rgb
    colourEnd = Pixel(colour2).rgb

    for j in range(y):
        pixels.append([])
    for i in range(x):
        colour = _rgbBlend(colourStart, colourEnd, i / x)
        for row in pixels:
            row.append(Pixel(colour))
    return pixels


def _patternGradientFillVertical(dims, colour1=0, colour2=255):
    pixels = []
    x, y = dims

    colourStart = Pixel(colour1).rgb
    colourEnd = Pixel(colour2).rgb

    for j in range(y):
        colour = _rgbBlend(colourStart, colourEnd, j / y)
        pixels.append([])
        for i in range(x):
            pixels[-1].append(Pixel(colour))
    return pixels


def _patternStripe(dims, stripewidth, angle=0, colour1=0, colour2=255, interpolated=True):
    pixels = []
    vUnit = unitVector(angle)
    origin = _radialIntersection(dims, angle - 180)

    x, y = dims
    for j in range(y):
        pixels.append([])
        for i in range(x):
            if ((i % (2 * checksize)) >= checksize) ^ ((j % (2 * checksize)) >= checksize):
                pixels[-1].append(Pixel(colour1))
            else:
                pixels[-1].append(Pixel(colour2))
    return pixels


def _rgbBlend(c1, c2, proportion):
    """
    Blend with proportion: 0.0 = pure colour1, 1.0 = pure colour2
    :param c1: colour1
    :param c2: colour2
    :return: blended colour
    """
    prop = clipValue(proportion, lower=0.0, upper=1.0)
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


def _rgbBlend2(cs, proportions):
    """
    Blend with proportion: 0.0 = pure colour1, 1.0 = pure colour2
    :param c1: colour1
    :param c2: colour2
    :return: blended colour
    """
    prop = clipValue(proportion, lower=0.0, upper=1.0)
    return tuple([round(a * (1 - prop) + b * prop) for a, b in zip(c1, c2)])


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
        return (clipValue(value),) * 3

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
        return tuple([clipValue(v) for v in (tuple(values) + (0, 0, 0))[:3]])

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
        shift = 0
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
            msg = "Unsupported byte length: '{}'.".format(length)
            raise ValueError(msg)

        retVal = 0
        for c in components:
            retVal <<= shift
            retVal += c

        return retVal.to_bytes(length, byteorder=byteorder)


class Bitmap:
    """
    http://www.ece.ualberta.ca/~elliott/ee552/studentAppNotes/2003_w/misc/bmp_file_format/bmp_file_format.htm

    Each scan line is zero padded to the nearest 4-byte boundary. If the image has a width that is not divisible by
    four, say, 21 bytes, there would be 3 bytes of padding at the end of every scan line.

    Scan lines are stored bottom to top instead of top to bottom.

    RGB values are stored backwards i.e. BGR.
    """

    def __init__(self, dims, pixels=None, fillFunc=_patternBlank, fillParameters=None):
        """
        :param dims: tuple of (x, y) dimensions in pixels
        :param pixels: list of pixels, None for self-generated
        :param colours:
        :param fillFunc: function to genearate fill pattern.
        """
        if pixels:
            if type(pixels[0][0]) is Pixel:
                self.pixels = pixels
            else:
                raise ValueError("pixels parameter requires 2D iterable of Pixels.")
        elif fillParameters is None:
            self.pixels = fillFunc(dims, colour=255)
        else:
            self.pixels = fillFunc(dims, **fillParameters)
            # x, y = dims
            # self.pixels = [[(0).to_bytes(res // 8, byteorder='little')] * x for i in range(y)]

        self.dims = dims

    @classmethod
    def fromFile(cls, fileName):
        # read file, and fill bitmap object from the data
        dims = None
        res = None
        pixels = None
        return cls(dims, res, pixels)

    @classmethod
    def blank(cls, dims, colour=(255, 255, 255)):
        fillParameters = {"colour": colour}
        return cls(dims, fillFunc=_patternBlank, fillParameters=fillParameters)

    @classmethod
    def checkerboard(cls, dims, checksize, colour1=(0, 0, 0), colour2=(255, 255, 255)):
        fillParameters = {"checksize": checksize, "colour1": colour1, "colour2": colour2}
        return cls(dims, fillFunc=_patternCheckerboard, fillParameters=fillParameters)

    @classmethod
    def gradient(cls, dims, angle=0, colour1=(255, 255, 255), colour2=(0, 0, 0)):
        if not angle % 180:
            func = _patternGradientFillVertical
            if angle % 360:
                colourA = colour2
                colourB = colour1
            else:
                colourA = colour1
                colourB = colour2
        elif not angle % 90:
            func = _patternGradientFillHorizontal
            if angle % 270:
                colourA = colour1
                colourB = colour2
            else:
                colourA = colour2
                colourB = colour1
        fillParameters = {"colour1": colourA, "colour2": colourB}
        return cls(dims, fillFunc=func, fillParameters=fillParameters)

    def createHeader(self, fileSize, reserved=0, offset=54):
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
