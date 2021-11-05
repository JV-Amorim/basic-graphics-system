import sys

from PySide6 import QtCore, QtGui, QtWidgets
from gui.object_insertion_dialog import ObjectInsertionDialog
from gui.object_management_dialog import ObjectManagementDialog
from gui.objects_renderer import ObjectsRenderer
from models.line import Line
from models.point_2d import Point2D
from models.polygon import Polygon


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
    self.mainContainer = QtWidgets.QHBoxLayout(self)
    self.setLayout(self.mainContainer)

  def initSidePanel(self):
    sidePanel = QtWidgets.QVBoxLayout()
    sidePanel.setAlignment(QtGui.Qt.AlignTop)

    insertButton = QtWidgets.QPushButton('Insert Object')
    insertButton.clicked.connect(self.openObjectInsertionDialog)
    sidePanel.addWidget(insertButton)

    editOrRemoveButton = QtWidgets.QPushButton('Edit/Remove Object')
    editOrRemoveButton.clicked.connect(self.openObjectManagementDialog)
    sidePanel.addWidget(editOrRemoveButton)

    self.mainContainer.addLayout(sidePanel)

  def initObjectsRenderer(self):
    self.objectsRenderer = ObjectsRenderer(self.objectsData, self.viewportData)
    self.mainContainer.addWidget(self.objectsRenderer)

  def setWindowProperties(self):
    width = self.viewportData.get_width()
    height = self.viewportData.get_height()
    self.setFixedSize(QtCore.QSize(width + 300, height + 25))
    self.setWindowTitle('Window To Viewport Mapper')

  def openObjectInsertionDialog(self):
    dialog = ObjectInsertionDialog()
    dialog.onPointInserted.connect(self.insertNewPoint)
    dialog.onLineInserted.connect(self.insertNewLine)
    dialog.onPolygonInserted.connect(self.insertNewPolygon)
    dialog.exec()

  def openObjectManagementDialog(self):
    dialog = ObjectManagementDialog()
    dialog.exec()

  def refreshObjectsRenderer(self):
    self.mainContainer.removeWidget(self.objectsRenderer)
    self.initObjectsRenderer()

  @QtCore.Slot(Point2D)
  def insertNewPoint(self, point):
    self.objectsData['individual_points'].append(point)
    print('SUCCESS: New point inserted.')
    self.refreshObjectsRenderer()
    
  @QtCore.Slot(Line)
  def insertNewLine(self, line):
    self.objectsData['lines'].append(line)
    print('SUCCESS: New line inserted.')
    self.refreshObjectsRenderer()

  @QtCore.Slot(Polygon)
  def insertNewPolygon(self, polygon):
    self.objectsData['polygons'].append(polygon)
    print('SUCCESS: New polygon inserted.')
    self.refreshObjectsRenderer()
