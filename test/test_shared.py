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



if __name__ == '__main__':
    unittest.main()
