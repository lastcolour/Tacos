from lib.steps.PyTests import PyTests

import unittest
import pathlib

class TestPyTests(unittest.TestCase):

    def _getTestFolderPath(self):
        path = pathlib.Path(__file__).parent
        return "{0}/testData/testTests".format(path)

    def test_run_successed(self):
        data = {
            "path":self._getTestFolderPath(),
            "pattern":"*.py"
        }
        step = PyTests()
        step.serialize(data)
        self.assertTrue(step.run())