from PySide6 import QtGui


def get_custom_font(weight, size = 12):
  font = QtGui.QFont()
  font.setPixelSize(size)

  if weight == 'light':
    font.setWeight(QtGui.QFont.Weight.Light)
  elif weight == 'normal':
    font.setWeight(QtGui.QFont.Weight.Normal)
  elif weight == 'medium':
    font.setWeight(QtGui.QFont.Weight.Medium)
  elif weight == 'bold':
    font.setWeight(QtGui.QFont.Weight.Bold)
  elif weight == 'black':
    font.setWeight(QtGui.QFont.Weight.Black)

  return font
