import sys

from clippers.cohen_sutherland import CohenSutherlandClipper
from clippers.main_clipper import clip_all_objects_in_window_dict
from gui.main_window import start_gui
from dao.viewport import get_viewport_data, write_viewport_file
from dao.window import WindowDataReader, get_window_dict_from_viewport_dict, write_new_window_file
from mappers.wcs_to_ncs import WcsToNcsMapper


window_dict = None


def is_to_use_new_input_file():
  arguments = sys.argv[1:]
  return len(arguments) > 0 and (arguments[0] == '-n' or arguments[0] == '--new-file')


def initialize_gui():
  global window_dict
  window_dict = WcsToNcsMapper(window_dict).get_mapped_data()
  window_dict = clip_all_objects_in_window_dict(window_dict)
  viewport_dict = get_viewport_data(window_dict)
  write_viewport_file(viewport_dict)
  start_gui(viewport_dict, window_dict, update_window_dict, apply_transformation_to_the_window)


def update_window_dict(viewport_dict, is_to_export_the_data):
  global window_dict

  viewport_dict['window'] = window_dict['window']
  viewport_dict['viewport'] = window_dict['viewport']
  window_dict = get_window_dict_from_viewport_dict(viewport_dict)

  if is_to_export_the_data:
    write_new_window_file(window_dict)

  initialize_gui()


def apply_transformation_to_the_window(transformation_type):
  global window_dict
  window_dict['window'].apply_transformation(transformation_type)
  initialize_gui()


# APP INITIALIZATION:

if __name__ == '__main__':
  use_new_input_file = is_to_use_new_input_file()
  window_dict = WindowDataReader(use_new_input_file).get_window_dict()
  initialize_gui()
