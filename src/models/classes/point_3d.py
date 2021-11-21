import numpy

from utils.typecast import convert_dict_values_to_numeric


class Point3D:
  x_ncs = None
  y_ncs = None
  z_ncs = None

  def __init__(self, x, y, z):
    is_x_number = isinstance(x, int) or isinstance(x, float)
    is_y_number = isinstance(y, int) or isinstance(y, float)
    is_z_number = isinstance(z, int) or isinstance(z, float)

    if not is_x_number or not is_y_number or not is_z_number:
      raise ValueError('All point coordinates (x, y, z) must be a number.')
      
    self.x, self.y, self.z = x, y, z

  def __repr__(self):
    if self.x_ncs != None and self.y_ncs != None and self.z_ncs != None:
      return f'[NCS]({self.x_ncs}, {self.y_ncs}, {self.z_ncs})'
    return f'({self.x}, {self.y}, {self.z})'

  def __eq__(self, other):
    if not isinstance(other, Point3D):
      return NotImplemented
    
    is_x_equal = self.x == other.x
    is_y_equal = self.y == other.y
    is_z_equal = self.z == other.z

    return is_x_equal and is_y_equal and is_z_equal

  def set_ncs_values(self, translation_values, transformation_matrix):
    translated_x = self.x + translation_values[0]
    translated_y = self.y + translation_values[1]
    numpy_wcs_point = numpy.array([translated_x, translated_y, self.z])
    numpy_ncs_point = numpy_wcs_point.dot(transformation_matrix)
    self.x_ncs = numpy_ncs_point[0]
    self.y_ncs = numpy_ncs_point[1]
    self.z_ncs = numpy_ncs_point[2]

  def create_from_xml_attrib_dict(dict):
    dict = convert_dict_values_to_numeric(dict, 'float')
    return Point3D(dict['x'], dict['y'], dict['z'])
