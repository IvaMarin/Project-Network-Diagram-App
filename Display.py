import numpy as np

from PyQt5.QtCore import Qt, QRect, QPointF, QLineF
from PyQt5.QtGui import QPainter, QColor, QPolygonF, QPen
from PyQt5.QtWidgets import QApplication, QWidget

import controller as control
import graph_model as gm
import checker

# матрица смежности соответствующая варианту 1, 
# в дальнейшемй нужно заменить на считывание из файла
CorrectAdjacencyMatrix1 = np.array([[0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
                                    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

# функция для вычисления точек полигона стрелки
def calculate_arrow_points(start_point, end_point, radius):
    try:
        arrow_height = 10
        arrow_width = 10

        dx = start_point[0] - end_point[0]
        dy = start_point[1] - end_point[1]

        length = np.sqrt(dx ** 2 + dy ** 2)

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

# создание сетки 
def createGrid(x0=0, y0=0, step=50, vertical=True, horizontal=True):
    sizeWindow = QRect(QApplication.desktop().screenGeometry())
    lines = []

    if vertical:
        number_vertical_lines = (sizeWindow.width() - x0) // step + 1  # количество вертикальных линий
        for i in range(number_vertical_lines):
            lines.append(QLineF(x0, 0, x0, sizeWindow.height()))
            x0 = x0 + step

    if horizontal:
        number_horizontal_lines = (sizeWindow.height() - y0) // step + 1;  # количество горизонтальных линий
        for i in range(number_horizontal_lines):
            lines.append(QLineF(0, y0, sizeWindow.width(), y0))
            y0 = y0 + step

    return lines

graph = gm.Graph(60) # объект граф

class Display(QWidget):

    def __init__(self):
        super().__init__()
        self.functionAble = "Добавить вершину"
        self.TempPoints = np.empty(0) # массив временно выделенных вершин

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing) # убирает пикселизацию

        # отрисовка сетки
        painter.setPen(QColor(0, 0, 255, 90))
        lines = createGrid(0, 0, 50, True, True)
        painter.drawLines(lines)

        painter.setPen(QColor("black"))
        painter.setPen(Qt.PenStyle.SolidLine)  # тут можно использовать Qt.PenStyle.DashLine для пунктирных линий
        painter.setBrush(QColor("black"))

        # отрисовка стрелок
        for i in range(len(graph.AdjacencyMatrix)):
            for j in range(len(graph.AdjacencyMatrix)):
                # если существует связь
                if (graph.AdjacencyMatrix[i][j] != 0 and 
                    (not np.isnan(graph.Points[i][0])) and
                    (not np.isnan(graph.Points[j][0]))):
                    triangle_source = calculate_arrow_points(graph.Points[i], graph.Points[j], graph.RadiusPoint/2)
                    if triangle_source is not None:
                        painter.drawPolygon(triangle_source)
                        painter.drawLine((int)(graph.Points[i][0]),
                                         (int)(graph.Points[i][1]),
                                         (int)(graph.Points[j][0]),
                                         (int)(graph.Points[j][1]))

        # отрисовка вершин и цифр
        painter.setPen(QPen(QColor("black"), 2.5))
        painter.setBrush(QColor("white")) # обеспечиваем закрашивание вершин графа
        for i in range(len(graph.Points)):
            # если вершина существует
            if (not np.isnan(graph.Points[i][0])):
                painter.drawEllipse(graph.Points[i][0]-graph.RadiusPoint/2, graph.Points[i][1]-graph.RadiusPoint/2, 
                                    graph.RadiusPoint, graph.RadiusPoint)
                offset = [-(5*len(str(i+1)) - 2.5), 5] # определим смещение по длине строки номера вершины
                painter.drawText(graph.Points[i][0] + offset[0], graph.Points[i][1] + offset[1], f'{i+1}')

    def mousePressEvent(self, event):
        # нажатие на ЛКМ
        if (self.functionAble == "Добавить вершину"):
            control.CAddPoint(graph, event, Qt.LeftButton)

        elif (self.functionAble == "Добавить связь"):
            self.TempPoints = np.append(self.TempPoints, graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # добавить в массив выбранных вершин
            # если число выбранных вершин 2
            if len(self.TempPoints) == 2:
                # проверка, если пользователь случайно нажал дважды по одной и той же вершине
                if (self.TempPoints[0] != self.TempPoints[1]):
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
        
    def checkEvent(self):
        mistakes = checker.checkTask1(graph, CorrectAdjacencyMatrix1)
        return mistakes


class Display2(Display):

    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing) # убирает пикселизацию

        # отрисовка сетки
        painter.setPen(QColor(0, 0, 255, 90))
        lines = createGrid(0, 0, 50, True, True)
        painter.drawLines(lines)

        painter.setPen(QColor("black"))
        painter.setPen(Qt.PenStyle.SolidLine)  # тут можно использовать Qt.PenStyle.DashLine для пунктирных линий
        painter.setBrush(QColor("black"))

        # отрисовка стрелок
        scaler = 1.5
        radius = graph.RadiusPoint * scaler
        for i in range(len(graph.AdjacencyMatrix)):
            for j in range(len(graph.AdjacencyMatrix)):
                # если существует связь
                if (graph.AdjacencyMatrix[i][j] != 0 and 
                    (not np.isnan(graph.Points[i][0])) and
                    (not np.isnan(graph.Points[j][0]))):
                    triangle_source = calculate_arrow_points(graph.Points[i], graph.Points[j], radius/2)
                    if triangle_source is not None:
                        painter.drawPolygon(triangle_source)
                        painter.drawLine((int)(graph.Points[i][0]),
                                         (int)(graph.Points[i][1]),
                                         (int)(graph.Points[j][0]),
                                         (int)(graph.Points[j][1]))
                        # определим где отрисовать вес ребра/стрелки
                        cos_sign = graph.Points[j][0] - graph.Points[i][0]
                        sin_sign = graph.Points[j][1] - graph.Points[i][1]
                        offset = 10
                        if ((cos_sign > 0 and sin_sign > 0) or (cos_sign < 0 and sin_sign < 0)):
                            x = ((int)(graph.Points[i][0]) + (int)(graph.Points[j][0])) / 2 + offset
                        else:
                            x = ((int)(graph.Points[i][0]) + (int)(graph.Points[j][0])) / 2 - offset
                        y = ((int)(graph.Points[i][1]) + (int)(graph.Points[j][1])) / 2 - offset

                        # сюда нужно передать парметр веса для i-го ребра
                        weight = 'w'
                        painter.drawText(x, y, f'{weight}')

        # отрисовка вершин и цифр
        painter.setPen(QPen(QColor("black"), 2.5))
        painter.setBrush(QColor("white")) # обеспечиваем закрашивание вершин графа
        for i in range(len(graph.Points)):
            # если вершина существует
            if (not np.isnan(graph.Points[i][0])):
                x, y = graph.Points[i]
                
                painter.drawEllipse(x-radius/2, y-radius/2, radius, radius)

                line_off = (radius/2) * np.cos(np.pi/4)

                painter.drawLine(x-line_off, y-line_off, x+line_off, y+line_off)
                painter.drawLine(x-line_off, y+line_off, x+line_off, y-line_off)
                
                # сюда нужно передавать три параметра для секторов i-ой вершины
                t_p = 't^p'
                t_n = 't^n'
                R = 'R'

                x_off = -(5*len(str(t_p)) - 2.5) # по оси x определим смещение по длине строки
                y_off = 5                        # по оси y смещение не зависист от длины строки 
                painter.drawText(x-line_off+x_off/2, y+y_off, f'{t_p}')

                x_off = -(5*len(str(t_n)) - 2.5) # по оси x определим смещение по длине строки
                painter.drawText(x+line_off+1.5*x_off, y+y_off, f'{t_n}')

                x_off = -(5*len(str(i+1)) - 2.5) # по оси x определим смещение по длине строки
                painter.drawText(x+x_off, y-line_off+1.5*y_off, f'{i+1}')

                x_off = -(5*len(str(R)) - 2.5)   # по оси x определим смещение по длине строки
                painter.drawText(x+x_off, y+line_off, f'{R}')

    # забираем у пользователя возможность что-то двигать/нажимать
    def mousePressEvent(self, event):
        pass
    def mouseMoveEvent(self, event):
        pass

    # тут должна быть проверка для второго задания
    def checkEvent(self):
        pass