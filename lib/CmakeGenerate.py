from .Step import Step
from .Logger import Log

import os
import subprocess

class CmakeGenerate(Step):
    def __init__(self):
        Step.__init__(self)
        self._out_dir = None
        self._run_dir = None
        self._build_type = None
        self._generator = None
        self._arch = None
        self._cmake_out_dir = None
        self._bin_out_dir = None
        self._defs = []

    def serialize(self, node):
        self._out_dir = node["out_dir"]
        self._run_dir = node["run_dir"]
        self._build_type = node["build_type"]
        if "generator" in node:
            self._generator = node["generator"]
        if "arch" in node:
            self._arch = node["arch"]
        if "defs" in node:
            self._defs = node["defs"]
        self._cmake_out_dir = "{0}/_cmake/{1}".format(self._out_dir, self._build_type)
        self._bin_out_dir = self._out_dir
        return True

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
        if not os.path.exists(self._run_dir):
            Log.error("Can't find run dir: '{0}'".format(self._run_dir))
            return False
        cmakeFile = "{0}/CMakeLists.txt".format(self._run_dir)
        if not os.path.exists(cmakeFile):
            Log.error("Can't find CMakeLists.txt in '{0}'".format(self._run_dir))
            return False
        return True

    def _runCmakeGenerate(self):
        if not self._checkCmakeExists():
            return False
        if not self._generateCmakeProject():
            return False
        return True

    def _runCmakeBuild(self):
        try:
            ret = subprocess.run(["cmake", "--build", "."], cwd="{0}".format(self._cmake_out_dir))
            ret.check_returncode()
        except Exception as ex:
            Log.error("Can't build cmake solution. Error: {0}".format(ex.__str__()))
            return False
        else:
            pass
        return True

    def _buildCmakeRunArgas(self):
        cmakeArgs = [
            'cmake',
            '-S.',
            '-B{0}'.format(self._cmake_out_dir),
            '-DCMAKE_BUILD_TYPE={0}'.format(self._build_type),
            '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY={0}'.format(self._bin_out_dir),
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={0}'.format(self._bin_out_dir),
            '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY={0}'.format(self._bin_out_dir)
        ]
        if self._generator is None:
            Log.warning("Cmake will use default platform code genrator")
        else:
            cmakeArgs.append('-G"{0}"'.format(self._generator))
            if self._arch is not None:
                cmakeArgs.append('-A{0}'.format(self._arch))
        defs = self._getCmakeDefs()
        cmakeArgs.extend(defs)
        return cmakeArgs

    def _generateCmakeProject(self):
        runArgs = self._buildCmakeRunArgas()
        Log.info("Start process: {0}".format(" ".join(runArgs)))
        try:
            res = subprocess.run(args=runArgs, cwd=self._run_dir)
            res.check_returncode()
        except Exception as ex:
            Log.error("CFailed to generate cmake solutin. Error: {0}".format(ex.__str__()))
            return False
        else:
            pass
        return True

    def _checkCmakeExists(self):
        try:
            res = subprocess.run(args=["cmake", "--version"])
            res.check_returncode()
        except Exception as ex:
            Log.error("Can't find cmake bin: {0}".format(ex.__str__()))
            return False
        else:
            return True

    def _checkBuildType(self):
        validBuildTypes = ["Release", "Debug", "RelWithDebInfo", "MinSizeRel"]
        if self._build_type not in validBuildTypes:
            Log.error("Invalid build type: '{0}'".format(self._build_type))
            return False
        return True

    def _createOutDir(self):
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

    def _getCmakeDefs(self):
        cmakeDefs = []
        for item in self._defs:
            cmakeDefs.append("-D{0}={1}".format(item, self._defs[item]))
        return cmakeDefs