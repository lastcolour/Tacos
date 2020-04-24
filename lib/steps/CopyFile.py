from .Step import Step
from lib.Logger import Log


import os
import glob
import pathlib
import shutil

class CopyFile(Step):
    def __init__(self):
        Step.__init__(self)
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

class CopyCompiledBinaries(Step):
    def __init__(self):
        Step.__init__(self)
        self._platform = None
        self._to = None
        self._from = None
        self._name = None
        self._type = None
        self._force = None

    def serialize(self, jsonNode):
        self._platform = jsonNode["platform"]
        self._to = jsonNode["to"]
        self._from = jsonNode["from"]
        self._name = jsonNode["name"]
        self._type = jsonNode["type"]
        self._force = jsonNode["force"]

    def run(self):
        if self._platform not in ["Windows", "Linux", "Android"]:
            Log.error("Unsupported platform: {0}".format(self._platform))
            return False
        if self._type not in ["shared", "static", "all"]:
            Log.error("Unsupported binaries type: {0}".format(self._type))
            return False
        if not os.path.exists(self._from):
            Log.error("Source folder doesn't exist: {0}".format(self._from))
            return False
        if len(self._name) == 0:
            Log.error("Target file name is empty")
            return False
        if not os.path.exists(self._to):
            os.makedirs(self._to)
        for item in os.listdir(self._from):
            filePath = "{0}/{1}".format(self._from, item)
            if not os.path.isdir(filePath) and self._needCopy(item):
                Log.debug("Copy file : {0}, to folder: {1}".format(filePath, self._to))
                targetPath = "{0}/{1}".format(self._to, item)
                shutil.copy(filePath, targetPath)
        return True

    def _checkFileName(self, fileName):
        if self._platform == "Windows":
            formatTypes = [
                "{0}",
                "{0}32",
                "{0}d",
                "{0}dll"
            ]
        else:
            formatTypes = [
                "lib{0}"
            ]
        for formatType in formatTypes:
            if formatType.format(self._name) == fileName:
                return True
        return False

    def _checkExtension(self, fileExt):
        validExtensions = []
        if self._platform == "Windows":
            if self._type == "static" or self._type == "all":
                validExtensions.append("lib")
            if self._type == "shared" or self._type == "all":
                validExtensions.append("dll")
                validExtensions.append("exp")
            validExtensions.append("pdb")
        else:
            if self._type == "static" or self._type == "all":
                validExtensions.append("a")
            if self._type == "shared" or self._type == "all":
                validExtensions.append("so")
        if fileExt in validExtensions:
            return True
        return False

    def _needCopy(self, item):
        tokens = item.split(".")
        if len(tokens) != 2:
            return False
        fileName, fileExt = item.split(".")
        fileName = fileName.lower()
        if self._checkExtension(fileExt) and self._checkFileName(fileName):
            return True
        return False