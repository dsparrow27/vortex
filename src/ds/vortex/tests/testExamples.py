import unittest
from ds.vortex.examples import simple


class TestExampleGraphs(unittest.TestCase):
    def testSimple(self):
        self.assertEquals(simple.testExample(), 26)
