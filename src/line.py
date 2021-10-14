class Line:
  def __init__(self, point_1, point_2):
    if point_1 == point_2:
      raise ValueError('The points must be distinct.')
    self.__point_1 = point_1
    self.__point_2 = point_2

  def __repr__(self):
    return f'P1 = {self.__point_1} | P2 = {self.__point_2}'

  def get_points(self):
    return [self.__point_1, self.__point_2]
