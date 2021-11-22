class Line:
  clipped_point_1 = None
  clipped_point_2 = None
  completely_clipped = False

  def __init__(self, point_1, point_2):
    if point_1 == point_2:
      raise ValueError('The points must be distinct.')
    self.point_1 = point_1
    self.point_2 = point_2

  def __repr__(self):
    return f'P1 = {self.point_1} | P2 = {self.point_2}'
