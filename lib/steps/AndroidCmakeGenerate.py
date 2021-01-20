from .CmakeGenerate import CmakeGenerate
from lib.Logger import Log

import os
import json
import pathlib

class AndroidCmakeGenerate(CmakeGenerate):

    _GENERATE_LOG_FILE = "cmake_gen_log.txt"
    _BUILD_LOG_FILE = "cmake_build_log.txt"

    def __init__(self):
        CmakeGenerate.__init__(self)
        self._abi = ['arm64-v8a', 'armeabi-v7a', 'x86']
        self._currentAbi = None
        self._android_out_dir = None
        self._project_out_dir = None
        self._config_file = None
        self._android_sys_version = None
        self._android_platform = None
        self._android_ndk = None
        self._cmake_path = None

    def serialize(self, node):
        self._config_file = node['android_config']
        self._separate_bins = node["separate_bins"]
        self._build_type = node['build_type']
        self._android_out_dir = node['android_out_dir']
        self._project_out_dir = node['project_out_dir']
        self._run_dir = node['run_dir']
        self._verbosity = self._getVerboisty(node)

    def _buildCmakeRunArgs(self):
        cmakeArgs = [
            'cmake ',
            '-S.',
            '-B{0}'.format(self._cmake_out_dir),
            '-GNinja',
            '-DANDROID_ABI={0}'.format(self._currentAbi),
            '-DANDROID_NDK={0}'.format(self._android_ndk),
            '-DCMAKE_ANDROID_NDK={0}'.format(self._android_ndk),
            '-DCMAKE_TOOLCHAIN_FILE={0}/build/cmake/android.toolchain.cmake'.format(self._android_ndk),
            '-DANDROID_TOOLCHAIN=clang',
            '-DANDROID_STL=c++_static',
            '-DCMAKE_ANDROID_ARCH_ABI={0}'.format(self._currentAbi),
            '-DANDROID_PLATFORM={0}'.format(self._android_platform),
            '-DCMAKE_BUILD_TYPE={0}'.format(self._build_type),
            '-DCMAKE_SYSTEM_NAME=Android',
            '-DCMAKE_SYSTEM_VERSION={0}'.format(self._android_sys_version),
            '-DCMAKE_MAKE_PROGRAM={0}/ninja.exe'.format(self._cmake_path),
        ]

        if not self._separate_bins:
            cmakeArgs.extend([
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG={0}/Debug'.format(self._bin_out_dir),
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE={0}/Release'.format(self._bin_out_dir),
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELWITHDEBINFO={0}/RelWithDebInfo'.format(self._bin_out_dir)
            ])
        else:
            cmakeArgs.extend(self._getDefsForBuildResultOutput())
    
        defs = self._getCmakeDefs()
        cmakeArgs.extend(defs)

        return cmakeArgs

    def _buildCompileRunArgs(self):
        runArgs = [
            '{0}/ninja.exe'.format(self._cmake_path)
        ]
        return runArgs

    def _createDefaultConfigFile(self):
        default_config = {
            "android_nkd_path":"",
            "android_cmake_path":"",
            "android_sys_version":""
        }
        parentDir = pathlib.Path(self._config_file).parent
        if not os.path.exists(parentDir):
            os.makedirs(parentDir)
        with open(self._config_file, 'w') as tFile:
            json.dump(default_config, tFile)

    def _getFromConfigRequired(self, keyName, config, requiredType, checkExists):
        if keyName not in config:
            Log.error("[Android:_loadConfigs] Can't find '{0}' in '{1}'".format(keyName, self._config_file))
            raise RuntimeError("Config incomplete")
        keyVal = config[keyName]
        if type(keyVal) != requiredType:
            Log.error("[Android:_loadConfigs] Key '{0}' in '{1}' should have type of '{2}' instead of {3}".format(
                keyName, self._config_file, requiredType, type(keyVal)))
            raise RuntimeError("Config incomplete")
        if checkExists:
            if not os.path.exists(keyVal):
                Log.error("[Android:_loadConfigs] Key '{0}' path doesn't exists: '{1}' from file: '{2}'".format(
                    keyName, keyVal, self._config_file))
                raise RuntimeError("Config incomplete")
        return keyVal

    def _loadConfigs(self):
        if not os.path.exists(self._config_file):
            Log.warning("[AndroidCmakeGenerate:_loadConfigs] Can't find android build config file: '{0}'".format(self._config_file))
            self._createDefaultConfigFile()
            raise RuntimeError("Can't start build without config file")
        try:
            with open(self._config_file, 'r') as tFile:
                androidBuildConfig = json.load(tFile)
        except:
            Log.error("[AndroidCmakeGenerate:_loadConfig] Can't load android build config file: '{0}'".format(self._config_file))
            raise

        self._android_ndk = self._getFromConfigRequired('android_ndk_path', androidBuildConfig, requiredType=str, checkExists=True)
        self._cmake_path = self._getFromConfigRequired('android_cmake_path', androidBuildConfig, requiredType=str, checkExists=True)
        self._android_sys_version = self._getFromConfigRequired('android_sys_version', androidBuildConfig, requiredType=int, checkExists=False)
        self._android_platform = 'android-{0}'.format(self._android_sys_version)

    def run(self):
        self._loadConfigs()
        res = True
        for abi in self._abi:
            self._currentAbi = abi
            self._out_dir = "{0}/{1}/{2}".format(
                self._android_out_dir,
                self._currentAbi,
                self._project_out_dir)
            res = CmakeGenerate.run(self)
            if res != True:
                Log.error("[AndroidCmakeGenerate:run] Build for ABI '{0}' failed".format(self._currentAbi))
                break
        return res