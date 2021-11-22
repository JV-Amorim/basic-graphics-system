from clippers.cohen_sutherland import CohenSutherlandClipper

def clip_all_objects_in_window_dict(window_dict):
  # TODO - Perform clipping to the points and polygons.
  
  line_clipper = CohenSutherlandClipper(window_dict['window'])
    
  quantity_of_lines = len(window_dict['lines'])
  for index in range(quantity_of_lines):
    line = window_dict['lines'][index]
    window_dict['lines'][index] = line_clipper.clip_line(line)

  return window_dict
