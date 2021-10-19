class Window:
  def __init__(self, min_point, max_point):
    self.min_point, self.max_point = min_point, max_point

  def __repr__(self):
    return f'Min Point = {self.min_point} | Max Point = {self.max_point}'
