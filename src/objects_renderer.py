from PySide6 import QtCore, QtGui, QtWidgets

# Set as False to not draw the coordinates of each point.
# Defina como False para não desenhar as coordenadas de cada ponto.
DRAW_COORDINATES = True


def render_objects(objects_data, viewport_data):
  app = QtWidgets.QApplication()
  window = ObjectsRenderer(objects_data, viewport_data)
  window.show()
  print('SUCCESS: Objects rendered.')
  app.exec()


class ObjectsRenderer(QtWidgets.QWidget):
  def __init__(self, objectsData, viewportData):
    super().__init__()
    self.objectsData = objectsData
    self.viewportData = viewportData
    self.setWindowProperties()
    self.setBackgroundColor()


  def setWindowProperties(self):
    width = self.viewportData.min_point.x + self.viewportData.max_point.x
    height = self.viewportData.min_point.y + self.viewportData.max_point.y
    self.setFixedSize(QtCore.QSize(width, height))
    self.setWindowTitle(f'Objects (Window {width}x{height}px)')


  def setBackgroundColor(self):
    palette = self.palette()
    palette.setColor(self.backgroundRole(), QtGui.Qt.black)
    self.setPalette(palette)
    self.setAutoFillBackground(True)


  def paintEvent(self, event):
    self.drawViewportLimits()
    self.drawIndividualPoints()
    self.drawLines()
    self.drawPolygons()


  def drawViewportLimits(self):
    painter = QtGui.QPainter(self)
    pen = QtGui.QPen(QtGui.Qt.white)
    painter.setPen(pen)

    qtPoint1 = QtCore.QPointF(self.viewportData.min_point.x, self.viewportData.min_point.y)
    qtPoint2 = QtCore.QPointF(self.viewportData.max_point.x, self.viewportData.min_point.y)
    qtPoint3 = QtCore.QPointF(self.viewportData.max_point.x, self.viewportData.max_point.y)
    qtPoint4 = QtCore.QPointF(self.viewportData.min_point.x, self.viewportData.max_point.y)

    qtLine1 = QtCore.QLineF(qtPoint1, qtPoint2)
    qtLine2 = QtCore.QLineF(qtPoint2, qtPoint3)
    qtLine3 = QtCore.QLineF(qtPoint3, qtPoint4)
    qtLine4 = QtCore.QLineF(qtPoint4, qtPoint1)
    
    painter.drawLine(qtLine1)
    painter.drawLine(qtLine2)
    painter.drawLine(qtLine3)
    painter.drawLine(qtLine4)

    qtTextPoint = QtCore.QPointF(self.viewportData.min_point.x + 5, self.viewportData.min_point.y + 12)
    self.drawText(painter, qtTextPoint, 'VIEWPORT LIMITS')


  def drawText(self, painter, qtPoint, text):
    painter.setFont(QtGui.QFont('Arial', 7))
    painter.drawText(qtPoint, text)


  def drawIndividualPoints(self):
    painter = QtGui.QPainter(self)
    pen = QtGui.QPen(QtGui.Qt.green)
    painter.setPen(pen)

    for point in self.objectsData['individual_points']:
      qtPoint = QtCore.QPointF(point.x, point.y)
      painter.drawPoint(qtPoint)
      self.drawCoordinatesText(painter, qtPoint)


  def drawLines(self):
    painter = QtGui.QPainter(self)
    pen = QtGui.QPen(QtGui.Qt.cyan)
    painter.setPen(pen)

    for line in self.objectsData['lines']:
      qtPoint1 = QtCore.QPointF(line.point_1.x, line.point_1.y)
      qtPoint2 = QtCore.QPointF(line.point_2.x, line.point_2.y)
      qtLine = QtCore.QLineF(qtPoint1, qtPoint2)
      painter.drawLine(qtLine)
      self.drawCoordinatesText(painter, qtPoint1)
      self.drawCoordinatesText(painter, qtPoint2)


  def drawPolygons(self):
    painter = QtGui.QPainter(self)
    pen = QtGui.QPen(QtGui.Qt.magenta)
    painter.setPen(pen)

    for polygon in self.objectsData['polygons']:
      qtPolygon = QtGui.QPolygonF()
      for point in polygon.get_points():
        qtPoint = QtCore.QPointF(point.x, point.y)
        qtPolygon.append(qtPoint)
        self.drawCoordinatesText(painter, qtPoint)
      painter.drawPolygon(qtPolygon)
  

  def drawCoordinatesText(self, painter, qtPoint):
    if not DRAW_COORDINATES: return

    x, y = qtPoint.x(), qtPoint.y()
    tooltipPoint = QtCore.QPointF(x + 5, y + 10)
    self.drawText(painter, tooltipPoint, f'({x}, {y})')
