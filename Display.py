from contextlib import nullcontext
from matplotlib import lines
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys

import numpy as np

from PyQt5.QtCore import Qt, QRect, QPointF, QLineF
from PyQt5.QtGui import QPainter, QColor, QPolygonF, QPen, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit

import controller as control
import graph_model as gm
import checker


# функция для вычисления точек полигона стрелки
def calculate_arrow_points(start_point, end_point, radius):
    try:
        arrow_height = 10
        arrow_width = 10

        dx = start_point[0] - end_point[0]
        dy = start_point[1] - end_point[1]

        length = np.sqrt(dx ** 2 + dy ** 2)

        # нормализуем
        if (length == 0):
            norm_x, norm_y = 0, 0
        else:
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

        number_vertical_lines = (sizeWindow.width()*2 - x0) // step + 1  # количество вертикальных линий

        for i in range(number_vertical_lines):
            lines.append(QLineF(x0, 0, x0, sizeWindow.height()))
            x0 = x0 + step

    if horizontal:
        number_horizontal_lines = (sizeWindow.height()*2 - y0) // step + 1;  # количество горизонтальных линий
        for i in range(number_horizontal_lines):
            lines.append(QLineF(0, y0, sizeWindow.width()*2, y0))
            y0 = y0 + step

    return lines

# промежутки в сетке под цифры
def createGaps(x0=0, y0=0, step=50, sizeNumber = 40, yNumber = 170):
    sizeWindow = QRect(QApplication.desktop().screenGeometry())
    lines = []
    sizeNumber = sizeNumber / 2

    x0 = x0 + step
    
    number_vertical_lines = (sizeWindow.width() - x0) // step + 1  # количество вертикальных линий
    for i in range(number_vertical_lines):
        lines.append(QLineF(x0, sizeWindow.height() - yNumber - sizeNumber, x0, sizeWindow.height() - yNumber + sizeNumber))
        x0 = x0 + step

    return lines

