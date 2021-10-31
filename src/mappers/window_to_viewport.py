from models.line import Line
from models.point_2d import Point2D
from models.polygon import Polygon


class WindowToViewportMapper:
  def __init__(self, window, viewport):
    self.__window, self.__viewport = window, viewport

  def window_to_viewport_point(self, window_point):
    w_min, w_max = self.__window.min_point, self.__window.max_point
    v_min, v_max = self.__viewport.min_point, self.__viewport.max_point

    viewport_x = (window_point.x - w_min.x) / (w_max.x - w_min.x) * (v_max.x - v_min.x)

    viewport_y = (1 - ((window_point.y - w_min.y) / (w_max.y - w_min.y))) * (v_max.y - v_min.y)

    return Point2D(viewport_x, viewport_y)

  def window_to_viewport_line(self, window_line):
    p1 = self.window_to_viewport_point(window_line.point_1)
    p2 = self.window_to_viewport_point(window_line.point_2)
    return Line(p1, p2)

  def window_to_viewport_polygon(self, window_polygon):
    points = []
    for point in window_polygon.get_points():
      points.append(self.window_to_viewport_point(point))
    return Polygon(points)
