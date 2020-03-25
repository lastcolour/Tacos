import unittest
import pathlib
import os
import subprocess

import TestUtils

from lib.CmakeGenerate import CmakeGenerate

class TestCmakeGenerate(unittest.TestCase):

    def _getTestProjectPath(self):
        path = pathlib.Path(__file__).parent
        return "{0}/testData/testProject".format(path)

    def _getOutDir(self):
        return TestUtils.CreateAndGetTMPDir()

    def tearDown(self):
        TestUtils.RemoteTMPDir()

    def test_cmake_in_empty_folder(self):
        cmakeGen = CmakeGenerate()
        data = {
            "run_dir":"",
            "build_type":"Invalid",
            "out_dir":""
        }
        cmakeGen.serialize(data)
        self.assertFalse(cmakeGen.run())


    def test_cmake_invalid_build_type(self):
        cmakeGen = CmakeGenerate()
        data = {
            "run_dir":self._getTestProjectPath(),
            "build_type": "Invalid",
            "out_dir":""
        }
        cmakeGen.serialize(data)
        self.assertFalse(cmakeGen.run())

    def test_cmake_invalid_out_dir(self):
        cmakeGen = CmakeGenerate()
        data = {
            "run_dir":self._getTestProjectPath(),
            "build_type": "Debug",
            "out_dir":""
        }
        cmakeGen.serialize(data)
        self.assertFalse(cmakeGen.run())

    def test_cmake_build_test_project(self):
        cmakeGen = CmakeGenerate()
        data = {
            "run_dir":self._getTestProjectPath(),
            "build_type": "Debug",
            "out_dir":self._getOutDir()
        }
        cmakeGen.serialize(data)
        self.assertTrue(cmakeGen.run())

        outDir = self._getOutDir()
        items = os.listdir(outDir)
        self.assertGreater(len(items), 0)

        buildLogFile = "{0}/_cmake/{1}/cmake_gen_log.txt".format(self._getOutDir(), "Debug")
        cmakeLogFile = "{0}/_cmake/{1}/cmake_build_log.txt".format(self._getOutDir(), "Debug")

        self.assertTrue(os.path.exists(buildLogFile))
        self.assertTrue(os.path.exists(cmakeLogFile))

    def test_cmake_add_definition(self):
        cmakeGen = CmakeGenerate()
        data = {
            "run_dir":self._getTestProjectPath(),
            "build_type": "Debug",
            "out_dir":self._getOutDir(),
            "defs":{
                "General": {
                    "PRINT_MESSAGE":"Hello From Tests!"
                }
            }
        }
        cmakeGen.serialize(data)
        self.assertTrue(cmakeGen.run())

        binOutDir = "{0}/{1}".format(self._getOutDir(), data["build_type"])
        binOutDir = binOutDir.replace('\\', '/')

        exePath = "{0}/TestProject.exe".format(binOutDir)
        self.assertTrue(os.path.exists(exePath))

        res = subprocess.run(args=[exePath], cwd=binOutDir, capture_output=True)
        self.assertEqual(res.returncode, 0)

        stderr = str(res.stderr, 'ascii').strip()
        self.assertEqual(stderr, '')

        stdout = str(res.stdout, 'ascii').strip()
        self.assertEqual(stdout, data["defs"]["General"]["PRINT_MESSAGE"])