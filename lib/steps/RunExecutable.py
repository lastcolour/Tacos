from .Step import Step
from lib.Logger import Log

import os
import subprocess
import pathlib
import platform

class RunExecutable(Step):
    def __init__(self):
        Step.__init__(self)
        self._cwd = None
        self._process = None
        self._args = None
        self._createCwd = None

    def serialize(self, jsonNode):
        self._process = jsonNode["process"]
        self._cwd = jsonNode["cwd"]
        self._args = jsonNode["args"]
        self._createCwd = jsonNode["createCwd"]

    def _getExecutableName(self):
        if platform.system() == "Windows":
            res = "{0}.exe".format(self._process)
        else:
            res = self._process
        return pathlib.Path(res).resolve().__str__()

    def run(self):
        self._cwd = pathlib.Path(self._cwd).resolve().__str__()
        if not os.path.exists(self._cwd):
            if not self._createCwd:
                Log.error("Can't find cwd to start process: {0}".format(self._cwd))
                return False
            else:
                Log.debug("Create cwd for process: {0}".format(self._cwd))
                os.makedirs(self._cwd)
        exeName = self._getExecutableName()
        if not os.path.exists(exeName):
            Log.error("Can't find executable: '{0}'".format(exeName))
            return False
        runArgs = [self._getExecutableName(), ]
        runArgs.extend(self._args)
        Log.debug("Start process: {0}".format(" ".join(runArgs)))
        process = subprocess.Popen(runArgs, cwd=self._cwd)
        retCode = process.wait()
        if retCode != 0:
            return False
        return True