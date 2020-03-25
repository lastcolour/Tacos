from .Logger import Log

from collections import OrderedDict

class FmtState:
    NoState = 0
    StartDollar = 1
    StartBracket = 2
    EndBracket = 3

def _canStartState(currState, startState):
    if startState == FmtState.StartDollar:
        if currState == FmtState.NoState:
            return True
        else:
            return False
    elif startState == FmtState.StartBracket:
        if currState == FmtState.StartDollar:
            return True
        else:
            return False
    elif startState == FmtState.EndBracket:
        if currState == FmtState.StartBracket:
            return True
        else:
            return False
    else:
        return False

def _raiseFomatError(fmtStr, pos, errStr):
    errMsg = "Error! Cannot format: "
    Log.error("{0}{1}".format(errMsg, fmtStr))
    Log.error("{0}^ -- {1}".format(
        " " * (len(errMsg) + pos),
        errStr
    ))
    raise RuntimeError("Invalid format variable")

def _getFmtTokens(s):
    res = []
    startIdx = 0
    endIdx = startIdx
    currState = FmtState.NoState
    for i in range(0, len(s)):
        ch = s[i]
        if ch == '$':
            if _canStartState(currState, FmtState.StartDollar):
                startIdx = i
                endIdx = startIdx
                currState = FmtState.StartDollar
            else:
                _raiseFomatError(s, i, "'$' inside of foramt expression")
        elif ch == '{':
            if _canStartState(currState, FmtState.StartBracket):
                currState = FmtState.StartBracket
            else:
                _raiseFomatError(s, i, "missing starting '$' before '{ ... '")
        elif ch == '}':
            if _canStartState(currState, FmtState.EndBracket):
                endIdx = i
                currState = FmtState.NoState
                res.append((startIdx, endIdx))
            else:
                _raiseFomatError(s, i, "missing starting '${ ... ' before closing '}'")

    if currState is not FmtState.NoState:
        if currState is FmtState.StartDollar:
            _raiseFomatError(s, startIdx, "missing '{ ... ' afrer '$'")
        elif currState is FmtState.StartBracket:
            _raiseFomatError(s, startIdx, "missing closing '}' after staring '${ ... '")
        elif currState is FmtState.EndBracket:
            raise RuntimeError("Invalid format state")

    tokens = []
    prevEnd = 0
    for item in res:
        if item[0] > prevEnd:
            reguralToken = (s[prevEnd:item[0]], False)
            tokens.append(reguralToken)
        fmtToken = (s[item[0]+2:item[1]], True)
        tokens.append(fmtToken)
        prevEnd = item[1] + 1
    if prevEnd < len(s):
        reguralToken = (s[prevEnd:len(s)], False)
        tokens.append(reguralToken)
    return tokens

class Context:
    def __init__(self):
        self._vars = {}

    def addVariable(self, varName, varValue):
        if varValue is None:
            raise RuntimeError("Can't create varialbe with none value <'{0}':None>".format(varName))
        if type(varValue) is not str:
            raise RuntimeError("Can't add variable: <'{0}' : '{1}'> of non 'str' type: {2}".format(varName, varValue, type(varName).__str__()))
        if varName in self._vars:
            Log.info("Override variable: <'{0}': '{1}' -> '{2}'>".format(varName, self._vars[varName], varValue))
            del self._vars[varName]
        varValue = self.getFormated(varValue, isSoft=False)
        if varValue is None:
            raise RuntimeError("Can't add variable {0} with format variable: {1}".format(varName, varValue))
        self._vars[varName] = varValue

    def getVariable(self, varName):
        if varName not in self._vars:
            Log.warn("Can't find variable: '{0}'".format(varName))
            return None
        return self._vars[varName]

    def getFormated(self, varStr, isSoft=False):
        res = []
        tokens = _getFmtTokens(varStr)
        for token in tokens:
            fmtFlag = token[1]
            if fmtFlag:
                fmtVarName = token[0]
                if fmtVarName not in self._vars:
                    if not isSoft:
                        raise RuntimeError("Can't find variable '{0}' to format string: '{1}'".format(fmtVarName, varStr))
                    else:
                        res.append("${{{0}}}".format(fmtVarName))
                else:
                    res.append(self._vars[fmtVarName])
            else:
                res.append(token[0])
        return "".join(res)

    def _recursiveFormat(self, val, isSoft):
        if type(val) is list:
            for i in range(0, len(val)):
                val[i] = self._recursiveFormat(val[i], isSoft)
            return val
        elif type(val) in [dict, OrderedDict]:
            for item in val.keys():
                val[item] = self._recursiveFormat(val[item], isSoft)
            return val
        elif type(val) is str:
            return self.getFormated(val, isSoft)
        else:
            return val

    def createStepNode(self, jsonNode):
        self._recursiveFormat(jsonNode, isSoft=False)
        return jsonNode

    def createStepNodeSoft(self, jsonNode):
        self._recursiveFormat(jsonNode, isSoft=True)
        return jsonNode

    def setParentContext(self, parentContext):
        for varName in parentContext._vars.keys():
            if varName not in self._vars:
                self._vars[varName] = parentContext._vars[varName]