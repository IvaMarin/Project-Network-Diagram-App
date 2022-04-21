import math
import numpy as np

from BNG.src.python.graph import GraphModel as graph_model
from BNG.src.python.graph import Controller as controller

from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QIcon, QPolygonF
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QToolBar, QAction

# функция для вычисления точек полигона стрелки
def calculate_arrow_points(start_point = QPointF, end_point = QPointF, radius = 30):
    try:
        arrow_height = 10
        arrow_width = 10

        dx = start_point.x() - end_point.x()
        dy = start_point.y() - end_point.y()

        length = math.sqrt(dx ** 2 + dy ** 2)

        # нормализуем
        norm_x, norm_y = dx / length, dy / length

        # перпендикулярный вектор
        perpendicular_x = -norm_y
        perpendicular_y = norm_x

        middle_point_x = end_point.x() + radius * norm_x
        middle_point_y = end_point.y() + radius * norm_y
        middle_point = QPointF(middle_point_x, middle_point_y)

        left_point_x = middle_point.x() + arrow_height * norm_x + arrow_width * perpendicular_x
        left_point_y = middle_point.y() + arrow_height * norm_y + arrow_width * perpendicular_y
        left_point = QPointF(left_point_x, left_point_y)

        right_point_x = middle_point.x() + arrow_height * norm_x - arrow_height * perpendicular_x
        right_point_y = middle_point.y() + arrow_height * norm_y - arrow_width * perpendicular_y
        right_point = QPointF(right_point_x, right_point_y)

        return QPolygonF([left_point, middle_point, right_point])

    except (ZeroDivisionError, Exception):
        return None


class Display(QWidget):

    def __init__(self):
        super().__init__()
        self.functionAble = "" #контролер действия (флаг)
        self.r = 30
        #self.initUI()
        self.Graph = graph_model.Graph(self.r) #создаем объект класса Граф

    def mousePressEvent(self, event):
        if (self.functionAble == "Добавить вершину"):
            controller.CAddPoint(self.Graph, event, Qt.LeftButton)
        elif (self.functionAble == "Добавить связь"):
            controller.CConnectPoints(self.Graph, event, Qt.LeftButton)
        elif(self.functionAble == "Удалить вершину"):
            controller.CDeletePoint(self.Graph, event, Qt.LeftButton)
        elif(self.functionAble == "Удалить связь"):
            print("Щас буду удалять")
            controller.CDeleteConnection(self.Graph, event, Qt.LeftButton)

        self.update()

    def mouseMoveEvent(self, event):
        # смотрим на все вершины и проверяем не двигают ли их
        # если да, то добавляем новые координаты в points
        # окно чувствительности rxr
        if (self.functionAble == "Переместить вершины"):
            controller.CMovePoint(self.Graph, event)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))
        if(len(self.Graph.ConnectedPoints) >= 2): # не заходит в отрисовку почему-то???
            painter.setPen(QColor(0, 0, 0))
            painter.setPen(Qt.PenStyle.SolidLine)
            # проходимся по массиву с шагом 2 и соединяем отмеченные вершины
            # тут берутся актуальные координаты из массива self.Graph.CoordCentrePoint
            for i in range(0, len(self.Graph.ConnectedPoints), 2):
                # проверка на случай, если число отмеченных вершин нечетное
                # а именно, чтобы индекс текущей парной вершины была в массиве
                # тут условие не проходит походу, такое оущщение что отрисовывает только 1ую пару
                if (i + 1 < len(self.Graph.ConnectedPoints) and (self.Graph.PointsIsVisible[self.Graph.ConnectedPoints[i]] and self.Graph.PointsIsVisible[self.Graph.ConnectedPoints[i+1]])):
                    triangle_source = calculate_arrow_points(self.Graph.CoordCentrePoint[self.Graph.ConnectedPoints[i]], self.Graph.CoordCentrePoint[self.Graph.ConnectedPoints[i+1]])
                    if triangle_source is not None:
                        painter.setBrush(QColor(0, 0, 0))
                        painter.drawPolygon(triangle_source)
                        painter.setPen(QColor(0, 0, 0))
                        painter.setPen(Qt.PenStyle.SolidLine)
                    painter.drawLine((int)(self.Graph.CoordCentrePoint[self.Graph.ConnectedPoints[i]].x()),
                                    (int)(self.Graph.CoordCentrePoint[self.Graph.ConnectedPoints[i]].y()),
                                    (int)(self.Graph.CoordCentrePoint[self.Graph.ConnectedPoints[i+1]].x()),
                                    (int)(self.Graph.CoordCentrePoint[self.Graph.ConnectedPoints[i+1]].y()))
                    #self.Graph.ConnectedPoints = np.delete(self.Graph.ConnectedPoints, -2)
                    #self.Graph.ConnectedPoints = np.delete(self.Graph.ConnectedPoints, -1)

        # обеспечиваем закрашивание вершин графа
        painter.setBrush(QColor(0, 0, 0))
        # отрисовываем вершины и цифры
        offset = QPointF(-2.5, 5)

        for i in range(len(self.Graph.CoordCentrePoint)):
            if (self.Graph.PointsIsVisible[i] == True):
                painter.drawEllipse(self.Graph.CoordCentrePoint[i], self.r, self.r)
                #print(self.Graph.CoordCentrePoint[i].x())
                painter.setPen(QColor("white"))
                painter.drawText(self.Graph.CoordCentrePoint[i] + offset, f'{i+1}')
                painter.setPen(QColor(0, 0, 0))

