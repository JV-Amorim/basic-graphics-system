import xml.etree.ElementTree as ET
from utils import create_directory_if_not_exists, indent_xml

OUTPUT_DIRECTORY = 'data/output/'
OUTPUT_FILE = 'viewport-coordinates.xml'

def write_output_file(output_data):
  root = ET.Element('root')
  tree = ET.ElementTree(root)

  if len(output_data['individual_points']) > 0:
    individual_points_group = ET.SubElement(root, 'individual-points')
    for point in output_data['individual_points']:
      ET.SubElement(individual_points_group, 'point', x = str(point.x), y = str(point.y))

  if len(output_data['lines']) > 0:
    lines_group = ET.SubElement(root, 'lines')
    for line in output_data['lines']:
      line_elem = ET.SubElement(lines_group, 'line')
      ET.SubElement(line_elem, 'point', x = str(line.point_1.x), y = str(line.point_1.y))
      ET.SubElement(line_elem, 'point', x = str(line.point_2.x), y = str(line.point_2.y))

  if len(output_data['polygons']) > 0:
    polygons_group = ET.SubElement(root, 'polygons')
    for polygon in output_data['polygons']:
      polygon_elem = ET.SubElement(polygons_group, 'polygon')
      for point in polygon.get_points():
        ET.SubElement(polygon_elem, 'point', x = str(point.x), y = str(point.y))

  indent_xml(root)
  
  create_directory_if_not_exists(OUTPUT_DIRECTORY)
  tree.write(OUTPUT_DIRECTORY + OUTPUT_FILE, encoding = "utf-8", xml_declaration = True)

  print('SUCCESS: Output file generation completed.')
