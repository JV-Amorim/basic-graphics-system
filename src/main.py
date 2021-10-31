from dao.viewport import get_viewport_data, write_viewport_file
from dao.window import WindowDataReader
from gui.objects_renderer import render_objects


if __name__ == '__main__':
  window_data = WindowDataReader().get_window_data()
  viewport_data = get_viewport_data(window_data)
  write_viewport_file(viewport_data)
  render_objects(viewport_data, window_data['viewport'])
