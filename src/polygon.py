class Polygon:
  def __init__(self, points):
    # TODO - Check if polygon is valid (if the first and last points meet).
    if len(points) < 3:
      raise ValueError('A polygon needs at least 3 points.')
    self.__points = points

  def __repr__(self):
    return 'Points = ' + str(self.__points)

  def insert_point(self, point):
    self.__points.append(point)

  def remove_point(self, index):
    if len(self.__points) - 1 < 3:
      print('Cannot remove the point. A polygon needs at least 3 points.')
      return
    self.__points[index:index+1] = []

  def get_points(self):
    return self.__points
