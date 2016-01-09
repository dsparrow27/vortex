import unittest


def createTestSuites():
    tests = ["ds.vortex.tests.testEdge", "ds.vortex.tests.testGraph", "ds.vortex.tests.testNode",
             "ds.vortex.tests.testPlug"]

    suites = [unittest.defaultTestLoader.loadTestsFromName(name) for name in tests]
    testSuite = unittest.TestSuite(suites)
    return testSuite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(createTestSuites())
