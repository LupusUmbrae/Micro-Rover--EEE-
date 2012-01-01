import pickle
class Message:
    def __init__(self, functionName, params = []):
        self.functionName = functionName
        self.params = params

    def getFunctionName(self):
        return self.functionName

    def getParams(self):
        return self.params

    def serialize(self):
        return pickle.dumps(self)

    def unserialize(serializedObject):
        return pickle.loads(serializedObject)

    unserialize = staticmethod(unserialize)
