from PySide6 import QtGui


def get_custom_font(weight, size = 12):
  font = QtGui.QFont()
  font.setPixelSize(size)

  if weight == 'light':
    font.setWeight(QtGui.QFont.Weight.Light)
  if weight == 'normal':
    font.setWeight(QtGui.QFont.Weight.Normal)
  if weight == 'medium':
    font.setWeight(QtGui.QFont.Weight.Medium)
  if weight == 'bold':
    font.setWeight(QtGui.QFont.Weight.Bold)
  if weight == 'black':
    font.setWeight(QtGui.QFont.Weight.Black)

  return font
