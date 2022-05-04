import sys, math
import numpy as np


from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QIcon, QCursor, QPolygonF
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QMenu, QToolBar, QAction

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRect

import controller as control
import graph_model as gm

# функция для вычисления точек полигона стрелки
def calculate_arrow_points(start_point, end_point, radius=30):
    try:
        arrow_height = 10
        arrow_width = 10

        dx = start_point[0] - end_point[0]
        dy = start_point[1] - end_point[1]

        length = math.sqrt(dx ** 2 + dy ** 2)

        # нормализуем
        norm_x, norm_y = dx / length, dy / length

        # перпендикулярный вектор
        perpendicular_x = -norm_y
        perpendicular_y = norm_x

        middle_point_x = end_point[0] + radius * norm_x
        middle_point_y = end_point[1] + radius * norm_y
        middle_point = QPointF(middle_point_x, middle_point_y)

        left_point_x = middle_point_x + arrow_height * norm_x + arrow_width * perpendicular_x
        left_point_y = middle_point_y + arrow_height * norm_y + arrow_width * perpendicular_y
        left_point = QPointF(left_point_x, left_point_y)

        right_point_x = middle_point_x + arrow_height * norm_x - arrow_height * perpendicular_x
        right_point_y = middle_point_y + arrow_height * norm_y - arrow_width * perpendicular_y
        right_point = QPointF(right_point_x, right_point_y)

        return QPolygonF([left_point, middle_point, right_point])

    except (ZeroDivisionError, Exception):
        return None

graph = gm.Graph(60) # объект граф

class Display(QWidget):

    def __init__(self):
        super().__init__()
        self.functionAble = "Добавить вершину"
        self.initUI()

    def initUI(self):
        self.TempPoints = np.empty(0) # массив временно выделенных вершин

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))
        # painter.setRenderHint(painter.Antialiasing)

        painter.setPen(QColor(0, 0, 0))
        painter.setPen(Qt.PenStyle.SolidLine)  # тут можно использовать Qt.PenStyle.DashLine для пунктирных линий
        # по матрицу смежности
        for i in range(len(graph.AdjacencyMatrix)):
            for j in range(len(graph.AdjacencyMatrix)):
                # если существует связь
                if (graph.AdjacencyMatrix[i][j] != 0):
                    triangle_source = calculate_arrow_points(graph.Points[i], graph.Points[j])
                    if triangle_source is not None:
                        painter.setBrush(QColor(0, 0, 0))
                        painter.drawPolygon(triangle_source)
                        painter.setPen(QColor(0, 0, 0))
                        painter.setPen(Qt.PenStyle.SolidLine)
                        painter.drawLine((int)(graph.Points[i][0]),
                                     (int)(graph.Points[i][1]),
                                     (int)(graph.Points[j][0]),
                                     (int)(graph.Points[j][1]))

                    # обеспечиваем закрашивание вершин графа
        painter.setBrush(QColor(0, 0, 0))

        # отрисовка вершин и цифр
        offset = [-2.5, 5]
        # по всем вершинам
        for i in range(len(graph.Points)):
            # если вершина существует
            if (not np.isnan(graph.Points[i][0])):
                painter.drawEllipse(graph.Points[i][0]-graph.RadiusPoint/2, graph.Points[i][1]-graph.RadiusPoint/2, graph.RadiusPoint, graph.RadiusPoint)
                painter.setPen(QColor("white"))
                painter.drawText(graph.Points[i][0] + offset[0], graph.Points[i][1] + offset[1], f'{i}')
                painter.setPen(QColor(0, 0, 0))

    def mousePressEvent(self, event):
        # нажатие на ЛКМ
        if (self.functionAble == "Добавить вершину"):
            control.CAddPoint(graph, event, Qt.LeftButton)
        elif (self.functionAble == "Добавить связь"):
            self.TempPoints = np.append(self.TempPoints, graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # добавить в массив выбранных вершин
            # если число выбранных вершин 2
            if len(self.TempPoints) == 2:
                control.CConnectPoints(graph, event, Qt.LeftButton, self.TempPoints)
                self.TempPoints = np.empty(0) # очистить массив
        elif (self.functionAble == "Удалить связь"):
            self.TempPoints = np.append(self.TempPoints, graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # добавить в массив выбранных вершин
            # если число выбранных вершин 2
            if len(self.TempPoints) == 2:
                control.CDeleteConnection(graph, event, Qt.LeftButton, self.TempPoints)
                self.TempPoints = np.empty(0) # очистить массив
        elif (self.functionAble == "Удалить вершину"):
            control.CDeletePoint(graph, event, Qt.LeftButton)

        self.update()

    def mouseMoveEvent(self, event):
        if (self.functionAble == "Переместить вершины"):
            control.CMovePoint(graph, event)

        self.update()