class Display(QWidget):
    FixedPoint = -1 # фиксированная вершина
    FixedArrowPoint = [-1, -1] # фиксированная стрелка
    def __init__(self, root, graph_in, start_coordination_X = 0, start_coordination_Y = 0, step = 50, color = [0, 0, 255, 90], horizontal = True, late_time = None, base_graph = None, switch = True):
        super().__init__(root)
        self.functionAble = ""
        self.TempPoints = np.empty(0) # массив временно выделенных вершин
        self.colorGrid = QColor(color[0],color[1],color[2],color[3])
        self.start_coordination_X = start_coordination_X
        self.start_coordination_Y = start_coordination_Y
        self.step = step
        self.graph = graph_in
        self.late_time = late_time # поле определяющее как мы изображаем пунктирную стрелку, True - в поздних, False - в ранних, None - в зависимости от резерва времени
        if (base_graph == None):
            self.base_graph = self.graph
        else:
            self.base_graph = base_graph
        if horizontal:
            self.lines = createGrid(start_coordination_X, start_coordination_Y, step, True, True)
        else:
            self.lines = createGrid(start_coordination_X, start_coordination_Y, step, True, False)
        self.whiteLines = createGaps(start_coordination_X, start_coordination_Y, step)
        self.graph_in = graph_in
        self.switch = switch
        self.illumination = -1  #подсветка кружков
        # print(root.sizeGet())


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing) # убирает пикселизацию

        # отрисовка сетки
        painter.setPen(self.colorGrid)
        #lines = createGrid(0, 0, 50, True, True)
        painter.drawLines(self.lines)

        painter.setPen(QColor("black"))
        font = "Times"
        font_size = 12
        painter.setFont(QFont(font, font_size))
        painter.setPen(Qt.PenStyle.SolidLine)  # тут можно использовать Qt.PenStyle.DashLine для пунктирных линий
        painter.setBrush(QColor("black"))

        # отрисовка стрелок
        for i in range(len(self.graph.AdjacencyMatrix)):
            for j in range(len(self.graph.AdjacencyMatrix)):
                # если существует связь
                if (self.graph.AdjacencyMatrix[i][j] != 0 and 
                    (not np.isnan(self.graph.Points[i][0])) and
                    (not np.isnan(self.graph.Points[j][0]))):
                    triangle_source = calculate_arrow_points(self.graph.Points[i], self.graph.Points[j], self.graph.RadiusPoint)
                    if triangle_source is not None:
                        painter.drawPolygon(triangle_source)
                        painter.drawLine((int)(self.graph.Points[i][0]),
                                         (int)(self.graph.Points[i][1]),
                                         (int)(self.graph.Points[j][0]),
                                         (int)(self.graph.Points[j][1]))

        # отрисовка вершин и цифр
        painter.setPen(QPen(QColor("black"), 2.5))
         
        for i in range(len(self.graph.Points)):
            # если вершина существует
            if (not np.isnan(self.graph.Points[i][0])):
                if (i != self.illumination):
                    painter.setBrush(QColor("white"))# обеспечиваем закрашивание вершин графа
                else:
                    painter.setBrush(QColor(127, 255, 212, 255))# обеспечиваем закрашивание вершин графа

                painter.drawEllipse(self.graph.Points[i][0]-self.graph.RadiusPoint, self.graph.Points[i][1]-self.graph.RadiusPoint, 
                                    2*self.graph.RadiusPoint, 2*self.graph.RadiusPoint)
                if len(str(i+1)) < 2:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
                else:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины               
                painter.drawText(self.graph.Points[i][0] + offset[0], self.graph.Points[i][1] + offset[1], f'{i}')

    def mousePressEvent(self, event):
        # нажатие на ЛКМ
        if (self.functionAble == "Добавить вершину"):
            control.CAddPoint(self.graph, event, Qt.LeftButton)

        elif (self.functionAble == "Добавить связь"):
            self.TempPoints = np.append(self.TempPoints, self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # добавить в массив выбранных вершин
            self.illumination = self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())
            # если число выбранных вершин 2
            if len(self.TempPoints) == 2:
                # проверка, если пользователь случайно нажал дважды по одной и той же вершине
                if (self.TempPoints[0] != self.TempPoints[1]):
                    control.CConnectPoints(self.graph, event, Qt.LeftButton, self.TempPoints)

                self.TempPoints = np.empty(0) # очистить массив
                self.illumination = -1 #очистить  подсветку

        elif (self.functionAble == "Удалить связь"):
            self.TempPoints = np.append(self.TempPoints, self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # добавить в массив выбранных вершин
            self.illumination = self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())

            # если число выбранных вершин 2
            if len(self.TempPoints) == 2:
                control.CDeleteConnection(self.graph, event, Qt.LeftButton, self.TempPoints)
                self.TempPoints = np.empty(0) # очистить массив
                self.illumination = -1 
    
        elif (self.functionAble == "Удалить вершину"):
            control.CDeletePoint(self.graph, event, Qt.LeftButton)
            self.illumination = -1

        elif (self.functionAble == "Переместить вершины"):
            self.FixedPoint = control.CIsCursorOnPoint(self.graph, event, Qt.LeftButton)
            self.illumination = -1
            self.TempPoints = np.empty(0)

        self.update()

    def mouseMoveEvent(self, event):
        if (self.functionAble == "Переместить вершины"):
            control.CMovePoint(self.graph, event, Qt.LeftButton, self.FixedPoint)
        self.update()
        
    def checkEvent(self):
        mistakes = checker.checkTask1(self.graph, self.graph.CorrectAdjacencyMatrix)
        return mistakes

    def _drawLabels(self):
        self.graph.label = np.zeros_like(self.graph.AdjacencyMatrix, dtype=QLineEdit)

        for i in range(len(self.graph.AdjacencyMatrix)):
            for j in range(len(self.graph.AdjacencyMatrix)):
                # если существует связь
                if (self.graph.AdjacencyMatrix[i][j] != 0 and 
                    (not np.isnan(self.graph.Points[i][0])) and
                    (not np.isnan(self.graph.Points[j][0]))):

                    # определим где отрисовать вес ребра/стрелки
                    cos_sign = self.graph.Points[j][0] - self.graph.Points[i][0]
                    sin_sign = self.graph.Points[j][1] - self.graph.Points[i][1]
                    offset = 10
                    if ((cos_sign >= 0 and sin_sign >= 0) or (cos_sign <= 0 and sin_sign <= 0)):
                        x = ((int)(self.graph.Points[i][0]) + (int)(self.graph.Points[j][0])) / 2 + offset
                    else:
                        x = ((int)(self.graph.Points[i][0]) + (int)(self.graph.Points[j][0])) / 2 - offset
                    y = ((int)(self.graph.Points[i][1]) + (int)(self.graph.Points[j][1])) / 2 - offset

                    self.graph.label[i][j] = (QLineEdit(self))
                    self.graph.label[i][j].setAlignment(Qt.AlignHCenter)

                    font = 'Times'
                    font_size = 12
                    self.graph.label[i][j].setFont(QFont(font, font_size))
                    
                    self.graph.label[i][j].move(x, y)
                    self.graph.label[i][j].resize(50,50)

                    self.graph.label[i][j].setStyleSheet("border :2px solid black;")
                    
                    self.graph.label[i][j].setInputMask("00")
                    self.graph.label[i][j].show()

