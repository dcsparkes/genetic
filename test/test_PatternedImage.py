"""
Test module for patterned Image generation.
"""
import unittest


from patternedimage import PatternedImage

class TestHelperFunctions(unittest.TestCase):
    def test__parseColours_None(self):
        self.assertEqual([(255, 255, 255)], PatternedImage._parseColours(None))

    def test__parseColours_0(self):
        self.assertEqual([(0, 0, 0)], PatternedImage._parseColours(0))

    def test__parseColours_255(self):
        self.assertEqual([(255, 255, 255)], PatternedImage._parseColours(255))

    def test__parseColours_tuple(self):
        self.assertEqual([(100, 80, 60)], PatternedImage._parseColours((100, 80, 60)))

    def test__parseColours_tuple_malformed(self):
        cs = PatternedImage._parseColours((100, 80))
        self.assertEqual(1, len(cs))
        self.assertEqual(3, len(cs[0]))
        self.assertEqual((100, 80), cs[0][:2])

    def test__parseColours_tupleList(self):
        l = [(100, 80, 60), (209, 123, 193), (0, 0, 0), (255, 255, 255)]
        self.assertEqual(l, PatternedImage._parseColours(l))


if __name__ == '__main__':
    unittest.main()
