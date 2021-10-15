import os
import xml.etree.ElementTree as ET
from utils import convert_dict_values_to_numeric
from models.line import Line
from models.point import Point
from models.polygon import Polygon
from models.viewport import Viewport
from models.window import Window

class XmlReader:
  def __init__(self):
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'input.xml')
    self.xml_root = ET.parse(path).getroot()

  def get_all_data(self):
    viewport = self.get_viewport_data()
    window = self.get_window_data()
    individual_points = self.get_individual_points_data()
    lines = self.get_lines_data()
    polygon = self.get_polygon_data()
    return {
      'viewport': viewport,
      'window': window,
      'individual_points': individual_points,
      'lines': lines,
      'polygon': polygon
    }

  def get_viewport_data(self):
    xml = self.xml_root
    vpmin = xml[0][0].attrib
    vpmax = xml[0][1].attrib
    vpmin = convert_dict_values_to_numeric(vpmin, 'float')
    vpmax = convert_dict_values_to_numeric(vpmax, 'float')
    return Viewport(vpmin['x'], vpmin['y'], vpmax['x'], vpmax['y'])

  def get_window_data(self):
    xml = self.xml_root
    w_min_point = Point.create_from_xml_attrib_dict(xml[1][0].attrib)
    w_max_point = Point.create_from_xml_attrib_dict(xml[1][1].attrib)
    return Window(w_min_point, w_max_point)

  def get_individual_points_data(self):
    xml = self.xml_root
    point_1 = Point.create_from_xml_attrib_dict(xml[2].attrib)
    point_2 = Point.create_from_xml_attrib_dict(xml[3].attrib)
    point_3 = Point.create_from_xml_attrib_dict(xml[4].attrib)
    return [point_1, point_2, point_3]

  def get_lines_data(self):
    xml = self.xml_root
    point_1_1 = Point.create_from_xml_attrib_dict(xml[5][0].attrib)
    point_1_2 = Point.create_from_xml_attrib_dict(xml[5][1].attrib)
    point_2_1 = Point.create_from_xml_attrib_dict(xml[6][0].attrib)
    point_2_2 = Point.create_from_xml_attrib_dict(xml[6][1].attrib)
    line_1 = Line(point_1_1, point_1_2)
    line_2 = Line(point_2_1, point_2_2)
    return [line_1, line_2]

  def get_polygon_data(self):
    xml = self.xml_root
    point_1 = Point.create_from_xml_attrib_dict(xml[7][0].attrib)
    point_2 = Point.create_from_xml_attrib_dict(xml[7][1].attrib)
    point_3 = Point.create_from_xml_attrib_dict(xml[7][2].attrib)
    point_4 = Point.create_from_xml_attrib_dict(xml[7][3].attrib)
    return Polygon([point_1, point_2, point_3, point_4])
