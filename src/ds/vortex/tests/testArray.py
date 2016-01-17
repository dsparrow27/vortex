import unittest

from ds.vortex.nodes.array import append
from ds.vortex.nodes.array import extend
from ds.vortex.nodes.array import indexByValue

from ds.vortex.nodes.array import pop


class TestAppendArray(unittest.TestCase):
    def setUp(self):
        self.node = append.ArrayAppend("append")

    def testAppendFails(self):
        pass

    def testAppendPasses(self):
        pass


class TestExtendArray(unittest.TestCase):
    def setUp(self):
        self.node = extend.ArrayExtend("extend")

    def testExtendFails(self):
        pass

    def testExtendPasses(self):
        pass


class TestIndexByValue(unittest.TestCase):
    def setUp(self):
        self.node = indexByValue.ArrayIndexNode("indexByArray")

    def testIndexFails(self):
        pass

    def testIndexPasses(self):
        pass


class TestPopArray(unittest.TestCase):
    def setUp(self):
        self.node = pop.PopIndex("append")

    def testPopFails(self):
        pass

    def testPopPasses(self):
        pass
