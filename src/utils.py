import os

def convert_dict_values_to_numeric(dict, int_or_float):
  if int_or_float != 'int' and int_or_float != 'float':
    raise ValueError('The parameter int_or_float must be "int" or "float".')

  if int_or_float == 'int':
    for key, value in dict.items():
      dict[key] = int(value)
  else:
    for key, value in dict.items():
      dict[key] = float(value)

  return dict

def create_directory_if_not_exists(directory):
  try:
    if not os.path.exists(directory):
      os.makedirs(directory)
  except OSError:
    raise OSError('It was not possible to create the directory.')

# The below function is from: https://stackoverflow.com/a/33956544/12331811.
def indent_xml(root, level = 0):
  i = '\n' + level * '  '
  if len(root):
    if not root.text or not root.text.strip():
      root.text = i + '  '
    if not root.tail or not root.tail.strip():
      root.tail = i
    for root in root:
      indent_xml(root, level + 1)
    if not root.tail or not root.tail.strip():
      root.tail = i
  else:
    if level and (not root.tail or not root.tail.strip()):
      root.tail = i
