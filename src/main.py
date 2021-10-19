from mapper import Mapper
from xml_input_reader import XmlInputReader

input_data = XmlInputReader().get_all_input_data()

mapper = Mapper(input_data['window'], input_data['viewport'])

output_data = {
  'individual_points': [],
  'lines': [],
  'polygons': []
}

for w_point in input_data['individual_points']:
  v_point = mapper.window_to_viewport_point(w_point)
  output_data['individual_points'].append(v_point)

for w_line in input_data['lines']:
  v_line = mapper.window_to_viewport_line(w_line)
  output_data['lines'].append(v_line)

for w_polygon in input_data['polygons']:
  v_polygon = mapper.window_to_viewport_polygon(w_polygon)
  output_data['polygons'].append(v_polygon)

print(output_data)

# TODO - Generate output file.
# TODO - Show objects in GUI with QT.
