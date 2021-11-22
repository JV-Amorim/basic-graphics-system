from clippers.cohen_sutherland import CohenSutherlandClipper
from clippers.individual_point import is_the_point_outside_the_window

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

  # TODO - Perform clipping to the polygons.

  return window_dict
