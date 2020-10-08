from .Step import Step
from lib.Logger import Log

import os
import subprocess
import io
import sys
import shutil
import platform
import pathlib

class _CmakeVerbosity:
    Silent = 1
    All = 2

class CmakeGenerate(Step):

    _GENERATE_LOG_FILE = "cmake_gen_log.txt"
    _BUILD_LOG_FILE = "cmake_build_log.txt"

    def __init__(self):
        Step.__init__(self)
        self._out_dir = None
        self._run_dir = None
        self._build_type = None
        self._build_platform = None
        self._generator = None
        self._arch = None
        self._cmake_out_dir = None
        self._bin_out_dir = None
        self._separate_bins = None
        self._verbosity = _CmakeVerbosity.All
        self._defs = []

    def serialize(self, node):
        self._separate_bins = node["separate_bins"]
        self._out_dir = node["out_dir"]
        self._run_dir = node["run_dir"]
        self._build_type = node["build_type"]
        self._verbosity = self._getVerboisty(node)
        if "generator" in node:
            self._generator = node["generator"]
        if "arch" in node:
            self._arch = node["arch"]
        if "defs" in node:
            self._defs = node["defs"]
        self._build_platform = platform.system()

    def run(self):
        if not self._checkBuildType():
            return False
        if not self._checkRunDir():
            return False
        if not self._createOutDir():
            return False
        if not self._runCmakeGenerate():
            return False
        return self._runCmakeBuild()

    def _checkRunDir(self):
        self._run_dir = pathlib.Path(self._run_dir).resolve().__str__()
        if not os.path.exists(self._run_dir):
            Log.error("Can't find run dir: '{0}'".format(self._run_dir))
            return False
        cmakeFile = "{0}/CMakeLists.txt".format(self._run_dir)
        if not os.path.exists(cmakeFile):
            Log.error("Can't find 'CMakeLists.txt' in '{0}'".format(self._run_dir))
            return False
        return True

    def _runCmakeGenerate(self):
        if not self._checkCmakeExists():
            return False
        if not self._generateCmakeProject():
            return False
        return True

    def _buildCmakeRunArgs(self):
        cmakeArgs = [
            'cmake',
            '-S.',
            '-B{0}'.format(self._cmake_out_dir),
            '-DCMAKE_BUILD_TYPE={0}'.format(self._build_type)
        ]

        if self._separate_bins:
            cmakeArgs.extend([
                '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG={0}/Debug'.format(self._bin_out_dir),
                '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE={0}/Release'.format(self._bin_out_dir),
                '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELWITHDEBINFO={0}/RelWithDebInfo'.format(self._bin_out_dir),

                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG={0}/Debug'.format(self._bin_out_dir),
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE={0}/Release'.format(self._bin_out_dir),
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELWITHDEBINFO={0}/RelWithDebInfo'.format(self._bin_out_dir),

                '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG={0}/Debug'.format(self._bin_out_dir),
                '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE={0}/Release'.format(self._bin_out_dir),
                '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO={0}/RelWithDebInfo'.format(self._bin_out_dir),

                '-DCMAKE_COMPILE_PDB_OUTPUT_DIRECTORY_DEBUG={0}/Debug'.format(self._bin_out_dir),
                '-DCMAKE_COMPILE_PDB_OUTPUT_DIRECTORY_RELEASE={0}/Release'.format(self._bin_out_dir),
                '-DCMAKE_COMPILE_PDB_OUTPUT_DIRECTORY_RELWITHDEBINFO={0}/RelWithDebInfo'.format(self._bin_out_dir)
            ])

        if self._generator is None:
            Log.debug("Cmake will use default platform code generator")
            pass
        else:
            cmakeArgs.append('-G"{0}"'.format(self._generator))
            if self._arch is not None:
                cmakeArgs.append('-A{0}'.format(self._arch))
        defs = self._getCmakeDefs()
        cmakeArgs.extend(defs)
        return cmakeArgs

    def _buildCompileRunArgs(self):
        runArgs = [
            "cmake",
            "--build",
            ".",
            "--target",
            "{0}".format(self._getBuildTarget()),
            "--config",
            self._build_type
        ]
        return runArgs

    def _getBuildTarget(self):
        if self._build_platform == "Windows":
            return "ALL_BUILD"
        else:
            return "all"

    def _runCmakeBuild(self):
        runArgs = self._buildCompileRunArgs()
        logFile = CmakeGenerate._BUILD_LOG_FILE
        return self._runCmake(runArgs, self._cmake_out_dir, logFile)

    def _generateCmakeProject(self):
        runArgs = self._buildCmakeRunArgs()
        logFile = CmakeGenerate._GENERATE_LOG_FILE
        return self._runCmake(runArgs, self._run_dir, logFile)

    def _checkCmakeExists(self):
        runArgs = ["cmake", "--version"]
        runCwd = None
        logFile = None
        return self._runCmake(runArgs, runCwd, logFile)

    def _checkBuildType(self):
        validBuildTypes = ["Release", "Debug", "RelWithDebInfo", "MinSizeRel"]
        if self._build_type not in validBuildTypes:
            Log.error("Invalid build type: '{0}'".format(self._build_type))
            return False
        return True

    def _createOutDir(self):
        self._out_dir = pathlib.Path(self._out_dir).resolve().__str__()
        self._bin_out_dir = self._fixPath("{0}".format(self._out_dir))
        self._cmake_out_dir = "{0}/_cmake".format(self._bin_out_dir)
        if len(self._out_dir) == 0:
            Log.error("Invalid out dir")
            return False
        try:
            if not os.path.exists(self._out_dir):
                os.makedirs(self._out_dir)
        except Exception as ex:
            Log.error("Can't create out dir: '{0}'. Error: '{1}'".format(self._out_dir, ex.__str__()))
            return False
        else:
            pass
        return True

    def _runCmake(self, runArgs, runCwd, logFile):
        if logFile is None:
            pipeObj = subprocess.DEVNULL
        else:
            pipeObj = self._createPipe(logFile)
        Log.debug("Start process: {0}".format(" ".join(runArgs)))
        if runCwd is not None:
            Log.debug("Process cwd: '{0}'".format(runCwd))
        process = subprocess.Popen(runArgs, cwd=runCwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for bLine in process.stdout:
            utfLine = bLine.decode('utf-8')
            if self._verbosity == _CmakeVerbosity.All:
                print(utfLine[:-1])
            if pipeObj != subprocess.DEVNULL:
                pipeObj.write(utfLine)
        retCode = process.wait()
        if pipeObj != subprocess.DEVNULL:
            Log.debug("Process output saved to: '{0}'".format(logFile))
            if self._verbosity != _CmakeVerbosity.All and retCode != 0:
                self._printRunResults(retCode, pipeObj)
            pipeObj.close()
        return retCode is 0

    def _getCmakeDefs(self):
        cmakeDefs = []
        if "General" in self._defs:
            for item in self._defs["General"]:
                cmakeDefs.append("-D{0}={1}".format(item, self._defs["General"][item]))
        if self._build_type in self._defs:
            for item in self._defs[self._build_type]:
                cmakeDefs.append("-D{0}={1}".format(item, self._defs[self._build_type][item]))
        if self._build_platform in self._defs:
            for item in self._defs[self._build_platform]:
                cmakeDefs.append("-D{0}={1}".format(item, self._defs[self._build_platform][item]))
        return cmakeDefs

    def _getVerboisty(self, node):
        if "verbosity" not in node:
            return _CmakeVerbosity.All
        verbStr = node["verbosity"]
        if verbStr == "silent":
            return _CmakeVerbosity.Silent
        else:
            Log.error("Uknown verbosity level: '{0}'".format(verbStr))
            raise RuntimeError("Can't parse verbosity level")
        return _CmakeVerbosity.All

    def _createPipe(self, filepath):
        if not os.path.exists(self._cmake_out_dir):
            os.makedirs(self._cmake_out_dir)
        tmpFilePath = "{0}/{1}".format(self._cmake_out_dir, filepath)
        return open(tmpFilePath, 'w+')

    def _printRunResults(self, retCode, pipeObj):
        pipeObj.tell()
        pipeObj.seek(0)
        printFunc = Log.info
        if retCode is not 0:
            printFunc = Log.warning
        fileContent = pipeObj.read()
        for item in fileContent.split('\n'):
            printFunc("\t{0}".format(item))

    def _fixPath(self, path):
        path = os.path.abspath(path)
        path = path.replace("\\", "/")
        return path