from clippers.cohen_sutherland import CohenSutherlandClipper
from clippers.individual_point import is_the_point_outside_the_window
from models.classes.polygon import Polygon

def clip_all_objects_in_window_dict(window_dict):
  quantity_of_points = len(window_dict['individual_points'])

  for index in range(quantity_of_points):
    point = window_dict['individual_points'][index]
    is_clipped = is_the_point_outside_the_window(window_dict['window'], point)
    window_dict['individual_points'][index].completely_clipped = is_clipped

  line_clipper = CohenSutherlandClipper(window_dict['window'])
  quantity_of_lines = len(window_dict['lines'])

  for index in range(quantity_of_lines):
    line = window_dict['lines'][index]
    window_dict['lines'][index] = line_clipper.clip_line(line)

  quantity_of_polygons = len(window_dict['polygons'])

  for index_p in range(quantity_of_polygons):
    polygon = window_dict['polygons'][index_p]
    quantity_of_polygon_lines = len(polygon.lines)

    for index_l in range(quantity_of_polygon_lines):
      line = polygon.lines[index_l]
      polygon.lines[index_l] = line_clipper.clip_line(line)

  return window_dict
