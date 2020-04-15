import unittest
import os
import shutil
import pathlib

from lib.steps.CopyFile import CopyFile

import TestUtils

class TestCopyFile(unittest.TestCase):

    @staticmethod
    def tearDownClass():
        TestUtils.RemoteTMPDir()

    def setUp(self):
        tmpFolder = "{0}/tmp".format(TestUtils.CreateAndGetTMPDir())
        if not os.path.exists(tmpFolder):
            os.makedirs(tmpFolder)

    def tearDown(self):
        dirToRemove = "{0}/tmp".format(TestUtils.CreateAndGetTMPDir())
        if os.path.exists(dirToRemove):
            shutil.rmtree(dirToRemove)

    def test_copy_invalid_file(self):
        testFileName = "test_file.txt"
        data = {
            "target":"{0}/{1}".format(TestUtils.CreateAndGetTMPDir(), testFileName),
            "to":"{0}/tmp".format(TestUtils.CreateAndGetTMPDir()),
            "force":False
        }
        self.assertFalse(os.path.exists(data["target"]))
        resFile = "{0}/{1}".format(data["to"], testFileName)

        step = CopyFile()
        step.serialize(data)
        self.assertFalse(step.run())
        self.assertFalse(os.path.exists(resFile))

    def test_copy_normal(self):
        testFileName = "test_file.txt"
        data = {
            "target":"{0}/{1}".format(TestUtils.CreateAndGetTMPDir(), testFileName),
            "to":"{0}/tmp".format(TestUtils.CreateAndGetTMPDir()),
            "force":False
        }

        with open(data["target"], 'w+') as fileObj:
            fileObj.write("1")

        resFile = "{0}/{1}".format(data["to"], testFileName)

        step = CopyFile()
        step.serialize(data)
        self.assertTrue(step.run())
        self.assertTrue(os.path.exists(resFile))

        with open(resFile, 'r') as fileObj:
            data = fileObj.read()
        self.assertEqual(data, "1")

    def test_copy_force(self):
        testFileName = "test_file.txt"
        data = {
            "target":"{0}/{1}".format(TestUtils.CreateAndGetTMPDir(), testFileName),
            "to":"{0}/tmp".format(TestUtils.CreateAndGetTMPDir()),
            "force":True
        }

        with open(data["target"], 'w+') as fileObj:
            fileObj.write("1")

        resFile = "{0}/{1}".format(data["to"], testFileName)
        with open(resFile, 'w+') as fileObj:
            fileObj.write("2")

        step = CopyFile()
        step.serialize(data)
        self.assertTrue(step.run())
        self.assertTrue(os.path.exists(resFile))

        with open(resFile, 'r') as fileObj:
            data = fileObj.read()
        self.assertEqual(data, "2")