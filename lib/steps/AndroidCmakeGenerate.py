from .CmakeGenerate import CmakeGenerate
from lib.Logger import Log

class AndroidCmakeGenerate(CmakeGenerate):

    _GENERATE_LOG_FILE = "cmake_gen_log.txt"
    _BUILD_LOG_FILE = "cmake_build_log.txt"

    def __init__(self):
        CmakeGenerate.__init__(self)
        self._abi = ['armeabi-v7a', 'x86']
        self._build_type = 'Debug'
        self._currentAbi = None
        self._android_sys_version = 21 # Min API Level to support; Read it from manifest file
        self._android_platform = 'android-{0}'.format(self._android_sys_version)
        self._android_sdk = 'C:/Users/Alex-/AppData/Local/Android/Sdk'
        self._android_ndk = '{0}/ndk/21.3.6528147'.format(self._android_sdk)
        self._cmake_path = '{0}/cmake/3.10.2.4988404/bin'.format(self._android_sdk)

    def serialize(self, node):
        self._build_type = node['build_type']
        self._out_dir = node['out_dir']
        self._run_dir = node['run_dir']
        self._verbosity = self._getVerboisty(node)

    def _buildCmakeRunArgs(self):
        configStr = self._build_type.upper()
        cmakeArgs = [
            'cmake ',
            '-S.',
            '-B{0}'.format(self._cmake_out_dir),
            '-GNinja',
            '-DANDROID_ABI={0}'.format(self._currentAbi),
            '-DANDROID_NDK={0}'.format(self._android_ndk),
            '-DCMAKE_TOOLCHAIN_FILE={0}/build/cmake/android.toolchain.cmake'.format(self._android_ndk),
            '-DANDROID_TOOLCHAIN=clang',
            '-DANDROID_STL=c++_static',
            '-DANDROID_PLATFORM={0}'.format(self._android_platform),
            '-DCMAKE_BUILD_TYPE={0}'.format(self._build_type),
            '-DCMAKE_SYSTEM_NAME=Android',
            '-DCMAKE_SYSTEM_VERSION={0}'.format(self._android_sys_version),
            '-DCMAKE_MAKE_PROGRAM={0}/ninja.exe'.format(self._cmake_path),
            '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY={0}'.format(self._bin_out_dir),
            '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{0}={1}'.format(configStr, self._bin_out_dir),
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={0}'.format(self._bin_out_dir),
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{0}={1}'.format(configStr, self._bin_out_dir),
            '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY={0}'.format(self._bin_out_dir),
            '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{0}={1}'.format(configStr, self._bin_out_dir)
        ]
        defs = self._getCmakeDefs()
        cmakeArgs.extend(defs)
        return cmakeArgs

    def _buildCompileRunArgs(self):
        runArgs = [
            '{0}/ninja.exe'.format(self._cmake_path)
        ]
        return runArgs

    def run(self):
        res = True
        for abi in self._abi:
            self._currentAbi = abi
            res = CmakeGenerate.run(self)
            if res != True:
                Log.error("[AndroidCmakeGenerate:run] Build for ABI '{0}' failed".format(self._currentAbi))
                break
        return res