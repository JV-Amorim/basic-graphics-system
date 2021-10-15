from utils import convert_dict_values_to_numeric

class Point:
  def __init__(self, x, y, z):
    is_x_number = isinstance(x, int) or isinstance(x, float)
    is_y_number = isinstance(y, int) or isinstance(y, float)
    is_z_number = isinstance(z, int) or isinstance(z, float)

    if not is_x_number or not is_y_number or not is_z_number:
      raise ValueError('All point coordinates (x, y, z) must be a number.')
      
    self.__x, self.__y, self.__z = x, y, z

  def __repr__(self):
    return f'({self.__x}, {self.__y}, {self.__z})'

  def __eq__(self, other):
    if not isinstance(other, Point):
      return NotImplemented
    
    is_x_equal = self.__x == other.__x
    is_y_equal = self.__y == other.__y
    is_z_equal = self.__z == other.__z

    return is_x_equal and is_y_equal and is_z_equal
  
  def get_coordinates(self):
    return [self.__x, self.__y, self.__z]

  def create_from_xml_attrib_dict(dict):
    dict = convert_dict_values_to_numeric(dict, 'float')
    return Point(dict['x'], dict['y'], dict['z'])
