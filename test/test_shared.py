from shared import shared
import unittest


class MyTestCase(unittest.TestCase):
    def test_clipValue(self):
        for i in range(-256, 512):
            clipped = shared.clipValue(i)
            if i < 0:
                self.assertEqual(0, clipped)
            elif i > 255:
                self.assertEqual(255, clipped)
            else:
                self.assertEqual(i, clipped)

    def test_reorient_unique(self):
        uniqueTopRows = set()
        vs = ([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        for i in range(8):
            reoriented = shared.reorient(vs, orientation=i)
            topRow = reoriented[0]
            uniqueTopRows.add(tuple(topRow))
            print("topRow({}) = {}".format(i, topRow))
        self.assertEqual(8, len(uniqueTopRows))

    def test_reorient_centreUnchanged(self):
        uniqueTopRows = set()
        vs = ([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        for i in range(8):
            reoriented = shared.reorient(vs, orientation=i)
            self.assertEqual(5, reoriented[1][1])

if __name__ == '__main__':
    unittest.main()
