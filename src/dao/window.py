import os
import xml.etree.ElementTree as ET

from mappers.viewport_to_window import ViewportToWindowMapper
from models.line import Line
from models.point_2d import Point2D
from models.point_3d import Point3D
from models.polygon import Polygon
from models.viewport import Viewport
from models.window import Window
from utils.io import create_directory_if_not_exists
from utils.xml import indent_xml


ROOT_TAG = 'dados'
POINT_TAG = 'ponto'
LINE_TAG = 'reta'
POLYGON_TAG = 'poligono'

ORIGINAL_INPUT_FILE_PATH = 'data/input/'
ORIGINAL_INPUT_FILE_NAME = 'input.xml'

NEW_INPUT_FILE_PATH = 'data/output/'
NEW_INPUT_FILE_NAME = 'new-input.xml'


class WindowDataReader:
  def __init__(self, use_new_input_file = False):
    self.use_new_input_file = use_new_input_file
    self.set_xml_root()

  def set_xml_root(self):
    partial_path = ''
    if self.use_new_input_file:
      partial_path = f'{NEW_INPUT_FILE_PATH}{NEW_INPUT_FILE_NAME}'
    else:
      partial_path = f'{ORIGINAL_INPUT_FILE_PATH}{ORIGINAL_INPUT_FILE_NAME}'
    full_path = os.path.join(os.path.dirname(__file__), '..', '..', partial_path)
    self.xml_root = ET.parse(full_path).getroot()

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


def get_window_data_from_viewport_data(viewport_data):
  mapper = ViewportToWindowMapper(viewport_data['window'], viewport_data['viewport'])

  window_data = {
    'window': viewport_data['window'],
    'viewport': viewport_data['viewport'],
    'individual_points': [],
    'lines': [],
    'polygons': []
  }

  for v_point in viewport_data['individual_points']:
    w_point = mapper.viewport_to_window_point(v_point)
    window_data['individual_points'].append(w_point)

  for v_line in viewport_data['lines']:
    w_line = mapper.viewport_to_window_line(v_line)
    window_data['lines'].append(w_line)

  for v_polygon in viewport_data['polygons']:
    w_polygon = mapper.viewport_to_window_polygon(v_polygon)
    window_data['polygons'].append(w_polygon)

  return window_data


def write_new_window_file(window_data):
  root = ET.Element(ROOT_TAG)
  tree = ET.ElementTree(root)

  v_min_point = window_data['viewport'].min_point
  v_max_point = window_data['viewport'].max_point
  w_min_point = window_data['window'].min_point
  w_max_point = window_data['window'].max_point

  viewport_elem = ET.SubElement(root, 'window')
  ET.SubElement(viewport_elem, 'vpmin', x = str(v_min_point.x), y = str(v_min_point.y))
  ET.SubElement(viewport_elem, 'vpmax', x = str(v_max_point.x), y = str(v_max_point.y))

  window_elem = ET.SubElement(root, 'window')
  ET.SubElement(window_elem, 'wmin', x = str(w_min_point.x), y = str(w_min_point.y), z = '0.0')
  ET.SubElement(window_elem, 'wmax', x = str(w_max_point.x), y = str(w_max_point.y), z = '0.0')

  for point in window_data['individual_points']:
    ET.SubElement(root, POINT_TAG, x = str(point.x), y = str(point.y), z = '0.0')

  for line in window_data['lines']:
    line_elem = ET.SubElement(root, LINE_TAG)
    ET.SubElement(line_elem, POINT_TAG, x = str(line.point_1.x), y = str(line.point_1.y), z = '0.0')
    ET.SubElement(line_elem, POINT_TAG, x = str(line.point_2.x), y = str(line.point_2.y), z = '0.0')
  
  for polygon in window_data['polygons']:
    polygon_elem = ET.SubElement(root, POLYGON_TAG)
    for point in polygon.get_points():
      ET.SubElement(polygon_elem, POINT_TAG, x = str(point.x), y = str(point.y), z = '0.0')

  indent_xml(root)
  
  create_directory_if_not_exists(NEW_INPUT_FILE_PATH)
  tree.write(NEW_INPUT_FILE_PATH + NEW_INPUT_FILE_NAME, encoding = "utf-8", xml_declaration = True)

  print('New input file generation completed.')
