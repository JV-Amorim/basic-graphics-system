class Point:
  def __init__(self, x, y, z):
    x_is_number = isinstance(x, int) or isinstance(x, float)
    y_is_number = isinstance(y, int) or isinstance(y, float)
    z_is_number = isinstance(z, int) or isinstance(z, float)

    if not x_is_number or not y_is_number or not z_is_number:
      raise ValueError('All point coordinates (x, y, z) must be a number.')
      
    self.__x, self.__y, self.__z = x, y, z

  def __repr__(self):
    return f'({self.__x}, {self.__y}, {self.__z})'

  def __eq__(self, other):
    if not isinstance(other, Point):
      return NotImplemented
    
    xEqual = self.__x == other.__x
    yEqual = self.__y == other.__y
    zEqual = self.__z == other.__z

    return xEqual and yEqual and zEqual
  
  def get_coordinates(self):
    return [self.__x, self.__y, self.__z]
