from .Step import Step

class IfVariableEqual(Step):
    def __init__(self):
        Step.__init__(self)
        self._varA = None
        self._varB = None

    def serialize(self, jsonData):
        self._varA = jsonData["varA"]
        self._varB = jsonData["varB"]
    
    def run(self):
        return self._varA == self._varB

class IfVariableInSet(Step):
    def __init__(self):
        Step.__init__(self)
        self._var = None
        self._set = set()

    def serialize(self, jsonData):
        self._var = jsonData["var"]
        for item in jsonData["set"]:
            self._set.add(item)
    
    def run(self):
        return self._var in self._set