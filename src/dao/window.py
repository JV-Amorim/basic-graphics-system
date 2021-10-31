import os
import xml.etree.ElementTree as ET

from models.line import Line
from models.point_2d import Point2D
from models.point_3d import Point3D
from models.polygon import Polygon
from models.viewport import Viewport
from models.window import Window


POINT_TAG = 'ponto'
LINE_TAG = 'reta'
POLYGON_TAG = 'poligono'


class WindowDataReader:
  def __init__(self):
    path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'input', 'input.xml')
    self.xml_root = ET.parse(path).getroot()

  def get_window_data(self):
    viewport = self.create_viewport_object()
    window = self.create_window_object()

    individual_points, lines, polygons = [], [], []

    for index in range(2, len(self.xml_root)):
      current_element = self.xml_root[index]

      if current_element.tag == POINT_TAG:
        point = self.create_individual_point_object(current_element)
        individual_points.append(point)

      if current_element.tag == LINE_TAG:
        line = self.create_line_object(current_element)
        lines.append(line)
      
      if current_element.tag == POLYGON_TAG:
        polygon = self.create_polygon_object(current_element)
        polygons.append(polygon)

    return {
      'viewport': viewport,
      'window': window,
      'individual_points': individual_points,
      'lines': lines,
      'polygons': polygons
    }

  def create_viewport_object(self):
    xml = self.xml_root
    v_min_point = Point2D.create_from_xml_attrib_dict(xml[0][0].attrib)
    v_max_point = Point2D.create_from_xml_attrib_dict(xml[0][1].attrib)
    return Viewport(v_min_point, v_max_point)

  def create_window_object(self):
    xml = self.xml_root
    w_min_point = Point3D.create_from_xml_attrib_dict(xml[1][0].attrib)
    w_max_point = Point3D.create_from_xml_attrib_dict(xml[1][1].attrib)
    return Window(w_min_point, w_max_point)

  def create_individual_point_object(self, individual_point_element):
    attrib = individual_point_element.attrib
    return Point3D.create_from_xml_attrib_dict(attrib)

  def create_line_object(self, line_element):
    point_1 = Point3D.create_from_xml_attrib_dict(line_element[0].attrib)
    point_2 = Point3D.create_from_xml_attrib_dict(line_element[1].attrib)
    return Line(point_1, point_2)

  def create_polygon_object(self, polygon_element):
    points = []
    for point_element in polygon_element:
      point = Point3D.create_from_xml_attrib_dict(point_element.attrib)
      points.append(point)
    return Polygon(points)
