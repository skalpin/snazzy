from TestClass import TestClass

class ComposedClass():
    def __init__(self, testClass):
        self._testClass = testClass
