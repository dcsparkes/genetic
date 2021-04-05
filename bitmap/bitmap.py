def clipValue(value, lower=0, upper=255):
    """
    Limits input 'value' between minimum and maximum (inclusive) limits.

    :param value: input
    :param lower: lower bound
    :param upper: upper bound
    :return: value clipped to be within range.
    """
    return max(min(value, upper), lower)


# Set of pattern functions
def _patternBlank(dims, colours):
    x, y = dims
    if colours:
        colour = colours[0]
    else:
        colour = 255  # default = white
    return [[Pixel(colour) for j in range(x)] for i in range(y)]


class Pixel:
    """
    Representation of a pixel as 24 bit RGB (for now).
    Intent is to decouple pixel from resolution and encapsulate the colour conversions and bitwise crossover.
    Resolution only matters when reading from an existing image or at write stage.
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
        return tuple([clipValue(v) for v in (values + (0, 0, 0))[:3]])

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

        if length == 2:  # 16-bit
            if byteorder == 'big':
                components = [x >> 3 for x in self.rgb]
            elif byteorder == 'little':
                components = [x >> 3 for x in self.rgb[::-1]]
            else:
                msg = "Unrecognised byteorder: '{}'.".format(byteorder)
                raise ValueError(msg)
            shift = 5

        elif length == 3:  # 24-bit
            if byteorder == 'big':
                components = self.rgb[:]
            elif byteorder == 'little':
                components = self.rgb[::-1]
                # print(self.rgb)
                # print(components)
            else:
                msg = "Unrecognised byteorder: '{}'.".format(byteorder)
                raise ValueError(msg)
            shift = 8
        else:
            msg = "Unsupported length: '{}'.".format(length)
            raise ValueError(msg)

        retVal = 0
        for c in components:
            retVal <<= shift
            retVal += c

        return retVal.to_bytes(length, byteorder='big')


class Bitmap:
    """
    http://www.ece.ualberta.ca/~elliott/ee552/studentAppNotes/2003_w/misc/bmp_file_format/bmp_file_format.htm

    Each scan line is zero padded to the nearest 4-byte boundary. If the image has a width that is not divisible by
    four, say, 21 bytes, there would be 3 bytes of padding at the end of every scan line.

    Scan lines are stored bottom to top instead of top to bottom.

    RGB values are stored backwards i.e. BGR.
    """

    def __init__(self, dims, pixels=None, colours=None, fillFunc=_patternBlank):
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
        else:
            self.pixels = fillFunc(dims, colours)
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
        return cls(dims, colours=[colour], fillFunc=_patternBlank)

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

    def write(self, filename, res=24):
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
