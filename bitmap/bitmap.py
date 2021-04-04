class Bitmap:
    """
    http://www.ece.ualberta.ca/~elliott/ee552/studentAppNotes/2003_w/misc/bmp_file_format/bmp_file_format.htm

    Each scan line is zero padded to the nearest 4-byte boundary. If the image has a width that is not divisible by
    four, say, 21 bytes, there would be 3 bytes of padding at the end of every scan line.

    Scan lines are stored bottom to top instead of top to bottom.

    RGB values are stored backwards i.e. BGR.
    """

    def __init__(self, dims, res, pixels=None, fillFunc=None):
        """
        :param dims: tuple of (x, y) dimensions in pixels
        :param res: bits per pixel
        :param pixels: list of pixels, None for self-generated
        """
        if res in [16, 24]:
            self.res = res
        else:
            msg = "Invalid resolution: {}".format(res)
            raise ValueError(msg)

        if not pixels:
            x, y = dims
            self.pixels = [[(0).to_bytes(res // 8, byteorder='little')] * x for i in range(y)]
        else:
            self.pixels = pixels
        self.dims = dims
        if res in [16, 24]:
            self.res = res
        else:
            msg = "Invalid resolution: {}".format(res)
            raise ValueError(msg)

    def _fillBlank(self, colour):

    @staticmethod
    def _isColourValid(rgb):
        """
        Assume colour fits in 24 bit RGB - check values are not too large (>255) or too small (<0).

        :param rgb: An RGB triple
        :return: True if valid, False if invalid
        """

        if len(rgb) is not 3:
            return False
        for value in rgb:
            if not (0 <= value <= 255):
                return False
        return True

    @classmethod
    def fromFile(cls, fileName):
        # read file, and fill bitmap object from the data
        dims = None
        res = None
        pixels = None
        return cls(dims, res, pixels)

    def blank(cls, dims, res=24, colour=None):
        if colour is None:
            pixel = (2 ** res - 1).to_bytes(res // 8, byteorder='little')
        elif type(colour) is tuple:
            if not self._isColourValid(colour):
                msg = "Incompatible RGB value: {}".format(colour)
                raise ValueError(msg)



        elif type(colour) is bytes:

            x, y = dims
            self.pixels = [[(0)].to_bytes(res // 8, byteorder='little') * x for i in range(y)]

        pass

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

    def createInfoHeader(self, offset=54, ppm=250):
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
        header += self.res.to_bytes(2, byteorder='little')  # bitsPerPixel
        header += (0).to_bytes(4, byteorder='little')  # compression not supported
        header += (0).to_bytes(4, byteorder='little')  # compression not supported: imagesize irrelevant
        header += ppm.to_bytes(4, byteorder='little')  # XpixelsPerM: use magic number?
        header += ppm.to_bytes(4, byteorder='little')  # YpixelsPerM: use magic number?
        header += (2 ** self.res).to_bytes(4, byteorder='little')  # colors used... appears to be big byte order?
        header += (0).to_bytes(4, byteorder='little')  # Important Colors = all

        return header

    def write(self, filename):
        """
        Each scan line is zero padded to the nearest 4-byte boundary. If the image has a width that is not divisible by
        four, say, 21 bytes, there would be 3 bytes of padding at the end of every scan line.

        :return:
        """
        lineBytes = (self.dims[0] * self.res) // 8  # line size = pixels * bits per pixel
        paddingSize = -lineBytes % 4
        imageStorageSize = (lineBytes + paddingSize) * self.dims[
            1]  # Storage size = line size (bytes) * number of lines
        headerSize = 14 + 40
        fileSize = headerSize + imageStorageSize
        fileHeader = self.createHeader(fileSize)
        infoHeader = self.createInfoHeader()

        paddingBytes = (0).to_bytes(1, 'little') * paddingSize

        with open('{}.bmp'.format(filename), 'wb') as bmp:
            bmp.write(fileHeader)
            bmp.write(infoHeader)
            for line in self.pixels:
                for pixel in line:
                    bmp.write(pixel)
                bmp.write(paddingBytes)
