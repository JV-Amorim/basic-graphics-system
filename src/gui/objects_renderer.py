from PySide6 import QtCore, QtGui, QtWidgets


OBJECTS_RENDERER_DIMENSIONS = (640, 480)


class ObjectsRenderer(QtWidgets.QWidget):
  def __init__(self, viewportDict, windowDict, isClippingEnabled, isDrawCoordinatesEnabled):
    super().__init__()
    self.viewportDict, self.windowDict = viewportDict, windowDict
    self.isClippingEnabled = isClippingEnabled
    self.isDrawCoordinatesEnabled = isDrawCoordinatesEnabled
    self.viewport = windowDict['viewport']
    self.setWidgetSize()
    self.setBackgroundColor()
    print('Objects rendered.')

  def setWidgetSize(self):
    width = OBJECTS_RENDERER_DIMENSIONS[0]
    height = OBJECTS_RENDERER_DIMENSIONS[1]
    self.setFixedSize(QtCore.QSize(width, height))

  def setBackgroundColor(self):
    palette = self.palette()
    palette.setColor(self.backgroundRole(), QtGui.Qt.black)
    self.setPalette(palette)
    self.setAutoFillBackground(True)

  def paintEvent(self, event):
    self.drawIndividualPoints()
    self.drawLines()
    self.drawPolygonsUsingLines()
    self.drawViewportLimits()

  def drawViewportLimits(self):
    painter = QtGui.QPainter(self)
    pen = QtGui.QPen(QtGui.Qt.yellow)
    painter.setPen(pen)

    viewport_right_and_left_bottom_x = self.viewport.max_point.x - self.viewport.min_point.x
    viewport_right_and_left_bottom_y = self.viewport.max_point.y - self.viewport.min_point.y

    if viewport_right_and_left_bottom_x >= OBJECTS_RENDERER_DIMENSIONS[0]:
      viewport_right_and_left_bottom_x = OBJECTS_RENDERER_DIMENSIONS[0] - 1
    if viewport_right_and_left_bottom_y >= OBJECTS_RENDERER_DIMENSIONS[1]:
      viewport_right_and_left_bottom_y = OBJECTS_RENDERER_DIMENSIONS[1] - 1

    qtPoint1 = QtCore.QPointF(0, 0)
    qtPoint2 = QtCore.QPointF(viewport_right_and_left_bottom_x, 0)
    qtPoint3 = QtCore.QPointF(viewport_right_and_left_bottom_x, viewport_right_and_left_bottom_y)
    qtPoint4 = QtCore.QPointF(0, viewport_right_and_left_bottom_y)

    qtLine1 = QtCore.QLineF(qtPoint1, qtPoint2)
    qtLine2 = QtCore.QLineF(qtPoint2, qtPoint3)
    qtLine3 = QtCore.QLineF(qtPoint3, qtPoint4)
    qtLine4 = QtCore.QLineF(qtPoint4, qtPoint1)
    
    painter.drawLine(qtLine1)
    painter.drawLine(qtLine2)
    painter.drawLine(qtLine3)
    painter.drawLine(qtLine4)

    qtTextPoint = QtCore.QPointF(viewport_right_and_left_bottom_x - 53, viewport_right_and_left_bottom_y - 5)
    self.drawText(painter, qtTextPoint, 'VIEWPORT')

  def drawText(self, painter, qtPoint, text):
    painter.setFont(QtGui.QFont('Arial', 7))
    painter.drawText(qtPoint, text)

  def drawIndividualPoints(self):
    painter = QtGui.QPainter(self)
    pen = QtGui.QPen(QtGui.Qt.green)
    painter.setPen(pen)

    for point in self.viewportDict['individual_points']:
      if self.isClippingEnabled and point.completely_clipped:
        continue
      qtPoint = QtCore.QPointF(point.x, point.y)
      painter.drawPoint(qtPoint)
      self.drawCoordinatesText(painter, qtPoint)

  def drawLines(self):
    painter = QtGui.QPainter(self)
    pen = QtGui.QPen(QtGui.Qt.cyan)
    painter.setPen(pen)

    for line in self.viewportDict['lines']:
      self.drawLine(painter, line)
  
  def drawLine(self, painter, line):
    if self.isClippingEnabled:
      if line.completely_clipped:
        return
      qtPoint1 = QtCore.QPointF(line.clipped_point_1.x, line.clipped_point_1.y)
      qtPoint2 = QtCore.QPointF(line.clipped_point_2.x, line.clipped_point_2.y)
      qtLine = QtCore.QLineF(qtPoint1, qtPoint2)
    else:
      qtPoint1 = QtCore.QPointF(line.point_1.x, line.point_1.y)
      qtPoint2 = QtCore.QPointF(line.point_2.x, line.point_2.y)
      qtLine = QtCore.QLineF(qtPoint1, qtPoint2)
    
    painter.drawLine(qtLine)
    self.drawCoordinatesText(painter, qtPoint1)
    self.drawCoordinatesText(painter, qtPoint2)

  def drawPolygonsUsingLines(self):
    painter = QtGui.QPainter(self)
    pen = QtGui.QPen(QtGui.Qt.magenta)
    painter.setPen(pen)

    for polygon in self.viewportDict['polygons']:
      for line in polygon.lines:
        self.drawLine(painter, line)

  def drawPolygonsUsingPoints(self):
    painter = QtGui.QPainter(self)
    pen = QtGui.QPen(QtGui.Qt.magenta)
    painter.setPen(pen)

    for polygon in self.viewportDict['polygons']:
      qtPolygon = QtGui.QPolygonF()
      for point in polygon.get_points():
        qtPoint = QtCore.QPointF(point.x, point.y)
        qtPolygon.append(qtPoint)
        self.drawCoordinatesText(painter, qtPoint)
      painter.drawPolygon(qtPolygon)
  
  def drawCoordinatesText(self, painter, qtPoint):
    if not self.isDrawCoordinatesEnabled: return

    x, y = qtPoint.x(), qtPoint.y()
    tooltipPoint = QtCore.QPointF(x + 5, y + 10)
    self.drawText(painter, tooltipPoint, f'({x:.0f}, {y:.0f})')
