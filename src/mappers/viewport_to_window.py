from models.classes.line import Line
from models.classes.point_3d import Point3D
from models.classes.polygon import Polygon


class ViewportToWindowMapper:
  def __init__(self, window, viewport):
    self.w_min,  self.w_max = window.min_point, window.max_point
    self.v_min,  self.v_max = viewport.min_point, viewport.max_point

  def window_to_viewport_x(self, x_value):
    return (x_value / (self.v_max.x - self.v_min.x) * (self.w_max.x - self.w_min.x)) + self.w_min.x

  def window_to_viewport_y(self, y_value):
    return ((((y_value / (self.v_max.y - self.v_min.y)) - 1) * (self.w_max.y - self.w_min.y)) - self.w_min.y) * (- 1)

  def viewport_to_window_point(self, viewport_point):
    window_x = self.window_to_viewport_x(viewport_point.x)
    window_y = self.window_to_viewport_y(viewport_point.y)
    return Point3D(window_x, window_y, 0)

  def viewport_to_window_line(self, viewport_line):
    p1 = self.viewport_to_window_point(viewport_line.point_1)
    p2 = self.viewport_to_window_point(viewport_line.point_2)
    return Line(p1, p2)

  def viewport_to_window_polygon(self, viewport_polygon):
    points = []
    for point in viewport_polygon.get_points():
      points.append(self.viewport_to_window_point(point))
    return Polygon(points)
