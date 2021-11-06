from inspect import ismethod

def method_exists(object, methodName):
  return hasattr(object, methodName) and ismethod(getattr(object, methodName))
