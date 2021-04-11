from bitmap import bitmap
import math
import unittest


class TestHelperFunctions(unittest.TestCase):
    def test_dotProduct_directionalVectors_arbitrary_horizontal(self):
        vHorizontal = bitmap.unitVector(0)
        vsTest = [(a, b) for a in range(-5, 6) for b in range(-5, 6) if a or b]  # No zero length vectors
        xs = [a for a, b in vsTest]
        distances = [round(bitmap._dotProduct(vHorizontal, v)) for v in vsTest]
        self.assertEqual(xs, distances)

    def test_dotProduct_directionalVectors_arbitrary_vertical(self):
        vVertical = bitmap.unitVector(90)
        vsTest = [(a, b) for a in range(-5, 6) for b in range(-5, 6) if a or b]  # No zero length vectors
        ys = [b for a, b in vsTest]
        distances = [round(bitmap._dotProduct(vVertical, v)) for v in vsTest]
        self.assertEqual(ys, distances)

    def test_dotProduct_directionalVectors_arbitrary_directional(self):
        places = 3
        vsTest = [(a, b) for a in range(-5, 6) for b in range(-5, 6) if a or b]  # No zero length vectors
        lengths = [round(bitmap._vectorLength(v), places) for v in vsTest]
        distances = [round(bitmap._dotProduct(bitmap.unitVector(v), v), places) for v in vsTest]
        # for i in range(len(vsTest)):
        #     print("v: {}: l: {}: vu: {}: ".format(vsTest[i], lengths[i], vsUnit[i]))
        self.assertEqual(lengths, distances)

    def test_dotProduct_directionalVectors_triangle345(self):
        vHorizontal = bitmap.unitVector(0)
        vVertical = bitmap.unitVector(90)
        vsTest = [(3, 4), (4, 3)]
        thetas = [math.degrees(math.atan(b / a)) for a, b in vsTest]
        print(thetas)
        vsUnit = [bitmap.unitVector(theta) for theta in thetas]  # unit vectors in the direction of the vectors
        print(vsUnit)
        distances = []
        distances.append([round(bitmap._dotProduct(vHorizontal, v)) for v in vsTest])
        distances.append([round(bitmap._dotProduct(vVertical, v)) for v in vsTest])
        distances.append([round(bitmap._dotProduct(vsUnit[i], vsTest[i])) for i in range(2)])
        print(distances)
        self.assertEqual([[3, 4], [4, 3], [5, 5]], distances)

    def test_dotProduct_unitVectors_fromZero(self):
        uv1 = bitmap.unitVector(0)
        for theta in range(-179, 180):
            uv2 = bitmap.unitVector(theta)
            msg = "{}: {}, {}: {}".format(theta, uv1, theta, uv2)
            print(msg)
            self.assertAlmostEqual(math.cos(abs(math.radians(theta))), bitmap._dotProduct(uv1, uv2), msg=msg)

    def test_dotProduct_knownVectors(self):
        a = (1, 2, 3)
        b = (4, -5, 6)
        self.assertEqual(12, bitmap._dotProduct(a, b))
        c = (-4, -9)
        d = (-1, 2)
        self.assertEqual(-14, bitmap._dotProduct(c, d))
        e = (6, -1, 3)
        f = (4, 18, -2)
        self.assertEqual(0, bitmap._dotProduct(e, f))

    def test_dotProduct_orthogonals(self):
        thetas = [270, 90, -90, -270]
        for angle in range(0, 360, 7):
            uv1 = bitmap.unitVector(angle)
            for theta in thetas:
                uv2 = bitmap.unitVector(angle + theta)
                msg = "{}: {}, {}: {}".format(angle, uv1, theta, uv2)
                self.assertAlmostEqual(0, bitmap._dotProduct(uv1, uv2), msg=msg)

    def test_dotProduct_opposites(self):
        thetas = [180, -180]
        for angle in range(0, 360, 7):
            uv1 = bitmap.unitVector(angle)
            for theta in thetas:
                uv2 = bitmap.unitVector(angle + theta)
                msg = "{}: {}, {}: {}".format(angle, uv1, theta, uv2)
                self.assertAlmostEqual(-1, bitmap._dotProduct(uv1, uv2), msg=msg)

    def test_dotProduct_unitVectors(self):
        for angle in range(-179, 360, 7):
            uv1 = bitmap.unitVector(angle)
        for theta in range(0, 180, 2):
            uv2 = bitmap.unitVector(angle + theta)
            msg = "{}: {}, {}: {}".format(angle, uv1, theta, uv2)
            print(msg)
            self.assertAlmostEqual(math.cos(abs(math.radians(theta))), bitmap._dotProduct(uv1, uv2), places=2, msg=msg)

    def test_radialIntersection_landscape_inPicture(self):
        xmax = 149
        ymax = 99
        dims = (xmax + 1, ymax + 1)
        for angle in range(0, 360, 5):
            x, y = bitmap._radialIntersection(dims, angle)
            msg = "Angle: {}, Intersect: ({}, {})".format(angle, x, y)
            print(msg)
            self.assertTrue(0 <= x <= xmax and 0 <= y <= ymax, msg=msg)

    def test_radialIntersection_landscape_onEdge(self):
        xmax = 149
        ymax = 99
        dims = (xmax + 1, ymax + 1)
        for angle in range(0, 360, 5):
            x, y = bitmap._radialIntersection(dims, angle)
            msg = "Angle: {}, Intersect: ({}, {})".format(angle, x, y)
            print(msg)
            self.assertTrue(x == 0 or x == xmax or y == 0 or y == ymax, msg)

    def test_radialIntersection_portrait_inPicture(self):
        xmax = 99
        ymax = 149
        dims = (xmax + 1, ymax + 1)
        for angle in range(0, 360, 5):
            x, y = bitmap._radialIntersection(dims, angle)
            msg = "Angle: {}, Origin: ({}, {})".format(angle, x, y)
            print(msg)
            self.assertTrue(0 <= x <= xmax and 0 <= y <= ymax, msg)

    def test_radialIntersection_portrait_onEdge(self):
        xmax = 99
        ymax = 149
        dims = (xmax + 1, ymax + 1)
        for angle in range(0, 360, 3):
            x, y = bitmap._radialIntersection(dims, angle)
            msg = "Angle: {}, Origin: ({}, {})".format(angle, x, y)
            print(msg)
            self.assertTrue(x == 0 or x == xmax or y == 0 or y == ymax, msg)

    def test_radialIntersection_square_inPicture(self):
        max = 99
        dims = (max + 1, max + 1)
        for angle in range(0, 360, 5):
            x, y = bitmap._radialIntersection(dims, angle)
            msg = "Angle: {}, Origin: ({}, {})".format(angle, x, y)
            print(msg)
            self.assertTrue(0 <= x <= max and 0 <= y <= max, msg)

    def test_radialIntersection_square_onEdge(self):
        max = 99
        dims = (max + 1, max + 1)
        for angle in range(0, 360, 5):
            x, y = bitmap._radialIntersection(dims, angle)
            msg = "Angle: {}, Origin: ({}, {})".format(angle, x, y)
            print(msg)
            self.assertTrue(x == 0 or x == max or y == 0 or y == max, msg)

    def test_radialIntersection_cornerBL(self):
        dims = (100, 100)
        self.assertEqual((0, 0), bitmap._radialIntersection(dims, -135))

    def test_radialIntersection_cornerTL(self):
        dims = (100, 100)
        self.assertEqual((0, 99), bitmap._radialIntersection(dims, 135))

    def test_radialIntersection_cornerBR(self):
        dims = (100, 100)
        self.assertEqual((99, 0), bitmap._radialIntersection(dims, -45))

    def test_radialIntersection_cornerTR(self):
        dims = (100, 100)
        self.assertEqual((99, 99), bitmap._radialIntersection(dims, 45))

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

    def test_clipValue(self):
        for i in range(-256, 512):
            clipped = bitmap.clipValue(i)
            if i < 0:
                self.assertEqual(0, clipped)
            elif i > 255:
                self.assertEqual(255, clipped)
            else:
                self.assertEqual(i, clipped)

    def test_unitVector_length(self):
        for i in range(0, 359):
            a, b = bitmap.unitVector(i)
            self.assertAlmostEqual(1.0, a ** 2 + b ** 2, msg=i)

    def test_unitVector_opposite(self):
        for i in range(0, 179):
            a1, b1 = bitmap.unitVector(i)
            a2, b2 = bitmap.unitVector(i + 180)
            self.assertAlmostEqual(0, a1 + a2, msg=i)
            self.assertAlmostEqual(0, b1 + b2, msg=i)

    def test_unitVector_45s(self):
        for i in range(45, 360, 90):
            a1, b1 = bitmap.unitVector(i)
            self.assertAlmostEqual(abs(a1), abs(b1), msg=i)

    def test_unitVector_90s(self):
        for i in range(0, 360, 90):
            a1, b1 = bitmap.unitVector(i)
            self.assertTrue(round(abs(a1)) == 1.0 or round(abs(b1)) == 1.0, i)

    def test_unitVector_bottomHalf(self):
        for i in range(181, 360):
            x, y = bitmap.unitVector(i)
            msg = "({}, {}) = {}°".format(x, y, i)
            print(msg)
            self.assertTrue(y < 0, msg=msg)

    def test_unitVector_leftHalf(self):
        for i in range(91, 270):
            x, y = bitmap.unitVector(i)
            msg = "({}, {}) = {}°".format(x, y, i)
            print(msg)
            self.assertTrue(x < 0, msg=msg)

    def test_unitVector_rightHalf(self):
        for i in range(-89, 90):
            x, y = bitmap.unitVector(i)
            msg = "({}, {}) = {}°".format(x, y, i)
            print(msg)
            self.assertTrue(x > 0, msg=msg)

    def test_unitVector_topHalf(self):
        for i in range(1, 180):
            x, y = bitmap.unitVector(i)
            msg = "({}, {}) = {}°".format(x, y, i)
            print(msg)
            self.assertTrue(y > 0, msg=msg)

    def test_vectorAngle_knownAngles(self):
        v1 = (1, 0)
        vsTest = [((1, 0), 0), ((5, 0), 0), ((1, 1), 45), ((3, 3), 45), ((0, 1), 90), ((0, 6), 90), ((-1, 1), 135),
                  ((-3, 3), 135), ((-1, 0), 180), ((-5, 0), 180), ((-1, -1), 135), ((-3, -3), 135), ((0, -1), 90),
                  ((0, -6), 90), ((1, -1), 45), ((7, -7), 45)]
        expectedAnswers = [a for v, a in vsTest]
        calculatedAnswers = [round(bitmap._vectorAngle(v1, v)) for v, a in vsTest]
        self.assertEqual(expectedAnswers, calculatedAnswers)

    def test_vectorLength_unitVectors(self):
        for theta in range(-180, 180):
            v = bitmap.unitVector(theta)
            self.assertAlmostEqual(1.0, bitmap._vectorLength(v), msg=v)

    def test_vectorLength_345(self):
        v = (3, 4)
        self.assertEqual(5, bitmap._vectorLength(v))

    def test_vectorLength_435(self):
        v = (4, 3)
        self.assertEqual(5, bitmap._vectorLength(v))

    def test_vectorLength_unitVectors(self):
        for theta in range(-180, 180):
            v = bitmap.unitVector(theta)
            self.assertAlmostEqual(1.0, bitmap._vectorLength(v), msg=v)


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


