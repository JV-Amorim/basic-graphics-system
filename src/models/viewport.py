class Viewport:
  def __init__(self, v_min_x, v_min_y, v_max_x, v_max_y):
    self.__v_min_x, self.__v_min_y = v_min_x, v_min_y
    self.__v_max_x, self.__v_max_y = v_max_x, v_max_y

  def __repr__(self):
    min_point = f'Min Point = ({self.__v_min_x}, {self.__v_min_y})'
    max_point = f'Max Point = ({self.__v_max_x}, {self.__v_max_y})'
    return f'{min_point} | {max_point}'

  def get_min_max_points(self):
    min_point = [self.__v_min_x, self.__v_min_y]
    max_point = [self.__v_max_x, self.__v_max_y]
    return [min_point, max_point]
