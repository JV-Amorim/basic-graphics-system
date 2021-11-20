# Mapper: Window Coordinates System (WCS) to Normalized Coordinates System (NCS).
# Mapeador: Sistema de Coordenadas da Window (SCW) para Sistema de Coordenadas Normalizado (SCN).

import math
import numpy

from models.point_2d import Point2D


class WcsToNcsMapper:
  def __init__(self, window_data):
    self.window_data = window_data

  def get_mapped_data(self):
    translation_matrix = self.generate_translation_matrix()
    rotation_matrix = self.generate_rotation_matrix()
    scale_matrix = self.generate_scale_matrix()

    numpy_translation_array = numpy.array(translation_matrix)
    numpy_rotation_array = numpy.array(rotation_matrix)
    numpy_scale_array = numpy.array(scale_matrix)
    
    transformation_matrix = numpy_scale_array.dot(numpy_rotation_array).dot(numpy_translation_array)
  
    self.window_data['window'].min_point.set_ncs_values(transformation_matrix)
    self.window_data['window'].max_point.set_ncs_values(transformation_matrix)

    for individual_point in self.window_data['individual_points']:
      individual_point.set_ncs_values(transformation_matrix)
    
    for line in self.window_data['lines']:
      line.point_1.set_ncs_values(transformation_matrix)
      line.point_2.set_ncs_values(transformation_matrix)

    for polygon in self.window_data['polygons']:
      for point in polygon.get_points():
        point.set_ncs_values(transformation_matrix)

    return self.window_data
  
  def generate_translation_matrix(self):
    window = self.window_data['window']

    window_center_x = (window.min_point.x + window.max_point.x) / 2
    window_center_y = (window.min_point.y + window.max_point.y) / 2
    window_center_point = Point2D(window_center_x, window_center_y)

    return [
      [1, 0, -window_center_point.x],
      [0, 1, -window_center_point.y],
      [0, 0, 1]
    ]
  
  def generate_rotation_matrix(self):
    window = self.window_data['window']

    inverted_window_rotation = math.radians(-window.current_rotation)
    rotation_cos = math.cos(inverted_window_rotation)
    rotation_sin = math.sin(inverted_window_rotation)

    return [
      [rotation_cos, -rotation_sin, 0],
      [rotation_sin, rotation_cos, 0],
      [0, 0, 1],
    ]
  
  def generate_scale_matrix(self):
    window = self.window_data['window']

    half_window_width = (window.max_point.x - window.min_point.x) / 2
    half_window_height = (window.max_point.y - window.min_point.y) / 2

    return [
      [1 / half_window_width, 0, 0],
      [0, 1 / half_window_height, 0],
      [0, 0, 1],
    ]

  def generate_point_with_ncs_values(self, wcs_point, transformation_matrix):
    numpy_wcs_point = numpy.array([wcs_point.x, wcs_point.y, 0])
    numpy_ncs_point = numpy_wcs_point.dot(transformation_matrix)
    
    new_point = Point2D(wcs_point.x, wcs_point.y)
    new_point.x_ncs = numpy_ncs_point[0]
    new_point.y_ncs = numpy_ncs_point[1]

    return new_point
