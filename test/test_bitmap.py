import shared.shared
from bitmap import bitmap
import unittest


class TestHelperFunctions(unittest.TestCase):
    def test_rgbBlend_0(self):
        rgb1 = (8, 16, 32)
        rgb2 = (255, 128, 64)
        self.assertEqual(rgb1, bitmap._rgbBlend(rgb1, rgb2, 0.0))

    def test_rgbBlend_1(self):
        rgb1 = (8, 16, 32)
        rgb2 = (255, 128, 64)
        self.assertEqual(rgb2, bitmap._rgbBlend(rgb1, rgb2, 1.0))

    def test_rgbBlend_withinBounds(self):
        rgb1 = (8, 16, 32)
        rgb2 = (255, 128, 64)
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2

        for d in range(10):
            for n in range(1, d):
                msg = "{}/{} = {}".format(n, d, n / d)
                rt, gt, bt = bitmap._rgbBlend(rgb1, rgb2, n / d)
                self.assertTrue(r1 < rt < r2, msg)
                self.assertTrue(g1 < gt < g2, msg)
                self.assertTrue(b1 < bt < b2, msg)

    def test_rgbBlend_typeCheck(self):
        rgb1 = (8, 16, 32)
        rgb2 = (255, 128, 64)
        blend = bitmap._rgbBlend(rgb1, rgb2, 0.5)
        self.assertEqual(tuple, type(blend), "tuple")
        self.assertEqual(int, type(blend[0]), "int")


class TestPixel(unittest.TestCase):
    def test_constructTupleFromNumber(self):
        for i in range(-256, 512):
            p = bitmap.Pixel()
            tuple = p._constructTupleFromNumber(i)
            if i < 0:
                self.assertEqual((0, 0, 0), tuple, i)
            elif i > 255:
                self.assertEqual((255, 255, 255), tuple)
            else:
                self.assertEqual((i, i, i), tuple)

    def test_validateTuple(self):
        for i in range(-256, 512):
            p = bitmap.Pixel()
            tuple = p._validateTuple((i, i, i))
            if i < 0:
                self.assertEqual((0, 0, 0), tuple, i)
            elif i > 255:
                self.assertEqual((255, 255, 255), tuple, i)
            else:
                self.assertEqual((i, i, i), tuple, i)


class TestBitmapCreation(unittest.TestCase):
    def test_init_16x16_16(self):
        bmp = bitmap.Bitmap((16, 16))
        self.assertEqual(16, len(bmp.pixels))
        self.assertEqual(16, len(bmp.pixels[0]))

    def test_init_2x2_16(self):
        bmp = bitmap.Bitmap((2, 2))
        self.assertEqual(2, len(bmp.pixels))
        self.assertEqual(2, len(bmp.pixels[0]))

    def test_createHeader_16x16_16_len(self):
        bmp = bitmap.Bitmap((16, 16))
        header = bmp.createHeader(16 ** 3)
        # print(header)
        self.assertEqual(14, len(header))

    def test_createInfoHeader_16x16_16_len(self):
        bmp = bitmap.Bitmap((16, 16))
        header = bmp.createInfoHeader(16)
        # print(header)
        self.assertEqual(40, len(header))

    def test_write_16x16_invalidResolutions(self):
        for res in [0, 2, 3, 5, 7, 15, 17, 23, 25, 1, 4, 8]:
            with self.assertRaises(ValueError):
                bmp = bitmap.Bitmap((16, 16))
                bmp.writeBMP("exception", res)
                print("Successful resolution = {}".format(res))


