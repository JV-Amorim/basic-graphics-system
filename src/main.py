import sys

from gui.main_window import start_gui
from dao.viewport import get_viewport_data, write_viewport_file
from dao.window import WindowDataReader, get_window_data_from_viewport_data, write_new_window_file
from mappers.wcs_to_ncs import WcsToNcsMapper


window_data = None


def initialize_gui():
  global window_data
  window_data = WcsToNcsMapper(window_data).get_mapped_data()
  viewport_data = get_viewport_data(window_data)
  write_viewport_file(viewport_data)
  start_gui(viewport_data, window_data['viewport'], update_objects_data, apply_transformation_to_window)

def is_to_use_new_input_file():
  arguments = sys.argv[1:]
  return len(arguments) > 0 and (arguments[0] == '-n' or arguments[0] == '--new-file')

def update_objects_data(viewport_objects_data, is_to_export_data):
  global window_data

  viewport_objects_data['window'] = window_data['window']
  viewport_objects_data['viewport'] = window_data['viewport']
  window_data = get_window_data_from_viewport_data(viewport_objects_data)

  if is_to_export_data:
    write_new_window_file(window_data)

  initialize_gui()

def apply_transformation_to_window(transformation_type):
  global window_data
  window_data['window'].apply_transformation(transformation_type)
  initialize_gui()


if __name__ == '__main__':
  use_new_input_file = is_to_use_new_input_file()
  window_data = WindowDataReader(use_new_input_file).get_window_data()
  initialize_gui()
