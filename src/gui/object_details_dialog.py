from PySide6 import QtWidgets
from utils.font import get_custom_font


DIALOG_TITLE = 'Object Details'


class ObjectDetailsDialog(QtWidgets.QDialog):
  def __init__(self, objectPoints, objectName):
    super().__init__()
    self.objectPoints = objectPoints
    self.objectName = objectName
    self.setWindowProperties()
    self.initUI()

  def setWindowProperties(self):
    self.setWindowTitle(DIALOG_TITLE)
    self.setModal(True)
    self.setFixedSize(250, 250)

  def initUI(self):
    self.initMainContainer()
    self.initPointList()
    
  def initMainContainer(self):
    self.mainContainer = QtWidgets.QVBoxLayout()

    title = QtWidgets.QLabel(DIALOG_TITLE)
    title.setFont(get_custom_font('bold', 14))
    self.mainContainer.addWidget(title)

    objectType = QtWidgets.QLabel(self.objectName)
    objectType.setFont(get_custom_font('bold'))
    self.mainContainer.addWidget(objectType)

    self.setLayout(self.mainContainer)

  def initPointList(self):
    self.pointsList = QtWidgets.QGridLayout()
    pointListWrapper = QtWidgets.QWidget()
    pointListWrapper.setLayout(self.pointsList)

    pointListScrollArea = QtWidgets.QScrollArea()
    pointListScrollArea.setWidget(pointListWrapper)
    pointListScrollArea.setFixedHeight(150)
    pointListScrollArea.setWidgetResizable(True)

    for index in range(len(self.objectPoints)):
      point = self.objectPoints[index]

      pointNumber = QtWidgets.QLabel(f'P{index + 1}')
      pointNumber.setFont(get_custom_font('bold'))

      xLabel = QtWidgets.QLabel('X = ')
      xLabel.setFont(get_custom_font('bold'))

      yLabel = QtWidgets.QLabel('Y = ')
      yLabel.setFont(get_custom_font('bold'))

      self.pointsList.addWidget(pointNumber, index, 0)
      self.pointsList.addWidget(QtWidgets.QLabel(''), index, 1)
      self.pointsList.addWidget(QtWidgets.QLabel(''), index, 4)
      self.pointsList.addWidget(xLabel, index, 2)
      self.pointsList.addWidget(QtWidgets.QLabel(f'{point.x}'), index, 3)
      self.pointsList.addWidget(yLabel, index, 5)
      self.pointsList.addWidget(QtWidgets.QLabel(f'{point.y}'), index, 6)

    self.mainContainer.addWidget(pointListScrollArea)
