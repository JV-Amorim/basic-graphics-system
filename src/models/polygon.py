class Polygon:
  def __init__(self, points):
    if len(points) < 3:
      raise ValueError('A polygon needs at least 3 points.')

    if points[0] != points[-1]:
      raise ValueError('The polygon is invalid. The first and last point must be equal.')
      
    self.__points = points

  def __repr__(self):
    return 'Points = ' + str(self.__points)

  def get_points(self):
    return self.__points