class TestBitmap_16x16_16(unittest.TestCase):
    filename = "test_16x16_16"
    bmp = bitmap.Bitmap.blank((16, 16), colour=(255, 255, 255))
    bmp.writeBMP(filename, res=16)

    def test_write_16x16_16_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_16_red(unittest.TestCase):
    filename = "test_128x128_16_red"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(255, 5, 2))
    bmp.writeBMP(filename, res=16)

    def test_write_128x128_16_red_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_16_green(unittest.TestCase):
    filename = "test_128x128_16_green"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(2, 255, 5))
    bmp.writeBMP(filename, res=16)

    def test_write_128x128_16_green_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_16_blue(unittest.TestCase):
    filename = "test_128x128_16_blue"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(5, 2, 255))
    bmp.writeBMP(filename, res=16)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_lightOrange(unittest.TestCase):
    filename = "test_128x128_24_lightorange"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(255, 192, 64))
    bmp.writeBMP(filename)

    def test_write_128x128_24_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_default(unittest.TestCase):
    filename = "test_128x128_24_default"
    bmp = bitmap.Bitmap.blank((128, 128))
    bmp.writeBMP(filename)

    def test_write_128x128_24_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_red(unittest.TestCase):
    filename = "test_128x128_24_red"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(255, 5, 10))
    bmp.writeBMP(filename)

    def test_write_128x128_24_red_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_green(unittest.TestCase):
    filename = "test_128x128_24_green"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(10, 255, 5))
    bmp.writeBMP(filename)

    def test_write_128x128_24_green_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_blue(unittest.TestCase):
    filename = "test_128x128_24_blue"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(5, 10, 255))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_checkerboard_default(unittest.TestCase):
    filename = "test_128x128_24_checkerboard_default"
    bmp = bitmap.Bitmap.checkerboard((128, 128), checksize=64)
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_checkerboard_colours(unittest.TestCase):
    filename = "test_128x128_24_checkerboard_colours"
    bmp = bitmap.Bitmap.checkerboard((128, 128), checksize=16, colour1=(255, 255, 31), colour2=(128, 31, 128))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gaussian_default(unittest.TestCase):
    filename = "test_128x128_24_gaussian_default"
    bmp = bitmap.Bitmap.gaussian((256, 256))
    bmp.writeBMP(filename)

    def test_write_128x128_24_gaussian_default(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gaussian_reversed(unittest.TestCase):
    filename = "test_128x128_24_gaussian_reversed"
    bmp = bitmap.Bitmap.gaussian((256, 256), colour=(255, 255, 255), delta=-1, terminal=0)
    bmp.writeBMP(filename)

    def test_write_128x128_24_gaussian_default(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient0__default(unittest.TestCase):
    filename = "test_128x128_24_gradient_0°_default"
    bmp = bitmap.Bitmap.gradient((256, 256), angle=0)
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient0_colours(unittest.TestCase):
    filename = "test_128x128_24_gradient_0°_colours"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=0, colour1=(11, 31, 255), colour2=(129, 128, 15))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient90__default(unittest.TestCase):
    filename = "test_128x128_24_gradient_90°_default"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=90)
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient90_colours(unittest.TestCase):
    filename = "test_128x128_24_gradient_90°_colours"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=90, colour1=(63, 0, 64), colour2=(224, 255, 128))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient180__default(unittest.TestCase):
    filename = "test_128x128_24_gradient_180°_default"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=180)
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient180_colours(unittest.TestCase):
    filename = "test_128x128_24_gradient_180°_colours"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=180, colour1=(255, 0, 129), colour2=(255, 255, 15))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient270__default(unittest.TestCase):
    filename = "test_128x128_24_gradient_270°_default"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=270)
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient130__colours(unittest.TestCase):
    filename = "test_128x128_24_gradient_130°_colours"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=130, colour1=(129, 31, 133), colour2=(108, 106, 255))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient255__colours(unittest.TestCase):
    filename = "test_128x128_24_gradient_255°_colours"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=255, colour1=(0, 63, 0), colour2=(255, 190, 255))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient270_colours(unittest.TestCase):
    filename = "test_128x128_24_gradient_270°_colours"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=270, colour1=(221, 31, 192), colour2=(7, 96, 7))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_stripes_default(unittest.TestCase):
    filename = "test_128x128_24_stripes_default"
    bmp = bitmap.Bitmap.stripes((128, 128))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_stripes9_30_colours(unittest.TestCase):
    filename = "test_128x128_24_stripes_9_30°_colours"
    bmp = bitmap.Bitmap.stripes((128, 128), stripewidth=9, angle=30, colour1=(221, 237, 192), colour2=(7, 96, 7))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_stripes14_100_colours(unittest.TestCase):
    filename = "test_128x128_24_stripes_14_100°_colours"
    bmp = bitmap.Bitmap.stripes((128, 128), stripewidth=14, angle=100, colour1=(221, 237, 7), colour2=(7, 96, 192))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


if __name__ == '__main__':
    unittest.main()
