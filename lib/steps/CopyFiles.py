from .Step import Step
from lib.Logger import Log

import pathlib
import os
import glob
import pathlib
import shutil
import glob

class CopyFiles(Step):
    def __init__(self):
        Step.__init__(self)
        self._targets = None
        self._from = None
        self._to = None
        self._force = False

    def serialize(self, jsonNode):
        self._targets = jsonNode["targets"]
        self._to = jsonNode["to"]
        self._from = jsonNode["from"]
        self._force = jsonNode["force"]

        self._to = pathlib.Path(self._to).resolve().__str__()

    def run(self):
        if not os.path.exists(self._from):
            Log.error("Can't find 'from' path: '{0}'".format(self._from))
            return False
        if not os.path.isdir(self._from):
            Log.error("The 'from' path: '{0}' is not a dir".format(self._from))
            return False
        for target in self._targets:
            targetPath = "{0}/{1}".format(self._from, target)
            matchFiles = glob.glob(targetPath)
            for fileName in matchFiles:
                self._copySingleFile(fileName)
        return True

    def _copySingleFile(self, fileName):
        if not os.path.exists(self._to):
            os.makedirs(self._to)
        targetName = pathlib.Path(fileName).name
        targetPath = "{0}/{1}".format(self._to, targetName)
        if os.path.exists(targetPath):
            if not self._force:
                Log.debug("Skip copy because target already exist in destination: {0}".format(targetPath))
                return True
            else:
                if os.path.isdir(targetPath):
                    Log.debug("Remove target before coping: {0}".format(targetPath))
                    shutil.rmtree(targetPath)
        if os.path.isdir(fileName):
            Log.debug("Copy folder: {0}, to folder: {1}".format(fileName, self._to))
            shutil.copytree(fileName, targetPath)
        else:
            Log.debug("Copy file : {0}, to folder: {1}".format(fileName, self._to))
            shutil.copy(fileName, targetPath)