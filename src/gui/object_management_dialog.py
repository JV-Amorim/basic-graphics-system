from PySide6 import QtCore, QtWidgets
from gui.object_details_dialog import ObjectDetailsDialog
from gui.object_insertion_dialog import ObjectInsertionDialog
from models.classes.line import Line
from models.classes.point_2d import Point2D
from models.classes.polygon import Polygon
from utils.font import get_custom_font


DIALOG_TITLE = 'Update/Delete Objects'
ITEMS_PER_LIST_ROW = 5


class ObjectManagementDialog(QtWidgets.QDialog):
  # Emits a tuple (int, int).
  onObjectRemoved = QtCore.Signal(object)

  onPointInserted = QtCore.Signal(Point2D)
  onLineInserted = QtCore.Signal(Line)
  onPolygonInserted = QtCore.Signal(Polygon)

  currentOpenedDialog = None
  indexOfObjectBeingUpdated = None

  def __init__(self, objectsData):
    super().__init__()
    self.objectsData = objectsData
    self.setWindowProperties()
    self.initUI()

  def setWindowProperties(self):
    self.setWindowTitle(DIALOG_TITLE)
    self.setModal(True)
    self.setFixedSize(280, 360)

  def initUI(self):
    self.initMainContainer()
    self.initObjectList()

  def initMainContainer(self):
    self.mainContainer = QtWidgets.QVBoxLayout()

    title = QtWidgets.QLabel(DIALOG_TITLE)
    title.setFont(get_custom_font('bold', 14))
    self.mainContainer.addWidget(title)
    
    self.setLayout(self.mainContainer)

  def initObjectList(self):
    self.objectList = QtWidgets.QGridLayout()
    objectListWrapper = QtWidgets.QWidget()
    objectListWrapper.setLayout(self.objectList)

    objectListScrollArea = QtWidgets.QScrollArea()
    objectListScrollArea.setWidget(objectListWrapper)
    objectListScrollArea.setFixedHeight(300)
    objectListScrollArea.setWidgetResizable(True)

    for index in range(len(self.objectsData['individual_points'])):
      point = self.objectsData['individual_points'][index]
      self.insertItemInTheObjectList('individual_point', point, (0, index))
      
    for index in range(len(self.objectsData['lines'])):
      line = self.objectsData['lines'][index]
      self.insertItemInTheObjectList('line', line, (1, index))

    for index in range(len(self.objectsData['polygons'])):
      polygon = self.objectsData['polygons'][index]
      self.insertItemInTheObjectList('polygon', polygon, (2, index))

    self.mainContainer.addWidget(objectListScrollArea)

  def insertItemInTheObjectList(self, type, item, indexes):
    newRowNumber = int(self.objectList.count() / ITEMS_PER_LIST_ROW + 1)

    rowName = QtWidgets.QLabel(f'{newRowNumber}.')
    rowName.setFont(get_custom_font('bold'))
    rowName.setFixedWidth(25)
    self.objectList.addWidget(rowName, newRowNumber, 0)

    objectName = ''
    if type == 'individual_point':
      objectName = 'Point'
    elif type == 'line':
      objectName = 'Line'
    elif type == 'polygon':
      objectName = 'Polygon'

    objectType = QtWidgets.QLabel(objectName)
    self.objectList.addWidget(objectType, newRowNumber, 1)

    objectPoints = self.getObjectPoints(item, objectName)

    detailsButton = QtWidgets.QPushButton('🔍')
    detailsButton.setFixedWidth(25)
    detailsButton.clicked.connect(lambda : self.openObjectDetailsDialog(objectPoints, objectName))
    self.objectList.addWidget(detailsButton, newRowNumber, 2)

    updateButton = QtWidgets.QPushButton('🖊')
    updateButton.setFixedWidth(25)
    updateButton.clicked.connect(lambda : self.openObjectUpdateDialog(objectPoints, indexes[1]))
    self.objectList.addWidget(updateButton, newRowNumber, 3)

    deleteButton = QtWidgets.QPushButton('❌')
    deleteButton.setFixedWidth(25)
    deleteButton.clicked.connect(lambda : self.onObjectRemoved.emit(indexes))
    self.objectList.addWidget(deleteButton, newRowNumber, 4)

  def getObjectPoints(self, object, objectName):
    if objectName == 'Point':
      return [object]
    if objectName == 'Line':
      return [object.point_1, object.point_2]
    elif objectName == 'Polygon':
      return object.get_points()

  def openObjectDetailsDialog(self, objectPoints, objectName):
    dialog = ObjectDetailsDialog(objectPoints, objectName)
    dialog.exec()

  def openObjectUpdateDialog(self, objectPoints, objectIndex):
    self.indexOfObjectBeingUpdated = objectIndex

    dialog = ObjectInsertionDialog(objectPoints)
    dialog.onPointInserted.connect(self.updatePoint)
    dialog.onLineInserted.connect(self.updateLine)
    dialog.onPolygonInserted.connect(self.updatePolygon)

    self.currentOpenedDialog = dialog
    dialog.exec()

  def refreshObjectsData(self, objectsData):
    objectList = self.mainContainer.takeAt(1).widget()
    objectList.setParent(None)
    self.objectsData = objectsData
    self.initObjectList()

  @QtCore.Slot(Point2D)
  def updatePoint(self, point):
    self.currentOpenedDialog.close()
    self.onObjectRemoved.emit((0, self.indexOfObjectBeingUpdated, False))
    self.onPointInserted.emit(point)
    
  @QtCore.Slot(Line)
  def updateLine(self, line):
    self.currentOpenedDialog.close()
    self.onObjectRemoved.emit((1, self.indexOfObjectBeingUpdated, False))
    self.onLineInserted.emit(line)

  @QtCore.Slot(Polygon)
  def updatePolygon(self, polygon):
    self.currentOpenedDialog.close()
    self.onObjectRemoved.emit((2, self.indexOfObjectBeingUpdated, False))
    self.onPolygonInserted.emit(polygon)
