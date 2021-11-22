from models.classes.line import Line
from models.classes.point_2d import Point2D
from models.classes.polygon import Polygon


class WindowToViewportMapper:
  def __init__(self, window, viewport):
    self.w_min, self.w_max = window.min_point, window.max_point
    self.v_min, self.v_max = viewport.min_point, viewport.max_point

  def window_to_viewport_x(self, x_value):
    return (x_value - self.w_min.x_ncs) / (self.w_max.x_ncs - self.w_min.x_ncs) * (self.v_max.x - self.v_min.x)
  
  def window_to_viewport_y(self, y_value):
    return  (1 - ((y_value - self.w_min.y_ncs) / (self.w_max.y_ncs - self.w_min.y_ncs))) * (self.v_max.y - self.v_min.y)

  def window_to_viewport_point(self, window_point):
    viewport_point = Point2D(0, 0)
    viewport_point.x_ncs = window_point.x_ncs
    viewport_point.y_ncs = window_point.y_ncs

    viewport_point.x = self.window_to_viewport_x(window_point.x_ncs)
    viewport_point.y = self.window_to_viewport_y(window_point.y_ncs)

    if window_point.x_clipped != None:
      viewport_point.x_clipped = self.window_to_viewport_x(window_point.x_clipped)
    if window_point.y_clipped != None:
      viewport_point.y_clipped =  self.window_to_viewport_y(window_point.y_clipped)

    return viewport_point

  def window_to_viewport_line(self, window_line):
    p1 = self.window_to_viewport_point(window_line.point_1)
    p2 = self.window_to_viewport_point(window_line.point_2)
    return Line(p1, p2)

  def window_to_viewport_polygon(self, window_polygon):
    points = []
    for point in window_polygon.get_points():
      points.append(self.window_to_viewport_point(point))
    return Polygon(points)
