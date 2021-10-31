import sys

from PySide6 import QtCore, QtWidgets
from gui.objects_renderer import ObjectsRenderer


def start_gui(objects_data, viewport_data):
  app = QtWidgets.QApplication()
  window = MainWindow(objects_data, viewport_data)
  window.show()
  sys.exit(app.exec())


class MainWindow(QtWidgets.QWidget):
  def __init__(self, objectsData, viewportData):
    super().__init__()
    self.objectsData = objectsData
    self.viewportData = viewportData
    self.initUI()
    self.setWindowProperties()

  def initUI(self):
    self.initMainPanel()
    self.initSidePanel()
    self.initObjectsPanel()

  def initMainPanel(self):
    mainPanel = QtWidgets.QHBoxLayout(self)
    self.layout = mainPanel

  def initSidePanel(self):
    label = QtWidgets.QLabel('Test Label')
    button = QtWidgets.QPushButton('Test Button')
    sidePanel = QtWidgets.QVBoxLayout()
    sidePanel.addWidget(label)
    sidePanel.addWidget(button)
    self.layout.addLayout(sidePanel)

  def initObjectsPanel(self):
    objectsPanel = ObjectsRenderer(self.objectsData, self.viewportData)
    self.layout.addWidget(objectsPanel)

  def setWindowProperties(self):
    width = self.viewportData.get_width()
    height = self.viewportData.get_height()
    self.setFixedSize(QtCore.QSize(width + 300, height + 25))
    self.setWindowTitle('Window To Viewport Mapper')
