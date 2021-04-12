"""
Test file for vector operations.  Decoupled from bitmap module.
"""
from shared import shared
from vector import vector
import math
import unittest


class TestHelperFunctions(unittest.TestCase):
    def test_dotProduct_directionalVectors_arbitrary_horizontal(self):
        vHorizontal = vector.unitVector(0)
        vsTest = [(a, b) for a in range(-5, 6) for b in range(-5, 6) if a or b]  # No zero magnitude vectors
        xs = [a for a, b in vsTest]
        distances = [round(vector.dotProduct(vHorizontal, v)) for v in vsTest]
        self.assertEqual(xs, distances)

    def test_dotProduct_directionalVectors_arbitrary_vertical(self):
        vVertical = vector.unitVector(90)
        vsTest = [(a, b) for a in range(-5, 6) for b in range(-5, 6) if a or b]  # No zero magnitude vectors
        ys = [b for a, b in vsTest]
        distances = [round(vector.dotProduct(vVertical, v)) for v in vsTest]
        self.assertEqual(ys, distances)

    def test_dotProduct_directionalVectors_arbitrary_directional(self):
        places = 3
        vsTest = [(a, b) for a in range(-5, 6) for b in range(-5, 6) if a or b]  # No zero magnitude vectors
        lengths = [round(vector._vectorLength(v), places) for v in vsTest]
        distances = [round(vector.dotProduct(vector.unitVector(v), v), places) for v in vsTest]
        # for i in range(len(vsTest)):
        #     print("v: {}: l: {}: vu: {}: ".format(vsTest[i], lengths[i], vsUnit[i]))
        self.assertEqual(lengths, distances)

    def test_dotProduct_directionalVectors_triangle345(self):
        vHorizontal = vector.unitVector(0)
        vVertical = vector.unitVector(90)
        vsTest = [(3, 4), (4, 3)]
        thetas = [math.degrees(math.atan(b / a)) for a, b in vsTest]
        # print(thetas)
        vsUnit = [vector.unitVector(theta) for theta in
                  thetas]  # unit vectors in the direction of the vectors
        # print(vsUnit)
        distances = []
        distances.append([round(vector.dotProduct(vHorizontal, v)) for v in vsTest])
        distances.append([round(vector.dotProduct(vVertical, v)) for v in vsTest])
        distances.append([round(vector.dotProduct(vsUnit[i], vsTest[i])) for i in range(2)])
        # print(distances)
        self.assertEqual([[3, 4], [4, 3], [5, 5]], distances)

    def test_dotProduct_unitVectors_fromZero(self):
        uv1 = vector.unitVector(0)
        for theta in range(-179, 180):
            uv2 = vector.unitVector(theta)
            msg = "{}: {}, {}: {}".format(theta, uv1, theta, uv2)
            # print(msg)
            self.assertAlmostEqual(math.cos(abs(math.radians(theta))), vector.dotProduct(uv1, uv2), msg=msg)

    def test_dotProduct_knownVectors(self):
        a = (1, 2, 3)
        b = (4, -5, 6)
        self.assertEqual(12, vector.dotProduct(a, b))
        c = (-4, -9)
        d = (-1, 2)
        self.assertEqual(-14, vector.dotProduct(c, d))
        e = (6, -1, 3)
        f = (4, 18, -2)
        self.assertEqual(0, vector.dotProduct(e, f))

    def test_dotProduct_orthogonals(self):
        thetas = [270, 90, -90, -270]
        for angle in range(0, 360, 7):
            uv1 = vector.unitVector(angle)
            for theta in thetas:
                uv2 = vector.unitVector(angle + theta)
                msg = "{}: {}, {}: {}".format(angle, uv1, theta, uv2)
                self.assertAlmostEqual(0, vector.dotProduct(uv1, uv2), msg=msg)

    def test_dotProduct_opposites(self):
        thetas = [180, -180]
        for angle in range(0, 360, 7):
            uv1 = vector.unitVector(angle)
            for theta in thetas:
                uv2 = vector.unitVector(angle + theta)
                msg = "{}: {}, {}: {}".format(angle, uv1, theta, uv2)
                self.assertAlmostEqual(-1, vector.dotProduct(uv1, uv2), msg=msg)

    def test_dotProduct_unitVectors(self):
        for angle in range(-179, 360, 7):
            uv1 = vector.unitVector(angle)
        for theta in range(0, 180, 2):
            uv2 = vector.unitVector(angle + theta)
            msg = "{}: {}, {}: {}".format(angle, uv1, theta, uv2)
            # print(msg)
            self.assertAlmostEqual(math.cos(abs(math.radians(theta))), vector.dotProduct(uv1, uv2),
                                   places=2, msg=msg)

    def test_radialIntersection_landscape_inPicture(self):
        xmax = 149
        ymax = 99
        dims = (xmax + 1, ymax + 1)
        for angle in range(0, 360, 5):
            x, y = vector.radialIntersection(dims, angle)
            msg = "Angle: {}, Intersect: ({}, {})".format(angle, x, y)
            # print(msg)
            self.assertTrue(0 <= x <= xmax and 0 <= y <= ymax, msg=msg)

    def test_radialIntersection_landscape_onEdge(self):
        xmax = 149
        ymax = 99
        dims = (xmax + 1, ymax + 1)
        for angle in range(0, 360, 5):
            x, y = vector.radialIntersection(dims, angle)
            msg = "Angle: {}, Intersect: ({}, {})".format(angle, x, y)
            # print(msg)
            self.assertTrue(x == 0 or x == xmax or y == 0 or y == ymax, msg)

    def test_radialIntersection_portrait_inPicture(self):
        xmax = 99
        ymax = 149
        dims = (xmax + 1, ymax + 1)
        for angle in range(0, 360, 5):
            x, y = vector.radialIntersection(dims, angle)
            msg = "Angle: {}, Origin: ({}, {})".format(angle, x, y)
            # print(msg)
            self.assertTrue(0 <= x <= xmax and 0 <= y <= ymax, msg)

    def test_radialIntersection_portrait_onEdge(self):
        xmax = 99
        ymax = 149
        dims = (xmax + 1, ymax + 1)
        for angle in range(0, 360, 3):
            x, y = vector.radialIntersection(dims, angle)
            msg = "Angle: {}, Origin: ({}, {})".format(angle, x, y)
            # print(msg)
            self.assertTrue(x == 0 or x == xmax or y == 0 or y == ymax, msg)

    def test_radialIntersection_square_inPicture(self):
        max = 99
        dims = (max + 1, max + 1)
        for angle in range(0, 360, 5):
            x, y = vector.radialIntersection(dims, angle)
            msg = "Angle: {}, Origin: ({}, {})".format(angle, x, y)
            # print(msg)
            self.assertTrue(0 <= x <= max and 0 <= y <= max, msg)

    def test_radialIntersection_square_onEdge(self):
        max = 99
        dims = (max + 1, max + 1)
        for angle in range(0, 360, 5):
            x, y = vector.radialIntersection(dims, angle)
            msg = "Angle: {}, Origin: ({}, {})".format(angle, x, y)
            # print(msg)
            self.assertTrue(x == 0 or x == max or y == 0 or y == max, msg)

    def test_radialIntersection_cornerBL(self):
        dims = (100, 100)
        self.assertEqual((0, 0), vector.radialIntersection(dims, -135))

    def test_radialIntersection_cornerTL(self):
        dims = (100, 100)
        self.assertEqual((0, 99), vector.radialIntersection(dims, 135))

    def test_radialIntersection_cornerBR(self):
        dims = (100, 100)
        self.assertEqual((99, 0), vector.radialIntersection(dims, -45))

    def test_radialIntersection_cornerTR(self):
        dims = (100, 100)
        self.assertEqual((99, 99), vector.radialIntersection(dims, 45))

    def test_unitVector_length(self):
        for i in range(0, 359):
            a, b = vector.unitVector(i)
            self.assertAlmostEqual(1.0, a ** 2 + b ** 2, msg=i)

    def test_unitVector_opposite(self):
        for i in range(0, 179):
            a1, b1 = vector.unitVector(i)
            a2, b2 = vector.unitVector(i + 180)
            self.assertAlmostEqual(0, a1 + a2, msg=i)
            self.assertAlmostEqual(0, b1 + b2, msg=i)

    def test_unitVector_45s(self):
        for i in range(45, 360, 90):
            a1, b1 = vector.unitVector(i)
            self.assertAlmostEqual(abs(a1), abs(b1), msg=i)

    def test_unitVector_90s(self):
        for i in range(0, 360, 90):
            a1, b1 = vector.unitVector(i)
            self.assertTrue(round(abs(a1)) == 1.0 or round(abs(b1)) == 1.0, i)

    def test_unitVector_bottomHalf(self):
        for i in range(181, 360):
            x, y = vector.unitVector(i)
            msg = "({}, {}) = {}°".format(x, y, i)
            # print(msg)
            self.assertTrue(y < 0, msg=msg)

    def test_unitVector_leftHalf(self):
        for i in range(91, 270):
            x, y = vector.unitVector(i)
            msg = "({}, {}) = {}°".format(x, y, i)
            # print(msg)
            self.assertTrue(x < 0, msg=msg)

    def test_unitVector_rightHalf(self):
        for i in range(-89, 90):
            x, y = vector.unitVector(i)
            msg = "({}, {}) = {}°".format(x, y, i)
            # print(msg)
            self.assertTrue(x > 0, msg=msg)

    def test_unitVector_topHalf(self):
        for i in range(1, 180):
            x, y = vector.unitVector(i)
            msg = "({}, {}) = {}°".format(x, y, i)
            # print(msg)
            self.assertTrue(y > 0, msg=msg)

    def test_vectorAngle_knownAngles(self):
        v1 = (1, 0)
        vsTest = [((1, 0), 0), ((5, 0), 0), ((1, 1), 45), ((3, 3), 45), ((0, 1), 90), ((0, 6), 90), ((-1, 1), 135),
                  ((-3, 3), 135), ((-1, 0), 180), ((-5, 0), 180), ((-1, -1), 135), ((-3, -3), 135), ((0, -1), 90),
                  ((0, -6), 90), ((1, -1), 45), ((7, -7), 45)]
        expectedAnswers = [a for v, a in vsTest]
        calculatedAnswers = [round(vector._vectorAngle(v1, v)) for v, a in vsTest]
        self.assertEqual(expectedAnswers, calculatedAnswers)

    def test_vectorLength_unitVectors(self):
        for theta in range(-180, 180):
            v = vector.unitVector(theta)
            self.assertAlmostEqual(1.0, vector._vectorLength(v), msg=v)

    def test_vectorLength_345(self):
        v = (3, 4)
        self.assertEqual(5, vector._vectorLength(v))

    def test_vectorLength_435(self):
        v = (4, 3)
        self.assertEqual(5, vector._vectorLength(v))

    def test_vectorLength_unitVectors(self):
        for theta in range(-180, 180):
            v = vector.unitVector(theta)
            self.assertAlmostEqual(1.0, vector._vectorLength(v), msg=v)



class TestVector(unittest.TestCase):
    def test_vectorLength_unitVectors(self):
        for theta in range(-180, 180):
            v = bitmap.Vector.unit(theta)
            self.assertAlmostEqual(1.0, v.magnitude(v), msg=v)

    def test_vectorLength_345(self):
        v = (3, 4)
        self.assertEqual(5, vector._vectorLength(v))

    def test_vectorLength_435(self):
        v = (4, 3)
        self.assertEqual(5, vector._vectorLength(v))

    def test_vectorLength_unitVectors(self):
        for theta in range(-180, 180):
            v = vector.unitVector(theta)
            self.assertAlmostEqual(1.0, vector._vectorLength(v), msg=v)

if __name__ == '__main__':
    unittest.main()
