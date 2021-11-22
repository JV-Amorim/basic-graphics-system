import numpy

from utils.typecast import convert_dict_values_to_numeric


class Point2D:
  x_ncs = None
  y_ncs = None

  x_clipped = None
  y_clipped = None

  def __init__(self, x, y):
    is_x_number = isinstance(x, int) or isinstance(x, float)
    is_y_number = isinstance(y, int) or isinstance(y, float)

    if not is_x_number or not is_y_number:
      raise ValueError('All point coordinates (x, y) must be a number.')
      
    self.x, self.y = x, y

  def __repr__(self):
    if self.x_ncs != None and self.y_ncs != None:
      return f'[NCS]({self.x_ncs}, {self.y_ncs})'
    return f'({self.x}, {self.y})'

  def __eq__(self, other):
    if not isinstance(other, Point2D):
      return NotImplemented
    
    is_x_equal = self.x == other.x
    is_y_equal = self.y == other.y

    return is_x_equal and is_y_equal

  def set_ncs_values(self, translation_values, transformation_matrix):
    translated_x = self.x + translation_values[0]
    translated_y = self.y + translation_values[1]
    numpy_wcs_point = numpy.array([[translated_x], [translated_y], [0]])
    numpy_ncs_point = transformation_matrix.dot(numpy_wcs_point)
    self.x_ncs = numpy_ncs_point[0][0]
    self.y_ncs = numpy_ncs_point[1][0]

  def create_from_xml_attrib_dict(dict):
    dict = convert_dict_values_to_numeric(dict, 'int')
    return Point2D(dict['x'], dict['y'])
