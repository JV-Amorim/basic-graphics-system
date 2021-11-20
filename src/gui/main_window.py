import sys

from PySide6 import QtCore, QtGui, QtWidgets
from gui.object_insertion_dialog import ObjectInsertionDialog
from gui.object_management_dialog import ObjectManagementDialog
from gui.objects_renderer import ObjectsRenderer
from gui.window_transformations_group import WindowTransformationsGroup
from models.classes.line import Line
from models.classes.point_2d import Point2D
from models.classes.polygon import Polygon
from models.enums.window_transformations import WindowTransformations
from utils.font import get_custom_font
from utils.object import method_exists


WINDOW_TITLE = 'Basic Graphics System'
main_window = None


def start_gui(objects_data, viewport_data, export_callback, transformation_callback):
  global main_window

  if main_window != None:
    main_window.objectsData = objects_data
    main_window.refreshObjectsRenderer()
    return

  app = QtWidgets.QApplication()
  main_window = MainWindow(objects_data, viewport_data)
  main_window.onExportPointClicked.connect(lambda updated_objects_data : export_callback(updated_objects_data))
  main_window.onTransformationApplied.connect(lambda transformation_type : transformation_callback(transformation_type))
  main_window.show()

  sys.exit(app.exec())


class MainWindow(QtWidgets.QWidget):
  currentOpenedDialog = None
  onExportPointClicked = QtCore.Signal(object)
  onTransformationApplied = QtCore.Signal(WindowTransformations)

  def __init__(self, objectsData, viewportData):
    super().__init__()
    self.objectsData = objectsData
    self.viewportData = viewportData
    self.setWindowProperties()
    self.initUI()

  def setWindowProperties(self):
    width = self.viewportData.get_width()
    height = self.viewportData.get_height()
    self.setFixedSize(QtCore.QSize(width + 300, height + 25))
    self.setWindowTitle(WINDOW_TITLE)

  def initUI(self):
    self.initMainContainer()
    self.initSidePanel()
    self.initObjectsRenderer()

  def initMainContainer(self):
    self.mainContainer = QtWidgets.QHBoxLayout(self)
    self.setLayout(self.mainContainer)

  def initSidePanel(self):
    self.sidePanel = QtWidgets.QVBoxLayout()
    self.sidePanel.setAlignment(QtGui.Qt.AlignTop)

    title = QtWidgets.QLabel(WINDOW_TITLE)
    title.setFont(get_custom_font('bold', 14))
    title.setAlignment(QtGui.Qt.AlignCenter)
    self.sidePanel.addWidget(title)

    self.initObjectManagementGroup()
    self.initWindowTransformationsGroup()
    self.initGeneralOptionsGroup()

    self.mainContainer.addLayout(self.sidePanel)

  def initObjectManagementGroup(self):
    objectManagementLayout = QtWidgets.QVBoxLayout()

    insertButton = QtWidgets.QPushButton('Insert ➕')
    insertButton.clicked.connect(self.openObjectInsertionDialog)
    objectManagementLayout.addWidget(insertButton)

    managementButton = QtWidgets.QPushButton('Update/Delete 🖊')
    managementButton.clicked.connect(self.openObjectManagementDialog)
    objectManagementLayout.addWidget(managementButton)

    exportButton = QtWidgets.QPushButton('Export Data 💾')
    exportButton.clicked.connect(lambda : self.onExportPointClicked.emit(self.objectsData))
    objectManagementLayout.addWidget(exportButton)

    objectManagementGroup = QtWidgets.QGroupBox('Object Management')
    objectManagementGroup.setLayout(objectManagementLayout)
    self.sidePanel.addWidget(objectManagementGroup)

  def initWindowTransformationsGroup(self):
    windowTransformationsGroup = WindowTransformationsGroup()
    windowTransformationsGroup.onButtonClicked.connect(lambda t : self.onTransformationApplied.emit(t))
    self.sidePanel.addWidget(windowTransformationsGroup)

  def initGeneralOptionsGroup(self):
    generalOptionsLayout = QtWidgets.QVBoxLayout()

    self.drawCoordinatesCheckbox = QtWidgets.QCheckBox('Draw Coordinates')
    self.drawCoordinatesCheckbox.click()
    self.drawCoordinatesCheckbox.clicked.connect(self.refreshObjectsRenderer)
    generalOptionsLayout.addWidget(self.drawCoordinatesCheckbox)

    generalOptionsGroup = QtWidgets.QGroupBox('General Options')
    generalOptionsGroup.setLayout(generalOptionsLayout)
    self.sidePanel.addWidget(generalOptionsGroup)

  def initObjectsRenderer(self):
    isToDrawCoordinates = self.drawCoordinatesCheckbox.isChecked()
    self.objectsRenderer = ObjectsRenderer(self.objectsData, self.viewportData, isToDrawCoordinates)
    self.mainContainer.addWidget(self.objectsRenderer)

  def openObjectInsertionDialog(self):
    dialog = ObjectInsertionDialog()

    dialog.onPointInserted.connect(self.insertNewPoint)
    dialog.onLineInserted.connect(self.insertNewLine)
    dialog.onPolygonInserted.connect(self.insertNewPolygon)
    
    self.currentOpenedDialog = dialog
    dialog.exec()

  def openObjectManagementDialog(self):
    dialog = ObjectManagementDialog(self.objectsData)

    dialog.onObjectRemoved.connect(self.deleteObject)
    dialog.onPointInserted.connect(self.insertNewPoint)
    dialog.onLineInserted.connect(self.insertNewLine)
    dialog.onPolygonInserted.connect(self.insertNewPolygon)

    self.currentOpenedDialog = dialog
    dialog.exec()

  def refreshObjectsRenderer(self):
    self.mainContainer.removeWidget(self.objectsRenderer)
    self.initObjectsRenderer()

  def refreshCurrentDialog(self):
    if method_exists(self.currentOpenedDialog, 'refreshObjectsData'):
      self.currentOpenedDialog.refreshObjectsData(self.objectsData)

  @QtCore.Slot(Point2D)
  def insertNewPoint(self, point):
    self.objectsData['individual_points'].append(point)
    print('Point inserted.')
    self.refreshObjectsRenderer()
    self.refreshCurrentDialog()
    
  @QtCore.Slot(Line)
  def insertNewLine(self, line):
    self.objectsData['lines'].append(line)
    print('Line inserted.')
    self.refreshObjectsRenderer()
    self.refreshCurrentDialog()

  @QtCore.Slot(Polygon)
  def insertNewPolygon(self, polygon):
    self.objectsData['polygons'].append(polygon)
    print('Polygon inserted.')
    self.refreshObjectsRenderer()
    self.refreshCurrentDialog()

  # Receives a tuple (int, int, bool).
  @QtCore.Slot(object)
  def deleteObject(self, objectIndexes):
    print('Object deleted.')

    if objectIndexes[0] == 0:
      point = self.objectsData['individual_points'][objectIndexes[1]]
      self.objectsData['individual_points'].remove(point)

    elif objectIndexes[0] == 1:
      line = self.objectsData['lines'][objectIndexes[1]]
      self.objectsData['lines'].remove(line)

    elif objectIndexes[0] == 2:
      polygon = self.objectsData['polygons'][objectIndexes[1]]
      self.objectsData['polygons'].remove(polygon)
    
    if len(objectIndexes) < 3 or objectIndexes[3] == True:
      self.refreshObjectsRenderer()

    self.refreshCurrentDialog()
