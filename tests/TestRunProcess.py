from lib.steps.RunExecutable import RunExecutable

import unittest

import TestUtils

class TestRunProcess(unittest.TestCase):
    def test_run_invalid_process(self):
        data = {
            "cwd":"",
            "process":"win_dir",
            "createCwd":False,
            "args":[
            ]
        }
        runProcess = RunExecutable()
        runProcess.serialize(data)
        self.assertFalse(runProcess.run())

    def test_run_valid_process(self):
        data = {
            "cwd":"",
            "createCwd":False,
            "process":"dir",
            "args":[
            ]
        }
        runProcess = RunExecutable()
        runProcess.serialize(data)
        self.assertFalse(runProcess.run())