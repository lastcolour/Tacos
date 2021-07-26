from .Step import Step

import os

class SetEnvVar(Step):
    def __init__(self):
        Step.__init__(self)
        self._vars = {}

    def serialize(self, jsonNode):
        for key in jsonNode:
            self._vars[str(key)] = str(jsonNode[key])
    
    def run(self):
        for key, var in self._vars.items():
            os.environ[key] = var