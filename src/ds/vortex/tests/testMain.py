import unittest


def createTestSuites():
    tests = ["testEdge", "testGraph", "testBaseNodes", "testBasicMathNodes", "testPlug"]

    suites = [unittest.defaultTestLoader.loadTestsFromName("ds.vortex.tests."+name) for name in tests]
    testSuite = unittest.TestSuite(suites)
    return testSuite


if __name__ == "__main__":
    from ds.vortex import customLogger

    logger = customLogger.getCustomLogger()
    unittest.main(verbosity=2)
    unittest.TextTestRunner(verbosity=2).run(createTestSuites())
