from utils import convert_dict_values_to_numeric

class Point:
  def __init__(self, x, y, z):
    is_x_number = isinstance(x, int) or isinstance(x, float)
    is_y_number = isinstance(y, int) or isinstance(y, float)
    is_z_number = isinstance(z, int) or isinstance(z, float)

    if not is_x_number or not is_y_number or not is_z_number:
      raise ValueError('All point coordinates (x, y, z) must be a number.')
      
    self.x, self.y, self.z = x, y, z

  def __repr__(self):
    return f'({self.x}, {self.y}, {self.z})'

  def __eq__(self, other):
    if not isinstance(other, Point):
      return NotImplemented
    
    is_x_equal = self.x == other.x
    is_y_equal = self.y == other.y
    is_z_equal = self.z == other.z

    return is_x_equal and is_y_equal and is_z_equal

  def create_from_xml_attrib_dict(dict):
    dict = convert_dict_values_to_numeric(dict, 'float')
    return Point(dict['x'], dict['y'], dict['z'])
