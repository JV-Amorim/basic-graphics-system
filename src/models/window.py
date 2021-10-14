class Window:
  def __init__(self, w_min_point, w_max_point):
    self.__w_min_point, self.__w_max_point = w_min_point, w_max_point

  def __repr__(self):
    return f'Min Point = {self.__w_min_point} | Max Point = {self.__w_max_point}'

  def get_min_max_points(self):
    return [self.__w_min_point, self.__w_max_point]
