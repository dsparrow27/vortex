import unittest
from ds.vortex.core import basePlug as plugs


class TestPlug(unittest.TestCase):
    def setUp(self):
        self.plug = plugs.InputPlug(name="testName", node="testNode")

    def testIsInput(self):
        self.assertTrue(self.plug.isInput())
        self.assertFalse(self.plug.isOutput())

    def testConnect(self):
        inputAttr = plugs.InputPlug(name="testInput", node="testNode")
        outputAttr = plugs.OutputPlug(name="testOutput", node="testNode")
        floatTypeAttr = plugs.OutputPlug(name="testOutput", node="testNode")
        self.plug.connect(outputAttr)
        self.plug.connect(floatTypeAttr)
        self.assertTrue(self.plug.isConnected())
        self.assertIsNone(self.plug.connect(inputAttr))  # failed to connect

    def remove(self):
        floatTypeAttr = plugs.OutputPlug(name="testOutput", node="testNode")
        self.plug.connect(floatTypeAttr)
        self.plug.disconnect(floatTypeAttr)
        self.assertEquals(len(self.plug), 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
