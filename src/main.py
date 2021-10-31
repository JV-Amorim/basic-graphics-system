from gui.main_window import start_gui
from dao.viewport import get_viewport_data, write_viewport_file
from dao.window import WindowDataReader


if __name__ == '__main__':
  window_data = WindowDataReader().get_window_data()
  viewport_data = get_viewport_data(window_data)
  write_viewport_file(viewport_data)
  start_gui(viewport_data, window_data['viewport'])
