import sys

from PySide6 import QtCore, QtWidgets
from gui.new_object_form import NewObjectForm
from gui.objects_renderer import ObjectsRenderer
from models.point_2d import Point2D


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
    self.initMainContainer()
    self.initSidePanel()
    self.initObjectsRenderer()

  def initMainContainer(self):
    mainContainer = QtWidgets.QHBoxLayout(self)
    self.setLayout(mainContainer)
    self.mainContainer = mainContainer

  def initSidePanel(self):
    form = NewObjectForm()
    form.onPointInserted.connect(self.insertNewPoint)
    sidePanel = QtWidgets.QVBoxLayout()
    sidePanel.addWidget(form)
    self.mainContainer.addLayout(sidePanel)

  def initObjectsRenderer(self):
    self.objectsRenderer = ObjectsRenderer(self.objectsData, self.viewportData)
    self.mainContainer.addWidget(self.objectsRenderer)

  def setWindowProperties(self):
    width = self.viewportData.get_width()
    height = self.viewportData.get_height()
    self.setFixedSize(QtCore.QSize(width + 300, height + 25))
    self.setWindowTitle('Window To Viewport Mapper')

  @QtCore.Slot(Point2D)
  def insertNewPoint(self, point):
    self.objectsData['individual_points'].append(point)
    self.mainContainer.removeWidget(self.objectsRenderer)
    self.initObjectsRenderer()
