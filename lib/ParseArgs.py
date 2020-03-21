import sys

from .Logger import Log

def _removeQuoted(argStr):
    if len(argStr) < 2:
        return argStr
    if argStr[0] != '"':
        return argStr
    if argStr[-1] != '"':
        raise RuntimeError("Invalid string formation: can't find closing qoute")
    return argStr[1:-1]

def _getCmdArgValue(cmdStr):
    if len(cmdStr) is 0:
        return None
    return _removeQuoted(cmdStr)

def _extractrojectNameFromOneItem(argList, startIdx):
    item = argList[startIdx]
    if not item.startswith('--project'):
        return None
    projectName = item[len('--project'):]
    if len(projectName) is 0:
        return None
    if projectName[0] not in [':', '=']:
        return None
    resName = _removeQuoted(projectName[1:])
    if len(resName) == 0:
        return None
    return resName

def _extractProjectNameFromTwoItems(argList, startIdx):
    if len(argList) < startIdx + 2:
        return None
    firstItem = argList[startIdx]
    if firstItem != '--project':
        return None
    secondItem = argList[startIdx + 1]
    projectName = _getCmdArgValue(secondItem)
    if not projectName:
        return None
    return projectName

def _extractProjectName(argList, startIdx):
    projectName = _extractrojectNameFromOneItem(argList, startIdx)
    if projectName:
        return projectName, startIdx + 1
    projectName = _extractProjectNameFromTwoItems(argList, startIdx)
    if projectName:
        return projectName, startIdx + 2
    return None, startIdx

def _extractInputVars(argList, startIdx):
    return {}, startIdx

def _extractHelp(argList, startIdx):
    return False

def _printVersionInfo():
    print("Tacos -- 0.1 (Beta)")

def _printCantParseArgs():
    print("Error:\n")
    print("  Can't parse arguments: {0}\n".format(" ".join(sys.argv[1:])))

def _printGeneralHelp():
    print("Usage:\n")
    print("  - Required argument: ")
    print("    --project = ... \t\t\t -- path to a project file to run")
    print("\n  - Optional arguments: ")
    print("    [--inputVarName=inputVarValue, ]\t -- supported input variables for specified project")

def _printProjectHelp(projectName):
    pass

def ParseArgs():
    _printVersionInfo()
    argList = sys.argv[1:]
    if len(argList) is 0:
        _printGeneralHelp()
        sys.exit(1)
        return None, None
    startIdx = 1
    if _extractHelp(argList, startIdx):
        _printGeneralHelp()
        return None, None
    projectName, startIdx = _extractProjectName(sys.argv, startIdx)
    if projectName is None:
        _printCantParseArgs()
        _printGeneralHelp()
        sys.exit(1)
        return None, None
    if _extractHelp(argList, startIdx):
        _printProjectHelp(projectName)
        sys.exit(1)
        return None, None
    inputVars, startIdx = _extractInputVars(sys.argv, startIdx)
    return projectName, inputVars