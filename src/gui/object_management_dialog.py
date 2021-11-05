from PySide6 import QtWidgets
from utils.font import get_custom_font


DIALOG_TITLE = 'Edit/Remove Objects'


class ObjectManagementDialog(QtWidgets.QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowProperties()
    self.initUI()

  def setWindowProperties(self):
    self.setWindowTitle(DIALOG_TITLE)
    self.setModal(True)
    self.setFixedSize(500, 400)

  def initUI(self):
    self.initMainContainer()

  def initMainContainer(self):
    self.mainContainer = QtWidgets.QVBoxLayout()

    title = QtWidgets.QLabel(DIALOG_TITLE)
    title.setFont(get_custom_font('bold', 14))
    self.mainContainer.addWidget(title)
    
    self.setLayout(self.mainContainer)
