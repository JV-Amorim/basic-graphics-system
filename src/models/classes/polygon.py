from models.classes.line import Line

class Polygon:
  def __init__(self, points):
    if len(points) < 3:
      raise ValueError('A polygon needs at least 3 points.')
    self.__points = points

    self.lines = []
    for index in range(1, len(points)):
      self.lines.append(Line(points[index - 1], points[index]))
    self.lines.append(Line(points[-1], points[0]))

  def __repr__(self):
    return f'Points = {str(self.__points)}'

  def get_points(self):
    return self.__points
