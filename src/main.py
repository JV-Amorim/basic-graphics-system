import sys

from gui.main_window import start_gui
from dao.viewport import get_viewport_data, write_viewport_file
from dao.window import WindowDataReader, get_window_data_from_viewport_data, write_new_window_file


window_data = None


def export_updated_objects_data(viewport_objects_data):
  viewport_objects_data['window'] = window_data['window']
  viewport_objects_data['viewport'] = window_data['viewport']
  write_new_window_file(get_window_data_from_viewport_data(viewport_objects_data))

def is_to_use_new_input_file():
  arguments = sys.argv[1:]
  return len(arguments) > 0 and (arguments[0] == '-n' or arguments[0] == '--new-file')

if __name__ == '__main__':
  use_new_input_file = is_to_use_new_input_file()
  window_data = WindowDataReader(use_new_input_file).get_window_data()
  viewport_data = get_viewport_data(window_data)
  write_viewport_file(viewport_data)
  start_gui(viewport_data, window_data['viewport'], export_updated_objects_data)
