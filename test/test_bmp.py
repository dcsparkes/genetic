import pathlib
import unittest
from bitmap import bitmap


class TestHelperFunctions(unittest.TestCase):
    def test_clipValue(self):
        for i in range(-256, 512):
            clipped = bitmap.clipValue(i)
            if i < 0:
                self.assertEqual(0, clipped)
            elif i > 255:
                self.assertEqual(255, clipped)
            else:
                self.assertEqual(i, clipped)

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
                bmp.write("exception", res)
                print("Successful resolution = {}".format(res))


class TestBitmap_16x16_16(unittest.TestCase):
    filename = "test_16x16_16"
    bmp = bitmap.Bitmap.blank((16, 16), colour=(255, 0, 0))
    bmp.write(filename, res=16)

    def test_write_16x16_16_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)

class TestBitmap_128x128_16_red(unittest.TestCase):
    filename = "test_128x128_16_red"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(255, 5, 10))
    bmp.write(filename, res=16)

    def test_write_128x128_16_red_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)

class TestBitmap_128x128_16_green(unittest.TestCase):
    filename = "test_128x128_16_green"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(10, 255, 5))
    bmp.write(filename, res=16)

    def test_write_128x128_16_green_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)

class TestBitmap_128x128_16_blue(unittest.TestCase):
    filename = "test_128x128_16_blue"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(5, 10, 255))
    bmp.write(filename, res=16)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_lightOrange(unittest.TestCase):
    filename = "test_128x128_24_lightorange"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(255, 192, 64))
    bmp.write(filename)

    def test_write_128x128_24_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)

class TestBitmap_128x128_24_default(unittest.TestCase):
    filename = "test_128x128_24_default"
    bmp = bitmap.Bitmap.blank((128, 128))
    bmp.write(filename)

    def test_write_128x128_24_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)

class TestBitmap_128x128_24_red(unittest.TestCase):
    filename = "test_128x128_24_red"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(255, 5, 10))
    bmp.write(filename)

    def test_write_128x128_24_red_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)

class TestBitmap_128x128_24_green(unittest.TestCase):
    filename = "test_128x128_24_green"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(10, 255, 5))
    bmp.write(filename)

    def test_write_128x128_24_green_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)

class TestBitmap_128x128_24_blue(unittest.TestCase):
    filename = "test_128x128_24_blue"
    bmp = bitmap.Bitmap.blank((128, 128), colour=(5, 10, 255))
    bmp.write(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)

if __name__ == '__main__':
    unittest.main()
