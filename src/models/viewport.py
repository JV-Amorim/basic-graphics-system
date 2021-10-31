class Viewport:
  def __init__(self, min_point_2d, max_point_2d):
    self.min_point, self.max_point = min_point_2d, max_point_2d

  def __repr__(self):
    return f'Min Point = {self.min_point} | Max Point = {self.max_point}'

  def get_width(self):
    return self.min_point.x + self.max_point.x

  def get_height(self):
    return self.min_point.y + self.max_point.y