class Display2(Display):

    def __init__(self, root, graph_in):
        super().__init__(root, graph_in)
        self.graph = graph_in
        self.switch = True
        self.illumination = -1 
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing) # убирает пикселизацию

        # отрисовка сетки
        painter.setPen(QColor(0, 0, 255, 90))
        # lines = createGrid(0, 0, 50, True, True)
        painter.drawLines(self.lines)

        painter.setPen(QColor("black"))
        font = 'Times'
        font_size = 12
        painter.setFont(QFont(font, font_size))
        painter.setPen(Qt.PenStyle.SolidLine)  # тут можно использовать Qt.PenStyle.DashLine для пунктирных линий
        painter.setBrush(QColor("black"))

        # отрисовка стрелок
        scaler = 3 # параметр увеличения вершин относительно первого задания
        radius = self.graph.RadiusPoint * scaler
        for i in range(len(self.graph.AdjacencyMatrix)):
            for j in range(len(self.graph.AdjacencyMatrix)):
                # если существует связь
                if (self.graph.AdjacencyMatrix[i][j] != 0 and 
                    (not np.isnan(self.graph.Points[i][0])) and
                    (not np.isnan(self.graph.Points[j][0]))):
                    # выбор цвета в зависимости от выбора критического пути
                    if (self.graph.AdjacencyMatrix[i][j] == 2):
                        painter.setBrush(QColor("red"))
                        painter.setPen(QColor("red"))
                    elif (self.graph.AdjacencyMatrix[i][j] == 1):
                        painter.setBrush(QColor("black"))
                        painter.setPen(QColor("black"))
                    triangle_source = calculate_arrow_points(self.graph.Points[i], self.graph.Points[j], radius/2)
                    if triangle_source is not None:
                        painter.drawPolygon(triangle_source)
                        painter.drawLine((int)(self.graph.Points[i][0]),
                                         (int)(self.graph.Points[i][1]),
                                         (int)(self.graph.Points[j][0]),
                                         (int)(self.graph.Points[j][1]))

        # отрисовка вершин и цифр
        painter.setPen(QPen(QColor("black"), 2.5))
        #painter.setBrush(QColor("white")) # обеспечиваем закрашивание вершин графа
        for i in range(len(self.graph.Points)):
            if (i != self.illumination):
                painter.setBrush(QColor("white"))# обеспечиваем закрашивание вершин графа
            else:
                painter.setBrush(QColor(127, 255, 212, 255))# обеспечиваем закрашивание вершин графа
            # если вершина существует
            if (not np.isnan(self.graph.Points[i][0])):
                x, y = self.graph.Points[i]
                
                painter.drawEllipse(x-radius/2, y-radius/2, radius, radius)

                line_off = (radius/2) * np.cos(np.pi/4)

                painter.drawLine(x-line_off, y-line_off, x+line_off, y+line_off)
                painter.drawLine(x-line_off, y+line_off, x+line_off, y-line_off)
                
                if (self.graph.tp.size > i):
                    t_p = str(int(self.graph.tp[i]))
                else:
                    t_p = '0'

                if (self.graph.tn.size > i):
                    t_n = str(int(self.graph.tn[i]))
                else:
                    t_n = '0'

                if (self.graph.tn.size > i and self.graph.tp.size > i):
                    R = str(int(self.graph.tn[i]) - int(self.graph.tp[i]))
                else:
                    R = '0'

                x_off = -(5*len(str(t_p))*font_size/7.8 - 2.5) # по оси x определим смещение по длине строки
                y_off = 5*font_size/8                          # по оси y смещение не зависист от длины строки 
                painter.drawText(x-line_off+x_off/2, y+y_off, f'{t_p}')

                x_off = -(5*len(str(t_n))*font_size/7.8 - 2.5) # по оси x определим смещение по длине строки
                painter.drawText(x+line_off+1.5*x_off, y+y_off, f'{t_n}')

                x_off = -(5*len(str(i+1))*font_size/7.8 - 2.5) # по оси x определим смещение по длине строки
                painter.drawText(x+x_off, y-line_off+1.5*y_off, f'{i}')

                x_off = -(5*len(str(R))*font_size/7.8 - 2.5)   # по оси x определим смещение по длине строки
                painter.drawText(x+x_off, y+line_off+0.5*y_off, f'{R}')
        
        if self.switch:
            self._drawLabels()
            self.switch = False

        self.update()

    def mousePressEvent(self, event):
        if (self.functionAble == "Критический путь"):
            self.TempPoints = np.append(self.TempPoints, self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # добавить в массив выбранных вершин
            self.illumination = self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())
            # если число выбранных вершин 2
            if len(self.TempPoints) == 2:
                # проверка, если пользователь случайно нажал дважды по одной и той же вершине
                if (self.TempPoints[0] != self.TempPoints[1]):
                    control.CSelectCriticalPath(self.graph, event, Qt.LeftButton, self.TempPoints)
                self.TempPoints = np.empty(0) # очистить массив
                self.illumination = -1 
        self.update()
    def mouseMoveEvent(self, event):
        pass

    # проверка для второго задания
    def checkEvent(self):
        mistakes = checker.checkTask2(self.graph)
        return mistakes

