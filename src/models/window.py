class Window:
  def __init__(self, min_point_3d, max_point_3d):
    self.min_point, self.max_point = min_point_3d, max_point_3d

  def __repr__(self):
    return f'Min Point = {self.min_point} | Max Point = {self.max_point}'
