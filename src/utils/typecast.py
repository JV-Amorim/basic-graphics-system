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