class Display3(Display):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing) # убирает пикселизацию

        # отрисовка сетки
        painter.setPen(self.colorGrid)
        #lines = createGrid(0, 0, 50, True, True)
        painter.drawLines(self.lines)
        painter.setPen(QColor(255, 255, 255, 255))
        painter.drawLines(self.whiteLines)

        painter.setPen(QColor("black"))
        font = 'Times'
        font_size = 12
        painter.setFont(QFont(font, font_size))
        painter.setPen(Qt.PenStyle.SolidLine)  # тут можно использовать Qt.PenStyle.DashLine для пунктирных линий
        painter.setBrush(QColor("black"))
        
        # отрисовка нумерации осей сетки
        x0 = 0
        #step = 75
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        number_vertical_lines = (sizeWindow.width() - x0) // self.step + 1  # количество вертикальных линий
        y0 = sizeWindow.height()-170
        for i in range(number_vertical_lines):
            if len(str(i+1)) < 2:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
            else:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины
            painter.drawText(self.step + self.step * i + offset[0], y0 + offset[1], f'{i}')
       
        # отрисовка стрелок
        for i in range(len(self.graph.AdjacencyMatrix)):
            for j in range(len(self.graph.AdjacencyMatrix)):
                # если существует связь
                if (self.graph.AdjacencyMatrix[i][j] != 0 and
                    (not np.isnan(self.graph.Points[i][0])) and
                        (not np.isnan(self.graph.Points[j][0]))):
                    triangle_source = calculate_arrow_points(
                        self.graph.Points[i], self.graph.ArrowPoints[i][j], 0)
                    if triangle_source is not None:
                        painter.drawPolygon(triangle_source)
                        if (self.late_time == None):  # в зависимости от резерва
                            if (len(self.base_graph.R) > i) and (self.base_graph.R[i] > 0):
                                painter.setPen(Qt.PenStyle.SolidLine)
                                painter.drawLine(QPointF(self.graph.Points[i][0],
                                                         self.graph.Points[i][1]),
                                                 triangle_source[1])
                                painter.setPen(Qt.PenStyle.DashLine)
                                painter.drawLine(triangle_source[1],
                                                 QPointF(self.graph.Points[j][0],
                                                         self.graph.Points[j][1]))
                                painter.setPen(Qt.PenStyle.SolidLine)
                            else:
                                painter.setPen(Qt.PenStyle.DashLine)
                                painter.drawLine(QPointF(self.graph.Points[i][0],
                                                         self.graph.Points[i][1]),
                                                 triangle_source[1])
                                painter.setPen(Qt.PenStyle.SolidLine)
                                painter.drawLine(triangle_source[1],
                                                 QPointF(self.graph.Points[j][0],
                                                         self.graph.Points[j][1]))
                        elif (self.late_time == True):  # в поздних сроках
                            painter.setPen(Qt.PenStyle.DashLine)
                            painter.drawLine(QPointF(self.graph.Points[i][0],
                                                     self.graph.Points[i][1]),
                                             triangle_source[1])
                            painter.setPen(Qt.PenStyle.SolidLine)
                            painter.drawLine(triangle_source[1],
                                             QPointF(self.graph.Points[j][0],
                                                     self.graph.Points[j][1]))
                        else:  # в ранних сроках
                            painter.setPen(Qt.PenStyle.SolidLine)
                            painter.drawLine(QPointF(self.graph.Points[i][0],
                                                     self.graph.Points[i][1]),
                                             triangle_source[1])
                            painter.setPen(Qt.PenStyle.DashLine)
                            painter.drawLine(triangle_source[1],
                                             QPointF(self.graph.Points[j][0],
                                                     self.graph.Points[j][1]))
                            painter.setPen(Qt.PenStyle.SolidLine)

        # отрисовка вершин и цифр
        painter.setPen(QPen(QColor("black"), 2.5))
        painter.setBrush(QColor("white")) # обеспечиваем закрашивание вершин графа
        for i in range(len(self.graph.Points)):
            # если вершина существует
            if (not np.isnan(self.graph.Points[i][0])):
                painter.drawEllipse(self.graph.Points[i][0]-self.graph.RadiusPoint, self.graph.Points[i][1]-self.graph.RadiusPoint, 
                                    2*self.graph.RadiusPoint, 2*self.graph.RadiusPoint)
                if len(str(i+1)) < 2:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
                else:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины               
                painter.drawText(self.graph.Points[i][0] + offset[0], self.graph.Points[i][1] + offset[1], f'{i}')
    
    def checkEvent3(self):
        mistakes = checker.checkTask3(self.graph, self.graph.CorrectWeights, self.start_coordination_X, self.step)
        return mistakes

    def checkEvent4(self):
        mistakes = checker.checkTask4(self.graph, self.graph.CorrectWeights, self.start_coordination_X, self.step)
        return mistakes

    def mousePressEvent(self, event):
        # нажатие на ЛКМ
        if (self.functionAble == "Добавить вершину"):
            control.CAddPointGrid(
                self.graph, event, Qt.LeftButton, self.start_coordination_X, self.step, None)

        elif (self.functionAble == "Добавить связь"):
            self.TempPoints = np.append(self.TempPoints, self.graph.IsCursorOnPoint(
                event.pos().x(), event.pos().y()))  # добавить в массив выбранных вершин
            # если число выбранных вершин 2
            if len(self.TempPoints) == 2:
                # проверка, если пользователь случайно нажал дважды по одной и той же вершине
                if (self.TempPoints[0] != self.TempPoints[1]):
                    control.CConnectPoints(
                        self.graph, event, Qt.LeftButton, self.TempPoints)
                self.TempPoints = np.empty(0)  # очистить массив

        elif (self.functionAble == "Удалить связь"):
            self.TempPoints = np.append(self.TempPoints, self.graph.IsCursorOnPoint(
                event.pos().x(), event.pos().y()))  # добавить в массив выбранных вершин
            # если число выбранных вершин 2
            if len(self.TempPoints) == 2:
                control.CDeleteConnection(
                    self.graph, event, Qt.LeftButton, self.TempPoints)
                self.TempPoints = np.empty(0)  # очистить массив

        elif (self.functionAble == "Удалить вершину"):
            control.CDeletePoint(self.graph, event, Qt.LeftButton)

        elif (self.functionAble == "Переместить вершины"):
            self.FixedPoint = control.CIsCursorOnPoint(
                self.graph, event, Qt.LeftButton)

        elif (self.functionAble == "Добавить пунктирную связь"):
            self.FixedArrowPoint = control.CIsCursorOnArrowPoint(
                self.graph, event, Qt.LeftButton)  

            # !!! необходимо этот код перенсти в отдельную кнопку   
            if self.switch == True:
                self._drawLabels()
                self.switch = False
            # !!!

        self.update()

    def mouseMoveEvent(self, event):
        if (self.functionAble == "Переместить вершины"):
            control.CMovePointGrid(self.graph, event, Qt.LeftButton,
                                   self.FixedPoint, self.start_coordination_X, self.step, None)
                                   
        elif (self.functionAble == "Добавить пунктирную связь"):
            control.CMoveArrowPointGrid(
                self.graph, event, Qt.LeftButton, self.FixedArrowPoint, self.start_coordination_X, self.step)

        self.update()

