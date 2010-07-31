
import unittest
from nose import SkipTest

from com.rackspace.cloud.servers.api.client.tests import css, flavorManager, \
                                                         imageManager

fm = flavorManager
im = imageManager

from functools import partial
getFList = partial(fm.createListP, True)
getIList = partial(im.createListP, True)

class TestLimits(unittest.TestCase):
    """
    Test getting offset/limit sets by pulling out top and bottom pairs using
    the limit and offset parameters and comparing the results against slices
    out of the full list obtained without limit and offset pairs i.e. the
    whole list.
    """
    fullFList = None
    fullIList = None

    @classmethod
    def setUp(cls):
        """
        Get the full list of flavors against which to compare.
        """
        cls.fullFList = fm.createList(detail=True)
        cls.fullIList = im.createList(detail=True)

    def test_getBottomTwoFlavors(self):
        bottomTwo = getFList(0, 2)
        flBottomTwo = TestLimits.fullFList[:2]
        self.assertEqual(bottomTwo, flBottomTwo)

    def test_topTwoFlavors(self):
        top = len(TestLimits.fullFList) - 2  # get top 2
        topTwo = getFList(top, 2)
        fullListTopTwo = TestLimits.fullFList[-2:] # slice off top 2
        self.assertEqual(topTwo, fullListTopTwo)

    def test_getBottomTwoImages(self):
        bottomTwo = getIList(0, 2)
        ilBottomTwo = TestLimits.fullIList[:2]
        self.assertEqual(bottomTwo, ilBottomTwo)

    def test_topTwoImages(self):
        top = len(TestLimits.fullIList) - 2  # get top 2
        topTwo = getIList(top, 2)
        fullListTopTwo = TestLimits.fullIList[-2:] # slice off top 2
        self.assertEqual(topTwo, fullListTopTwo)

if __name__ == '__main__':
    unittest.main()
