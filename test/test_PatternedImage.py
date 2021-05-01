"""
Test module for patterned Image generation.
"""
import unittest
from patternedimage import PatternedImage


class TestHelperFunctions(unittest.TestCase):
    def test__generateGaussianFilename_bw(self):
        filename = PatternedImage._generateGaussianFilename((540, 1080), [(0, 0, 0), (255, 255, 255)])
        self.assertEqual("gaussians/540x1080/540x1080_0,0,0_255,255,255", filename)

    def test__generateGaussianDistributionFilename_default(self):
        filename = PatternedImage._generateGaussianDistributionFilename((540, 1080))
        self.assertEqual("gaussiandists/540x1080/540x1080.json", filename)

    def test__generateGaussianDistributionFilename_mus(self):
        filename = PatternedImage._generateGaussianDistributionFilename((540, 1080), mus=[0, 0])
        self.assertEqual("gaussiandists/540x1080/540x1080_μs(0,0).json", filename)

    def test__generateGaussianDistributionFilename_sigmas(self):
        filename = PatternedImage._generateGaussianDistributionFilename((1080, 540), sigmas=[10, 8])
        self.assertEqual("gaussiandists/1080x540/1080x540_σs(10,8).json", filename)

    def test__generateGaussianDistributionFilename_mus_sigmas(self):
        filename = PatternedImage._generateGaussianDistributionFilename((1080, 540), mus=[1080, 540], sigmas=[510, 80])
        self.assertEqual("gaussiandists/1080x540/1080x540_μs(1080,540)_σs(510,80).json", filename)

    def test__generate2DGaussianDistributions_size_x(self):
        xdim = 107
        ydim = 103
        dist = PatternedImage._generate2DGaussianDistribution((xdim, ydim))
        self.assertEqual(xdim, len(dist[0]))

    def test__generate2DGaussianDistributions_size_y(self):
        xdim = 6
        ydim = 7
        dist = PatternedImage._generate2DGaussianDistribution((xdim, ydim))
        self.assertEqual(ydim, len(dist))

    def test__generate2DGaussianDistributions_min_ge_0(self):
        xdim = 67
        ydim = 71
        dist = PatternedImage._generate2DGaussianDistribution((xdim, ydim))
        minval = min([min(row) for row in dist])
        print("minval = {}".format(minval))
        self.assertTrue(minval >= 0.0)

    def test__generate2DGaussianDistributions_max_le_1(self):
        xdim = 73
        ydim = 71
        dist = PatternedImage._generate2DGaussianDistribution((xdim, ydim))
        maxval = max([max(row) for row in dist])
        print("maxval = {}".format(maxval))
        self.assertTrue(maxval <= 1.0)

    def test__parseColours_None(self):
        self.assertEqual([(255, 255, 255)], PatternedImage._parseColoursList(None))

    def test__parseColours_0(self):
        self.assertEqual([(0, 0, 0)], PatternedImage._parseColoursList(0))

    def test__parseColours_255(self):
        self.assertEqual([(255, 255, 255)], PatternedImage._parseColoursList(255))

    def test__parseColours_tuple(self):
        self.assertEqual([(100, 80, 60)], PatternedImage._parseColoursList((100, 80, 60)))

    def test__parseColours_tuple_malformed(self):
        cs = PatternedImage._parseColoursList((100, 80))
        self.assertEqual(1, len(cs))
        self.assertEqual(3, len(cs[0]))
        self.assertEqual((100, 80), cs[0][:2])

    def test__parseColours_tupleList(self):
        l = [(100, 80, 60), (209, 123, 193), (0, 0, 0), (255, 255, 255)]
        self.assertEqual(l, PatternedImage._parseColoursList(l))


if __name__ == '__main__':
    unittest.main()
