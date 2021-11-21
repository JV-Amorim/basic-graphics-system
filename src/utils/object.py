from inspect import ismethod

def attribute_exists(object, attribute_name):
  return hasattr(object, attribute_name) and not(ismethod(getattr(object, attribute_name)))

def method_exists(object, method_name):
  return hasattr(object, method_name) and ismethod(getattr(object, method_name))
