from .Step import Step
from .Logger import Log

import os
import glob
import pathlib
import shutil

def _checkPath(path):
    return True

class CopyFile(Step):
    def __init__(self):
        self._target = None
        self._to = None
        self._force = False

    def serialize(self, jsonNode):
        self._target = jsonNode["target"]
        self._to = jsonNode["to"]

    def run(self):
        if not os.path.exists(self._target):
            Log.warning("Can't find folder to copy: {0}".format(self._target))
            return False
        if not os.path.exists(self._to):
            os.makedirs(self._to)
        targetName = pathlib.Path(self._target).name
        targetPath = "{0}/{1}".format(self._to, targetName)
        if os.path.exists(targetPath):
            if not self._force:
                Log.debug("Skip copy because target already exist in destination: {0}".format(targetPath))
                return True
            else:
                if os.path.isdir(targetPath):
                    Log.debug("Remove target before coping: {0}".format(targetPath))
                    shutil.rmtree(targetPath)
        if os.path.isdir(self._target):
            Log.debug("Copy folder: {0}, to folder: {1}".format(self._target, self._to))
            shutil.copytree(self._target, targetPath)
        else:
            Log.debug("Copy file : {0}, to folder: {1}".format(self._target, self._to))
            shutil.copy(self._target, targetPath)
        return True

class CopyFilesByMask(Step):
    def __init__(self):
        self._target = None
        self._to = None
        self._mask = None

    def serialize(self, jsonNode):
        self._target = jsonNode["target"]
        self._to = jsonNode["to"]
        self._mask = jsonNode["mask"]

    def run(self):
        return True