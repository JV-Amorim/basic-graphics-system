from PySide6 import QtCore, QtWidgets
from models.point_2d import Point2D
from utils.font import get_custom_font


class NewObjectForm(QtWidgets.QWidget):
  onPointInserted = QtCore.Signal(Point2D)

  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.initFormContainer()
    self.initTypeSelector()
    self.initPointForm()
    self.typeSelector.itemAt(1).widget().click()
    
  def initFormContainer(self):
    formContainer = QtWidgets.QVBoxLayout()
    formContainer.setAlignment(QtCore.Qt.AlignTop)

    title = QtWidgets.QLabel('Insert New Object')
    title.setFont(get_custom_font('bold', 14))
    formContainer.addWidget(title)

    self.setLayout(formContainer)
    self.formContainer = formContainer

  def initTypeSelector(self):
    typeSelector = QtWidgets.QHBoxLayout()
    typeSelector.addWidget(QtWidgets.QLabel('Type:'))

    pointRadio = QtWidgets.QRadioButton('Point')
    pointRadio.clicked.connect(lambda: self.changeSelectedType('point'))
    typeSelector.addWidget(pointRadio)

    lineRadio = QtWidgets.QRadioButton('Line')
    lineRadio.clicked.connect(lambda: self.changeSelectedType('line'))
    typeSelector.addWidget(lineRadio)

    polygonRadio = QtWidgets.QRadioButton('Polygon')
    polygonRadio.clicked.connect(lambda: self.changeSelectedType('polygon'))
    typeSelector.addWidget(polygonRadio)
    
    self.formContainer.addLayout(typeSelector)
    self.typeSelector = typeSelector

  def initPointForm(self):
    pointFormWrapper = QtWidgets.QWidget(self)
    pointFormWrapper.setVisible(False)

    pointForm = QtWidgets.QFormLayout(pointFormWrapper)

    xInput = QtWidgets.QDoubleSpinBox()
    xInput.setMinimum(-10000)
    xInput.setMaximum(10000)
    pointForm.addRow('X', xInput)

    yInput = QtWidgets.QDoubleSpinBox()
    yInput.setMinimum(-10000)
    yInput.setMaximum(10000)
    pointForm.addRow('Y', yInput)

    submitButton = QtWidgets.QPushButton('Insert', pointFormWrapper)
    submitButton.clicked.connect(self.insertNewPoint)
    pointForm.addRow('', submitButton)
    
    self.formContainer.addWidget(pointFormWrapper)
    self.pointFormWrapper = pointFormWrapper

  @QtCore.Slot(str)
  def changeSelectedType(self, type):
    if type == 'point':
      self.pointFormWrapper.setVisible(True)
    else:
      self.pointFormWrapper.setVisible(False)

  @QtCore.Slot(str)
  def insertNewPoint(self):
    pointForm = self.pointFormWrapper.children()[0]
    xFormItem = pointForm.itemAt(0, QtWidgets.QFormLayout.FieldRole)
    yFormItem = pointForm.itemAt(1, QtWidgets.QFormLayout.FieldRole)
    xValue = xFormItem.widget().value()
    yValue = yFormItem.widget().value()
    self.onPointInserted.emit(Point2D(xValue, yValue))
