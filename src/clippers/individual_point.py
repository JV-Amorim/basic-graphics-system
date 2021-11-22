def is_the_point_outside_the_window(window, point):
  is_x_coord_outside = window.min_point.x >= point.x or window.max_point.x <= point.x
  is_y_coord_outside = window.min_point.y >= point.y or window.max_point.y <= point.y
  return is_x_coord_outside or is_y_coord_outside
