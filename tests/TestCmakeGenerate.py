import unittest
import pathlib
import os

import TestUtils

from lib.CmakeGenerate import CmakeGenerate

class TestCmakeGenerate(unittest.TestCase):

    def _getTestProjectPath(self):
        path = pathlib.Path(__file__).parent
        return "{0}/testData/testProject".format(path)

    def _getOutDir(self):
        return TestUtils.CreateAndGetTMPDir()

    @staticmethod
    def tearDownClass():
        TestUtils.RemoteTMPDir()

    def test_cmake_in_empty_folder(self):
        cmakeGen = CmakeGenerate()
        data = {
            "run_dir":"",
            "build_type":"Invalid",
            "out_dir":""
        }
        self.assertTrue(cmakeGen.serialize(data))
        self.assertTrue(cmakeGen.init())
        self.assertFalse(cmakeGen.run())


    def test_cmake_invalid_build_type(self):
        cmakeGen = CmakeGenerate()
        data = {
            "run_dir":self._getTestProjectPath(),
            "build_type": "Invalid",
            "out_dir":""
        }
        self.assertTrue(cmakeGen.serialize(data))
        self.assertTrue(cmakeGen.init())
        self.assertFalse(cmakeGen.run())

    def test_cmake_invalid_out_dir(self):
        cmakeGen = CmakeGenerate()
        data = {
            "run_dir":self._getTestProjectPath(),
            "build_type": "Debug",
            "out_dir":""
        }
        self.assertTrue(cmakeGen.serialize(data))
        self.assertTrue(cmakeGen.init())
        self.assertFalse(cmakeGen.run())

    def test_cmake_build_test_project(self):
        cmakeGen = CmakeGenerate()
        data = {
            "run_dir":self._getTestProjectPath(),
            "build_type": "Debug",
            "out_dir":self._getOutDir()
        }
        self.assertTrue(cmakeGen.serialize(data))
        self.assertTrue(cmakeGen.init())
        self.assertTrue(cmakeGen.run())

        outDir = self._getOutDir()
        items = os.listdir(outDir)
        self.assertGreater(len(items), 0)