from models.line import Line
from models.point_2d import Point2D
from models.polygon import Polygon


class ViewportToWindowMapper:
  def __init__(self, window, viewport):
    self.__window, self.__viewport = window, viewport

  def viewport_to_window_point(self, viewport_point):
    w_min, w_max = self.__window.min_point, self.__window.max_point
    v_min, v_max = self.__viewport.min_point, self.__viewport.max_point

    window_x = (viewport_point.x / (v_max.x - v_min.x) * (w_max.x - w_min.x)) + w_min.x
    
    window_y = ((((viewport_point.y / (v_max.y - v_min.y)) - 1) * (w_max.y - w_min.y)) - w_min.y) * (- 1)

    return Point2D(window_x, window_y)

  def viewport_to_window_line(self, viewport_line):
    p1 = self.viewport_to_window_point(viewport_line.point_1)
    p2 = self.viewport_to_window_point(viewport_line.point_2)
    return Line(p1, p2)

  def viewport_to_window_polygon(self, viewport_polygon):
    points = []
    for point in viewport_polygon.get_points():
      points.append(self.viewport_to_window_point(point))
    return Polygon(points)
