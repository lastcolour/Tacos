from .Step import Step

class CreateVariables(Step):
    def __init__(self):
        Step.__init__(self)
        self._varsToCreate = []

    def serialize(self, jsonNode):
        for item in jsonNode.keys():
            self._varsToCreate.append((item, jsonNode[item]))
        return True

    def run(self):
        ctx = self._getContext()
        for varPair in self._varsToCreate:
            ctx.addVariable(varPair[0], varPair[1])
        return True

class SwtichCaseCreateVariable(Step):
    def __init__(self):
        Step.__init__(self)
        self._variable = None
        self._cases = {}

    def serialize(self, jsonNode):
        self._variable = jsonNode["variable"]
        self._cases = jsonNode["cases"]
        return True
    
    def run(self):
        ctx = self._getContext()
        if self._variable not in self._cases:
            return True
        varToCreate = self._cases[self._variable]
        for varName in varToCreate:
            ctx.addVariable(varName, varToCreate[varName])
        return True