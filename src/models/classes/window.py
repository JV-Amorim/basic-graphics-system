import copy

from models.enums.window_transformations import WindowTransformations


class Window:
  current_rotation = 0

  def __init__(self, min_point_3d, max_point_3d):
    self.min_point = min_point_3d
    self.max_point = max_point_3d
    self.original_min_point = copy.deepcopy(min_point_3d)
    self.original_max_point = copy.deepcopy(max_point_3d)

  def __repr__(self):
    return f'Min Point = {self.min_point} | Max Point = {self.max_point}'

  def apply_transformation(self, transformation_type):
    if transformation_type == WindowTransformations.RESET:
      self.reset_transformations()
    elif transformation_type == WindowTransformations.ZOOM_IN:
      self.apply_zoom(10)
    elif transformation_type == WindowTransformations.ZOOM_OUT:
      self.apply_zoom(-10)
    elif transformation_type == WindowTransformations.MOVE_UP:
      self.apply_y_translation(1)
    elif transformation_type == WindowTransformations.MOVE_DOWN:
      self.apply_y_translation(-1)
    elif transformation_type == WindowTransformations.MOVE_RIGHT:
      self.apply_x_translation(1)
    elif transformation_type == WindowTransformations.MOVE_LEFT:
      self.apply_x_translation(-1)
    elif transformation_type == WindowTransformations.ROTATE_LEFT:
      self.apply_rotation(10)
    elif transformation_type == WindowTransformations.ROTATE_RIGHT:
      self.apply_rotation(-10)

  def reset_transformations(self):
    self.min_point = copy.deepcopy(self.original_min_point)
    self.max_point = copy.deepcopy(self.original_max_point)
    self.current_rotation = 0

  def apply_zoom(self, zoom_percentage):
    self.max_point.x -= self.max_point.x * zoom_percentage / 100
    self.max_point.y -= self.max_point.y * zoom_percentage / 100

  def apply_x_translation(self, translation_value):
    self.min_point.x -= translation_value
    self.max_point.x -= translation_value

  def apply_y_translation(self, translation_value):
    self.min_point.y -= translation_value
    self.max_point.y -= translation_value

  def apply_rotation(self, rotation_in_degrees):
    self.current_rotation -= rotation_in_degrees
