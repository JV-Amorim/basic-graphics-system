import sys

from PySide6 import QtCore, QtGui, QtWidgets
from gui.object_insertion_dialog import ObjectInsertionDialog
from gui.object_management_dialog import ObjectManagementDialog
from gui.objects_renderer import ObjectsRenderer
from models.line import Line
from models.point_2d import Point2D
from models.polygon import Polygon
from utils.font import get_custom_font
from utils.object import method_exists


WINDOW_TITLE = 'Basic Graphics System'


def start_gui(objects_data, viewport_data, export_callback):
  app = QtWidgets.QApplication()
  window = MainWindow(objects_data, viewport_data)
  window.onExportPointClicked.connect(lambda updated_objects_data : export_callback(updated_objects_data))
  window.show()
  sys.exit(app.exec())


class MainWindow(QtWidgets.QWidget):
  currentOpenedDialog = None
  onExportPointClicked = QtCore.Signal(object)

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

  def initObjectsRenderer(self):
    self.objectsRenderer = ObjectsRenderer(self.objectsData, self.viewportData)
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
