class Window:
  def __init__(self, min_point_3d, max_point_3d, initial_rotation = 0):
    self.min_point = min_point_3d
    self.max_point = max_point_3d
    self.current_rotation = initial_rotation

  def __repr__(self):
    return f'Min Point = {self.min_point} | Max Point = {self.max_point}'

  def apply_rotation(self, rotation_in_degrees):
    self.current_rotation += rotation_in_degrees
