from enum import Enum
from models.classes.line import Line
from models.classes.point_2d import Point2D
from models.classes.point_3d import Point3D


# REGION CODES
RC_INSIDE = 0  # 0000
RC_LEFT = 1    # 0001
RC_RIGHT = 2   # 0010
RC_BOTTOM = 4  # 0100
RC_TOP = 8     # 1000


class ClippingResults(Enum):
  NONE = 0
  COMPLETELY_INSIDE = 1
  COMPLETELY_OUTSIDE = 2
  LINE_CLIPPED = 3


class CohenSutherlandClipper:
  def __init__(self, window):
    self.window = window

  def get_region_code(self, point):
    region_code = RC_INSIDE

    if (point.x_ncs < self.window.min_point.x_ncs):
      region_code |= RC_LEFT
    elif (point.x_ncs > self.window.max_point.x_ncs):
      region_code |= RC_RIGHT
    
    if (point.y_ncs < self.window.min_point.y_ncs):
      region_code |= RC_BOTTOM
    elif (point.y_ncs > self.window.max_point.y_ncs):
      region_code |= RC_TOP

    return region_code

  def clip_line(self, line):
    p1, p2 = Point2D(0, 0), Point2D(0, 0)
    p1.x_ncs, p1.y_ncs = line.point_1.x_ncs, line.point_1.y_ncs
    p2.x_ncs, p2.y_ncs = line.point_2.x_ncs, line.point_2.y_ncs
    
    region_code_p1 = self.get_region_code(p1)
    region_code_p2 = self.get_region_code(p2)

    result = ClippingResults.NONE
    
    while (True):
      is_both_points_inside_window = not(region_code_p1 | region_code_p2)

      if is_both_points_inside_window:
        if result == ClippingResults.NONE:
          result = ClippingResults.COMPLETELY_INSIDE
        break
      
      is_both_points_outside_window = region_code_p1 & region_code_p2

      if is_both_points_outside_window:
        if result == ClippingResults.NONE:
          result = ClippingResults.COMPLETELY_OUTSIDE
        break

      intersection_point_with_window = Point2D(0, 0)
      outside_region_code = region_code_p2 if region_code_p2 > region_code_p1 else region_code_p1
      
      if outside_region_code & RC_TOP:
        intersection_point_with_window.x = p1.x_ncs + (p2.x_ncs - p1.x_ncs) * (self.window.max_point.y_ncs - p1.y_ncs) / (p2.y_ncs - p1.y_ncs)
        intersection_point_with_window.y = self.window.max_point.y_ncs
      
      elif outside_region_code & RC_BOTTOM:
        intersection_point_with_window.x = p1.x_ncs + (p2.x_ncs - p1.x_ncs) * (self.window.min_point.y_ncs - p1.y_ncs) / (p2.y_ncs - p1.y_ncs)
        intersection_point_with_window.y = self.window.min_point.y_ncs
      
      elif outside_region_code & RC_RIGHT:
        intersection_point_with_window.y = p1.y_ncs + (p2.y_ncs - p1.y_ncs) * (self.window.max_point.x_ncs - p1.x_ncs) / (p2.x_ncs - p1.x_ncs)
        intersection_point_with_window.x = self.window.max_point.x_ncs
      
      elif outside_region_code & RC_LEFT:
        intersection_point_with_window.y = p1.y_ncs + (p2.y_ncs - p1.y_ncs) * (self.window.min_point.x_ncs - p1.x_ncs) / (p2.x_ncs - p1.x_ncs)
        intersection_point_with_window.x = self.window.min_point.x_ncs

      if outside_region_code == region_code_p1:
        p1.x_ncs = intersection_point_with_window.x
        p1.y_ncs = intersection_point_with_window.y
        region_code_p1 = self.get_region_code(p1)
      else:
        p2.x_ncs = intersection_point_with_window.x
        p2.y_ncs = intersection_point_with_window.y
        region_code_p2 = self.get_region_code(p2)

      result = ClippingResults.LINE_CLIPPED

    return {
      'line': self.generate_result_line(line, p1, p2),
      'result': result
    }

  def generate_result_line(self, line, p1, p2):
    line_point_1 = Point3D(line.point_1.x, line.point_1.y, line.point_1.z)
    line_point_1.x_ncs = p1.x_ncs
    line_point_1.y_ncs = p1.y_ncs
    line_point_1.z_ncs = line.point_1.z_ncs

    line_point_2 = Point3D(line.point_2.x, line.point_2.y, line.point_2.z)
    line_point_2.x_ncs = p2.x_ncs
    line_point_2.y_ncs = p2.y_ncs
    line_point_2.z_ncs = line.point_2.z_ncs

    return Line(line_point_1, line_point_2)