class TestBitmap_128x128_24_gradient0__default(unittest.TestCase):
    filename = "test_128x128_24_gradient0_default"
    bmp = bitmap.Bitmap.gradient((256, 256), angle=0)
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient0_colours(unittest.TestCase):
    filename = "test_128x128_24_gradient0_colours"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=0, colour1=(11, 31, 255), colour2=(129, 128, 15))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient90__default(unittest.TestCase):
    filename = "test_128x128_24_gradient90_default"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=90)
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient90_colours(unittest.TestCase):
    filename = "test_128x128_24_gradient90_colours"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=90, colour1=(63, 0, 64), colour2=(224, 255, 128))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient180__default(unittest.TestCase):
    filename = "test_128x128_24_gradient180_default"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=180)
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient180_colours(unittest.TestCase):
    filename = "test_128x128_24_gradient180_colours"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=180, colour1=(255, 0, 129), colour2=(255, 255, 15))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient270__default(unittest.TestCase):
    filename = "test_128x128_24_gradient270_default"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=270)
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


class TestBitmap_128x128_24_gradient270_colours(unittest.TestCase):
    filename = "test_128x128_24_gradient270_colours"
    bmp = bitmap.Bitmap.gradient((128, 128), angle=270, colour1=(221, 31, 192), colour2=(7, 96, 7))
    bmp.writeBMP(filename)

    def test_write_128x128_24_blue_identifier(self):
        with open('{}.bmp'.format(self.filename), 'rb') as bmp:
            signature = bmp.read(2)
        self.assertEqual(b'BM', signature)


if __name__ == '__main__':
    unittest.main()
