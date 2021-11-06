from PySide6 import QtCore, QtWidgets
from gui.object_details_dialog import ObjectDetailsDialog
from utils.font import get_custom_font


DIALOG_TITLE = 'Edit/Remove Objects'
ITEMS_PER_LIST_ROW = 5


class ObjectManagementDialog(QtWidgets.QDialog):
  # Emits a tuple.
  onObjectRemoved = QtCore.Signal(object)

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

    detailsButton = QtWidgets.QPushButton('🔍')
    detailsButton.setFixedWidth(25)
    detailsButton.clicked.connect(lambda : self.openObjectDetailsDialog(item, objectName))
    self.objectList.addWidget(detailsButton, newRowNumber, 2)

    editButton = QtWidgets.QPushButton('🖊')
    editButton.setFixedWidth(25)
    self.objectList.addWidget(editButton, newRowNumber, 3)

    deleteButton = QtWidgets.QPushButton('❌')
    deleteButton.setFixedWidth(25)
    deleteButton.clicked.connect(lambda : self.onObjectRemoved.emit(indexes))
    self.objectList.addWidget(deleteButton, newRowNumber, 4)

  def openObjectDetailsDialog(self, object, objectName):
    dialog = None
    if objectName == 'Point':
      dialog = ObjectDetailsDialog([object], objectName)
    elif objectName == 'Line':
      dialog = ObjectDetailsDialog([object.point_1, object.point_2], objectName)
    elif objectName == 'Polygon':
      dialog = ObjectDetailsDialog(object.get_points(), objectName)
    dialog.exec()

  def refreshObjectList(self, objectsData):
    objectList = self.mainContainer.takeAt(1).widget()
    objectList.setParent(None)
    self.objectsData = objectsData
    self.initObjectList()
