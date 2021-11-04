from PySide6 import QtCore, QtGui, QtWidgets
from models.line import Line
from models.point_2d import Point2D
from models.polygon import Polygon
from utils.font import get_custom_font


ITEMS_PER_FORM_ROW = 6


class NewObjectForm(QtWidgets.QWidget):
  onPointInserted = QtCore.Signal(Point2D)
  onLineInserted = QtCore.Signal(Line)
  onPolygonInserted = QtCore.Signal(Polygon)

  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.initFormContainer()
    self.initRowButtons()
    self.initForm()
    self.initInsertButton()
    
  def initFormContainer(self):
    self.formContainer = QtWidgets.QVBoxLayout()

    title = QtWidgets.QLabel('Insert New Object')
    title.setFont(get_custom_font('bold', 14))
    self.formContainer.addWidget(title)

    self.setLayout(self.formContainer)
    
  def initRowButtons(self):
    rowButtons = QtWidgets.QHBoxLayout()

    addPointButton = QtWidgets.QPushButton('Add Point')
    addPointButton.clicked.connect(self.insertFormRow)
    rowButtons.addWidget(addPointButton)

    resetButton = QtWidgets.QPushButton('Reset')
    resetButton.clicked.connect(self.resetForm)
    rowButtons.addWidget(resetButton)

    self.formContainer.addLayout(rowButtons)

  def initForm(self):
    self.formLayout = QtWidgets.QGridLayout()
    formLayoutWrapper = QtWidgets.QWidget()
    formLayoutWrapper.setLayout(self.formLayout)

    formScrollArea = QtWidgets.QScrollArea()
    formScrollArea.setWidget(formLayoutWrapper)
    formScrollArea.setFixedHeight(150)
    formScrollArea.setWidgetResizable(True)

    self.formContainer.addWidget(formScrollArea)
    self.insertFormRow()

  def initInsertButton(self):
    insertButton = QtWidgets.QPushButton('Insert')
    insertButton.clicked.connect(self.insertNewObject)
    self.formContainer.addWidget(insertButton)

  def insertFormRow(self):
    newRowNumber = int(self.formLayout.count() / ITEMS_PER_FORM_ROW + 1)

    rowName = QtWidgets.QLabel(f'P{newRowNumber}')
    rowName.setFont(get_custom_font('bold'))
    self.formLayout.addWidget(rowName, newRowNumber, 0)

    xLabel = QtWidgets.QLabel('X')
    xLabel.setAlignment(QtGui.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    self.formLayout.addWidget(xLabel, newRowNumber, 1)

    xInput = QtWidgets.QDoubleSpinBox()
    xInput.setMinimum(-10000)
    xInput.setMaximum(10000)
    self.formLayout.addWidget(xInput, newRowNumber, 2)

    yLabel = QtWidgets.QLabel('Y')
    yLabel.setAlignment(QtGui.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    self.formLayout.addWidget(yLabel, newRowNumber, 3)

    yInput = QtWidgets.QDoubleSpinBox()
    yInput.setMinimum(-10000)
    yInput.setMaximum(10000)
    self.formLayout.addWidget(yInput, newRowNumber, 4)

    deleteButton = QtWidgets.QPushButton('X')
    deleteButton.setFixedWidth(20)
    deleteButton.clicked.connect(lambda : self.deleteFormRow(newRowNumber))
    self.formLayout.addWidget(deleteButton, newRowNumber, 5)

  def deleteFormRow(self, rowToDelete):
    rangeStart = (rowToDelete - 1) * ITEMS_PER_FORM_ROW
    rangeEnd = (rowToDelete) * ITEMS_PER_FORM_ROW
    itemsToDelete = range(rangeStart, rangeEnd)

    for index in reversed(itemsToDelete):
      widgetToRemove = self.formLayout.itemAt(index).widget()
      self.formLayout.removeWidget(widgetToRemove)
      widgetToRemove.setParent(None)

    self.refreshFormRowsWithNewCount()

  def refreshFormRowsWithNewCount(self):
    for index in range(0, self.formLayout.count(), ITEMS_PER_FORM_ROW):
      newRowNumber = int(index / ITEMS_PER_FORM_ROW + 1)
      rowName = self.formLayout.itemAt(index).widget()
      rowName.setText(f'P{newRowNumber}')

    for index in range(5, self.formLayout.count(), ITEMS_PER_FORM_ROW):
      newRowNumber = int(index / ITEMS_PER_FORM_ROW + 1)
      deleteButton = self.formLayout.itemAt(index).widget()
      deleteButton.clicked.disconnect()
      deleteButton.clicked.connect(lambda : self.deleteFormRow(newRowNumber))

  def resetForm(self):
    for index in reversed(range(self.formLayout.count())):
      widgetToRemove = self.formLayout.itemAt(index).widget()
      self.formLayout.removeWidget(widgetToRemove)
      widgetToRemove.setParent(None)
    self.insertFormRow()

  @QtCore.Slot(str)
  def insertNewObject(self):
    xValues = []
    yValues = []

    for index in range(2, self.formLayout.count(), ITEMS_PER_FORM_ROW):
      xInput = self.formLayout.itemAt(index).widget()
      xValues.append(xInput.value())

    for index in range(4, self.formLayout.count(), ITEMS_PER_FORM_ROW):
      yInput = self.formLayout.itemAt(index).widget()
      yValues.append(yInput.value())

    pointsCount = len(xValues)
 
    if pointsCount == 0:
      return
    elif pointsCount == 1:
      self.onPointInserted.emit(Point2D(xValues[0], yValues[0]))
    elif pointsCount == 2:
      p1 = Point2D(xValues[0], yValues[0])
      p2 = Point2D(xValues[1], yValues[1])
      self.onLineInserted.emit(Line(p1, p2))
    else:
      points = []
      for index in range(pointsCount):
        points.append(Point2D(xValues[index], yValues[index]))
      self.onPolygonInserted.emit(Polygon(points))

    self.resetForm()
