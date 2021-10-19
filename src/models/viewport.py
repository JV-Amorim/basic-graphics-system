class Viewport:
  def __init__(self, min_x, min_y, max_x, max_y):
    self.min_x, self.min_y = min_x, min_y
    self.max_x, self.max_y = max_x, max_y

  def __repr__(self):
    min_point = f'Min Point = ({self.min_x}, {self.min_y})'
    max_point = f'Max Point = ({self.max_x}, {self.max_y})'
    return f'{min_point} | {max_point}'