class DrawHist(QWidget):
    def __init__(self, root, graph, start_coordination_X = 0, start_coordination_Y = 0, step = 25):
        super().__init__(root)
        self.step = step
        self.stepAlg = 75
        self.graph = graph
        self.lines = createGrid(start_coordination_X, start_coordination_Y, step, True, True)
        self.whiteLines = createGaps(start_coordination_X, start_coordination_Y, step)
        self.intervals = np.array([])
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 255, 90))
        painter.drawLines(self.lines)
        font_size = 12

        # отрисовка нумерации осей сетки
        painter.setPen(QColor("black"))
        x0 = 0
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        number_vertical_lines = (sizeWindow.width() - x0) // self.step + 1  # количество вертикальных линий
        y0 = sizeWindow.height()-170
        for i in range(number_vertical_lines):
            if len(str(i+1)) < 2:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
            else:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины
            painter.drawText(self.step + self.step * i + offset[0], y0 + offset[1], f'{i}')

        # отрисовка нумерации осей сетки
        x0 = 0
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        number_vertical_lines = (sizeWindow.width() - x0) // self.step + 1  # количество вертикальных линий
        y0 = sizeWindow.height()-170
        for i in range(number_vertical_lines):
            if len(str(i+1)) < 2:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
            else:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины
            painter.drawText(self.step + offset[0]-7, y0 - self.step * (i+1) - offset[1]/2, f'{i+1}')
        intervals = np.zeros(18)
        for p in range(len(self.graph)):
            AdjacencyMatrix = self.graph[p].GetNumberOfPeople()
            if AdjacencyMatrix is not None:
                for i in range(len(AdjacencyMatrix)):
                    for j in range(len(AdjacencyMatrix[i])):
                        if AdjacencyMatrix[i][j] != 0:
                            for k in range(len(intervals)):
                                #if k*self.step >= self.graph[p].Points[i][0] and self.graph[p].Points[j][0] >= (k+1)*self.step:
                                if k*self.stepAlg >= self.graph[p].Points[i][0] and self.graph[p].Points[j][0] >= (k+1)*self.stepAlg:
                                    intervals[k] += AdjacencyMatrix[i][j]
        # print(intervals)

        painter.setPen(QPen(QColor("red"), 3))
        lines = []
        for i in range(len(intervals)):
            lines.append(QLineF(0+self.step*(i+1), y0-intervals[i]*self.step - 10, self.step*(i+2), y0-intervals[i]*self.step - 10))
        painter.drawLines(lines)

        linesVert = []
        for i in range(1,len(intervals)):
            if intervals[i] != intervals[i-1]:
                linesVert.append(QLineF(0+self.step*(i+1), y0-intervals[i]*self.step- 10, 0+self.step*(i+1), y0-intervals[i-1]*self.step- 10))
        painter.drawLines(linesVert)
