import os
import pathlib
import shutil

def CreateAndGetTMPDir():
    tmpDir = "{0}/tmp".format(pathlib.Path(__file__).parent)
    if not os.path.exists(tmpDir):
        os.mkdir(tmpDir)
    return tmpDir

def RemoteTMPDir():
    tmpDir = "{0}/tmp".format(pathlib.Path(__file__).parent)
    if os.path.exists(tmpDir):
        shutil.rmtree(tmpDir)