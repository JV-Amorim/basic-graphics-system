class Polygon:
  def __init__(self, points):
    if len(points) < 3:
      raise ValueError('A polygon needs at least 3 points.')
    self.__points = points

  def __repr__(self):
    return f'Points = {str(self.__points)}'

  def get_points(self):
    return self.__points
