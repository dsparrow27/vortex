import unittest
from ds.vortex.core import basePlug


class TestPlug(unittest.TestCase):
    pass
    # def setUp(self):
    #     self.plug = basePlug.BasePlug(name="testName", node="testNode", attributeType=float, io="input")
    #
    # def testEquality(self):
    #     """Tests Equality between two attributes via type and io
    #     """
    #     inputAttr = basePlug.BasePlug(name="testInput", node="testNode", attributeType=float, io="input")
    #     outputAttr = basePlug.BasePlug(name="testOutput", node="testNode", attributeType=float, io="output")
    #     intTypeAttr = basePlug.BasePlug(name="testInput", node="testNode", attributeType=int, io="input")
    #     self.assertEquals(self.plug, inputAttr)
    #     self.assertNotEquals(self.plug, outputAttr)
    #     self.assertNotEquals(self.plug, intTypeAttr)
    #
    # def testIsInput(self):
    #     self.assertTrue(self.plug.isInput())
    #     self.assertFalse(self.plug.isOutput())
    #
    # def testIsOutput(self):
    #     self.assertTrue(self.plug.isOutput())
    #     self.assertFalse(self.plug.isInput())
    #
    # def testApiType(self):
    #     self.assertEquals(self.plug.apiType, float)
    #
    # def testIsDirty(self):
    #     self.assertFalse(self.plug.dirty)
    #     self.plug.dirty = True
    #     self.assertTrue(self.plug.dirty)
    #
    # def testConnect(self):
    #     inputAttr = basePlug.BasePlug(name="testInput", node="testNode", attributeType=float, io="input")
    #     outputAttr = basePlug.BasePlug(name="testOutput", node="testNode", attributeType=float, io="output")
    #     floatTypeAttr = basePlug.BasePlug(name="testOutput", node="testNode", attributeType=float, io="output")
    #     self.plug.connect(outputAttr)
    #     self.plug.connect(floatTypeAttr)
    #     self.assertTrue(self.plug.isConnected())
    #     self.assertIsNone(self.plug.connect(inputAttr))  # failed to connect
    #
    # def remove(self):
    #     floatTypeAttr = basePlug.BasePlug(name="testOutput", node="testNode", attributeType=float, io="output")
    #     self.plug.connect(floatTypeAttr)
    #     self.assertTrue(self.plug.remove(floatTypeAttr))
if __name__ == "__main__":
    unittest.main(verbosity=2)
