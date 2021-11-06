import xml.etree.ElementTree as ET

from mappers.window_to_viewport import WindowToViewportMapper
from utils.io import create_directory_if_not_exists
from utils.xml import indent_xml


VIEWPORT_FILE_PATH = 'data/output/'
VIEWPORT_FILE_NAME = 'viewport-coordinates.xml'


def get_viewport_data(window_data):
  mapper = WindowToViewportMapper(window_data['window'], window_data['viewport'])

  viewport_data = {
    'individual_points': [],
    'lines': [],
    'polygons': []
  }

  for w_point in window_data['individual_points']:
    v_point = mapper.window_to_viewport_point(w_point)
    viewport_data['individual_points'].append(v_point)

  for w_line in window_data['lines']:
    v_line = mapper.window_to_viewport_line(w_line)
    viewport_data['lines'].append(v_line)

  for w_polygon in window_data['polygons']:
    v_polygon = mapper.window_to_viewport_polygon(w_polygon)
    viewport_data['polygons'].append(v_polygon)

  return viewport_data


def write_viewport_file(viewport_data):
  root = ET.Element('root')
  tree = ET.ElementTree(root)

  if len(viewport_data['individual_points']) > 0:
    individual_points_group = ET.SubElement(root, 'individual-points')
    for point in viewport_data['individual_points']:
      ET.SubElement(individual_points_group, 'point', x = str(point.x), y = str(point.y))

  if len(viewport_data['lines']) > 0:
    lines_group = ET.SubElement(root, 'lines')
    for line in viewport_data['lines']:
      line_elem = ET.SubElement(lines_group, 'line')
      ET.SubElement(line_elem, 'point', x = str(line.point_1.x), y = str(line.point_1.y))
      ET.SubElement(line_elem, 'point', x = str(line.point_2.x), y = str(line.point_2.y))

  if len(viewport_data['polygons']) > 0:
    polygons_group = ET.SubElement(root, 'polygons')
    for polygon in viewport_data['polygons']:
      polygon_elem = ET.SubElement(polygons_group, 'polygon')
      for point in polygon.get_points():
        ET.SubElement(polygon_elem, 'point', x = str(point.x), y = str(point.y))

  indent_xml(root)
  
  create_directory_if_not_exists(VIEWPORT_FILE_PATH)
  tree.write(VIEWPORT_FILE_PATH + VIEWPORT_FILE_NAME, encoding = "utf-8", xml_declaration = True)

  print('Output file generation completed.')
