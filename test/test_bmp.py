import unittest
from bitmap import bitmap

class TestBitmapCreation(unittest.TestCase):
    def test_init_16x16_invalidResolutions(self):
        for res in [0, 2, 3, 5, 7, 15, 17, 23, 25, 1, 4, 8]:
            with self.assertRaises(ValueError):
                bitmap.Bitmap((16, 16), res)
                print("Successful resolution = {}".format(res))

    def test_init_16x16_16(self):
        bmp = bitmap.Bitmap((16,16), 16)
        self.assertEqual(16, len(bmp.pixels))
        self.assertEqual(16, len(bmp.pixels[0]))

    def test_init_2x2_16(self):
        bmp = bitmap.Bitmap((2, 2), 16)
        self.assertEqual(2, len(bmp.pixels))
        self.assertEqual(2, len(bmp.pixels[0]))

    def test_createHeader_16x16_16_len(self):
        bmp = bitmap.Bitmap((16,16), 16)
        header = bmp.createHeader(16**3)
        print(header)
        self.assertEqual(14, len(header))

    def test_createInfoHeader_16x16_16_len(self):
        bmp = bitmap.Bitmap((16,16), 16)
        header = bmp.createInfoHeader()
        print(header)
        self.assertEqual(40, len(header))

    def test_write_16x16_16_exists(self):
        bmp = bitmap.Bitmap((16,16), 16)
        bmp.write("test_16x16_16")

    def test_write_128x128_24_exists(self):
        bmp = bitmap.Bitmap((128, 128), 24)
        bmp.write("test_128x128_24")



if __name__ == '__main__':
    unittest.main()
