import sys

from PySide6 import QtCore, QtGui, QtWidgets
from gui.object_insertion_dialog import ObjectInsertionDialog
from gui.object_management_dialog import ObjectManagementDialog
from gui.objects_renderer import OBJECTS_RENDERER_DIMENSIONS, ObjectsRenderer
from gui.window_transformations_group import WindowTransformationsGroup
from models.classes.line import Line
from models.classes.point_2d import Point2D
from models.classes.polygon import Polygon
from models.enums.window_transformations import WindowTransformations
from utils.font import get_custom_font
from utils.object import method_exists


WINDOW_TITLE = 'Basic Graphics System'
main_window = None


def start_gui(viewport_dict, window_dict, update_window_dict_callback, window_transformations_callback):
  global main_window

  if main_window != None:
    main_window.viewportDict = viewport_dict
    main_window.windowDict = window_dict
    main_window.refreshObjectsRenderer()
    return

  app = QtWidgets.QApplication()
  main_window = MainWindow(viewport_dict, window_dict)
  main_window.onObjectsUpdated.connect(lambda objects_data : update_window_dict_callback(objects_data[0], objects_data[1]))
  main_window.onTransformationApplied.connect(lambda type : window_transformations_callback(type))
  main_window.show()

  sys.exit(app.exec())


class MainWindow(QtWidgets.QWidget):
  # Emits a tuple (objects_data, is_to_export_data).
  onObjectsUpdated = QtCore.Signal(object)
  onTransformationApplied = QtCore.Signal(WindowTransformations)
  currentOpenedDialog = None

  def __init__(self, viewportDict, windowDict):
    super().__init__()
    self.viewportDict, self.windowDict = viewportDict, windowDict
    self.setWindowWidgetProperties()
    self.initUI()

  def setWindowWidgetProperties(self):
    width = OBJECTS_RENDERER_DIMENSIONS[0] + 300
    height = OBJECTS_RENDERER_DIMENSIONS[1] + 25
    self.setFixedSize(QtCore.QSize(width, height))
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
    exportButton.clicked.connect(lambda : self.onObjectsUpdated.emit((self.viewportDict, True)))
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

    self.enableClippingCheckbox = QtWidgets.QCheckBox('Enable Clipping')
    self.enableClippingCheckbox.click()
    self.enableClippingCheckbox.clicked.connect(self.refreshObjectsRenderer)
    generalOptionsLayout.addWidget(self.enableClippingCheckbox)

    generalOptionsGroup = QtWidgets.QGroupBox('General Options')
    generalOptionsGroup.setLayout(generalOptionsLayout)
    self.sidePanel.addWidget(generalOptionsGroup)

  def initObjectsRenderer(self):
    isDrawCoordinatesEnabled = self.drawCoordinatesCheckbox.isChecked()
    isClippingEnabled = self.enableClippingCheckbox.isChecked()
    self.objectsRenderer = ObjectsRenderer(self.viewportDict, self.windowDict, isDrawCoordinatesEnabled, isClippingEnabled)
    self.mainContainer.addWidget(self.objectsRenderer)

  def openObjectInsertionDialog(self):
    dialog = ObjectInsertionDialog()

    dialog.onPointInserted.connect(self.insertNewPoint)
    dialog.onLineInserted.connect(self.insertNewLine)
    dialog.onPolygonInserted.connect(self.insertNewPolygon)
    
    self.currentOpenedDialog = dialog
    dialog.exec()

  def openObjectManagementDialog(self):
    dialog = ObjectManagementDialog(self.viewportDict)

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
      self.currentOpenedDialog.refreshObjectsData(self.viewportDict)

  @QtCore.Slot(Point2D)
  def insertNewPoint(self, point):
    self.viewportDict['individual_points'].append(point)
    print('Point inserted.')
    self.onObjectsUpdated.emit((self.viewportDict, False))
    self.refreshCurrentDialog()
    
  @QtCore.Slot(Line)
  def insertNewLine(self, line):
    self.viewportDict['lines'].append(line)
    print('Line inserted.')
    self.onObjectsUpdated.emit((self.viewportDict, False))
    self.refreshCurrentDialog()

  @QtCore.Slot(Polygon)
  def insertNewPolygon(self, polygon):
    self.viewportDict['polygons'].append(polygon)
    print('Polygon inserted.')
    self.onObjectsUpdated.emit((self.viewportDict, False))
    self.refreshCurrentDialog()

  # Receives a tuple (int, int, bool).
  @QtCore.Slot(object)
  def deleteObject(self, objectIndexes):
    print('Object deleted.')

    if objectIndexes[0] == 0:
      point = self.viewportDict['individual_points'][objectIndexes[1]]
      self.viewportDict['individual_points'].remove(point)

    elif objectIndexes[0] == 1:
      line = self.viewportDict['lines'][objectIndexes[1]]
      self.viewportDict['lines'].remove(line)

    elif objectIndexes[0] == 2:
      polygon = self.viewportDict['polygons'][objectIndexes[1]]
      self.viewportDict['polygons'].remove(polygon)
    
    if len(objectIndexes) < 3 or objectIndexes[2] == True:
      self.onObjectsUpdated.emit((self.viewportDict, False))

    self.refreshCurrentDialog()
