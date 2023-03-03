import numpy as np

from PyQt5.QtCore import Qt, QRect, QPointF, QLineF, QSize
from PyQt5.QtGui import QPainter, QColor, QPolygonF, QPen, QFont, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QFileDialog

import controller
import checker
import properties

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
def createGrid(size, step=50, vertical=True, horizontal=True, max_time = -1):
    x0=0
    y0=0
    sizeWindow = size
    lines = []

    if vertical:
        if (max_time == -1):
            number_vertical_lines = (sizeWindow.width() - x0) // step + 1  # количество вертикальных линий
        else:
            number_vertical_lines = max_time + 1 + 3

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
def createGaps(size, step=50, sizeNumber = 40, yNumber = 50, max_time = -1):
    x0=0
    y0=0
    sizeWindow = size
    lines = []
    sizeNumber = sizeNumber / 2

    x0 = x0 + step

    if (max_time == -1):
        number_vertical_lines = (sizeWindow.width() - x0) // step + 1  # количество вертикальных линий
    else:
        number_vertical_lines = max_time +1 + 3
    for i in range(number_vertical_lines):
        lines.append(QLineF(x0, sizeWindow.height() - yNumber - sizeNumber, x0, sizeWindow.height() - yNumber + sizeNumber))
        x0 = x0 + step

    return lines


class Display(QWidget):
    FixedPoint = -1 # фиксированная вершина
    FixedArrowPoint = [-1, -1] # фиксированная стрелка
    def __init__(self, root, graph_in, step = 50, max_time = -1, horizontal = True, late_time = None, base_graph = None, switch = True):
        super().__init__(root)
        self.root = root
        self.functionAble = ""
        self.TempPoints = np.empty(0) # массив временно выделенных вершин
        self.colorGrid = QColor(0, 0, 255, 90)
        self.start_coordination_X = 0
        self.start_coordination_Y = 0
        self.step = step
        self.graph = graph_in
        self.late_time = late_time # поле определяющее как мы изображаем пунктирную стрелку, True - в поздних, False - в ранних, None - в зависимости от резерва времени
        self.horizontal = horizontal
        if (base_graph == None):
            self.base_graph = self.graph
        else:
            self.base_graph = base_graph

        self.graph_in = graph_in
        self.switch = switch
        self.illumination = -1  # подсветка кружков

        self.max_time = max_time
        self.QLineEdits = None

    def paintEvent(self, event):
        self.root.image.fill(Qt.white)
        if self.horizontal:

            self.lines = createGrid(self.size(), self.step, True, True, self.max_time)

        else:
            self.lines = createGrid(self.size(), self.step, True, False, self.max_time)
        self.whiteLines = createGaps(self.size(), self.step, self.max_time)

        for el in [self, self.root.image]:
            painter = QPainter(el)
            painter.setRenderHint(painter.Antialiasing) # убирает пикселизацию

            # отрисовка сетки
            painter.setPen(self.colorGrid)
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

                    painter.drawEllipse(int(self.graph.Points[i][0]-self.graph.RadiusPoint), int(self.graph.Points[i][1]-self.graph.RadiusPoint), 
                                        2*self.graph.RadiusPoint, 2*self.graph.RadiusPoint)
                    if len(str(i+1)) < 2:
                        offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
                    else:
                        offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины               
                    painter.drawText(int(self.graph.Points[i][0] + offset[0]), int(self.graph.Points[i][1] + offset[1]), f'{i}')
    
    def save(self):
        self.root.image.save('encrypted_data/1.jpg')

    def mousePressEvent(self, event):
        # нажатие на ЛКМ
        if (self.functionAble == "Добавить вершину"):
            controller.CAddPoint(self.graph, event, Qt.LeftButton)

        elif (self.functionAble == "Добавить связь"):
            self.TempPoints = np.append(self.TempPoints, self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # добавить в массив выбранных вершин
            self.illumination = self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())
            # если число выбранных вершин 2
            if len(self.TempPoints) == 2:
                # проверка, если пользователь случайно нажал дважды по одной и той же вершине
                if (self.TempPoints[0] != self.TempPoints[1]):
                    controller.CAddConnection(self.graph, event, Qt.LeftButton, self.TempPoints)

                self.TempPoints = np.empty(0) # очистить массив
                self.illumination = -1 #очистить  подсветку

        elif (self.functionAble == "Удалить связь"):
            self.TempPoints = np.append(self.TempPoints, self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # добавить в массив выбранных вершин
            self.illumination = self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())

            # если число выбранных вершин 2
            if len(self.TempPoints) == 2:
                controller.CDeleteConnection(self.graph, event, Qt.LeftButton, self.TempPoints)
                self.TempPoints = np.empty(0) # очистить массив
                self.illumination = -1 
    
        elif (self.functionAble == "Удалить вершину"):
            controller.CDeletePoint(self.graph, event, Qt.LeftButton)
            self.illumination = -1

        elif (self.functionAble == "Переместить вершины"):
            self.FixedPoint = controller.CIsCursorOnPoint(self.graph, event, Qt.LeftButton)
            self.illumination = -1
            self.TempPoints = np.empty(0)

        self.update()

    def mouseMoveEvent(self, event):
        if (self.functionAble == "Переместить вершины"):
            controller.CMovePoint(self.graph, event, Qt.LeftButton, self.FixedPoint)
        self.update()
        
    def checkEvent(self):
        mistakes = checker.checkTask1(self.graph, self.graph.CorrectAdjacencyMatrix)
        return mistakes

    def _drawQLineEdits(self):
        self.QLineEdits = np.zeros_like(self.graph.AdjacencyMatrix, dtype=QLineEdit)
        for i in range(len(self.graph.AdjacencyMatrix)):
            for j in range(len(self.graph.AdjacencyMatrix)):
                # если существует связь
                if (self.graph.AdjacencyMatrix[i][j] != 0 and 
                    (not np.isnan(self.graph.Points[i][0])) and
                    (not np.isnan(self.graph.Points[j][0]))):

                    # определим где отрисовать вес ребра/стрелки
                    offset = 25
                    x = ((int)(self.graph.Points[i][0]) + (int)(self.graph.Points[j][0])) / 2 - offset
                    y = ((int)(self.graph.Points[i][1]) + (int)(self.graph.Points[j][1])) / 2 - offset 

                    self.QLineEdits[i][j] = (QLineEdit(self))
                    self.QLineEdits[i][j].setAlignment(Qt.AlignHCenter)

                    font = 'Times'
                    font_size = 12
                    self.QLineEdits[i][j].setFont(QFont(font, font_size))
                    
                    self.QLineEdits[i][j].move(int(x), int(y))
                    self.QLineEdits[i][j].resize(50,50)

                    self.QLineEdits[i][j].setStyleSheet("border :2px solid black;")
                    
                    self.QLineEdits[i][j].setInputMask("00")
                    self.QLineEdits[i][j].show()

    def GetNumberOfPeople(self):
        if not(self.QLineEdits is None):
            self.PeopleWeights = np.zeros_like(self.QLineEdits, dtype=int)
            n = len(self.QLineEdits)
            for i in range(n):
                for j in range(n):
                    if (type(self.QLineEdits[i][j]) == QLineEdit):
                        try:
                            self.PeopleWeights[i][j] = int(self.QLineEdits[i][j].text())
                        except ValueError:
                            pass
            return self.PeopleWeights
        else:
            return None


class Display2(Display):
    def __init__(self, root, graph_in):
        super().__init__(root, graph_in)
        self.graph = graph_in
        self.switch = True
        self.illumination = -1
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
    
    def paintEvent(self, event):
        self.root.image.fill(Qt.white)
        if self.horizontal:
            self.lines = createGrid(self.size(), self.step, True, True, self.max_time)
        else:
            self.lines = createGrid(self.size(), self.step, True, False, self.max_time)
        self.whiteLines = createGaps(self.size(), self.step, self.max_time)

        for el in [self, self.root.image]:
            painter = QPainter(el)
            painter.setRenderHint(painter.Antialiasing) # убирает пикселизацию

            # отрисовка сетки
            painter.setPen(QColor(0, 0, 255, 90))
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
                    
                    painter.drawEllipse(int(x-radius/2), int(y-radius/2), int(radius), int(radius))

                    line_off = (radius/2) * np.cos(np.pi/4)

                    painter.drawLine(int(x-line_off), int(y-line_off), int(x+line_off), int(y+line_off))
                    painter.drawLine(int(x-line_off), int(y+line_off), int(x+line_off), int(y-line_off))
                    
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
                    painter.drawText(int(x-line_off+x_off/2), int(y+y_off), f'{t_p}')

                    x_off = -(5*len(str(t_n))*font_size/7.8 - 2.5) # по оси x определим смещение по длине строки
                    painter.drawText(int(x+line_off+1.5*x_off), int(y+y_off), f'{t_n}')

                    x_off = -(5*len(str(i+1))*font_size/7.8 - 2.5) # по оси x определим смещение по длине строки
                    painter.drawText(int(x+x_off), int(y-line_off+1.5*y_off), f'{i}')

                    x_off = -(5*len(str(R))*font_size/7.8 - 2.5)   # по оси x определим смещение по длине строки
                    painter.drawText(int(x+x_off), int(y+line_off+0.5*y_off), f'{R}')
            
            if self.switch:
                self._drawQLineEdits()
                self.switch = False

            self.graph.PeopleWeights = self.GetNumberOfPeople()

        self.update()
    def save(self):
        self.root.image.save('encrypted_data/2.jpg')
    def mousePressEvent(self, event):
        if (self.functionAble == "Критический путь"):
            self.TempPoints = np.append(self.TempPoints, self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # добавить в массив выбранных вершин
            self.illumination = self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())
            # если число выбранных вершин 2
            if len(self.TempPoints) == 2:
                # проверка, если пользователь случайно нажал дважды по одной и той же вершине
                if (self.TempPoints[0] != self.TempPoints[1]):
                    controller.CSelectCriticalPath(self.graph, event, Qt.LeftButton, self.TempPoints)
                self.TempPoints = np.empty(0) # очистить массив
                self.illumination = -1 
        self.update()
    def mouseMoveEvent(self, event):
        pass

    # проверка для второго задания
    def checkEvent(self):
        mistakes = checker.checkTask2(self.graph, self)
        return mistakes


class Display3_4(Display):
    # def __init__(self, root, graph_in, step = 50, max_time = -1, horizontal = True, late_time = None, switch = True, **kwargs):
    #     super().__init__(root, graph_in, step, max_time, horizontal, late_time, switch,**kwargs)
    #     # sizeWindow = QRect(QApplication.desktop().screenGeometry())
    #     # size = QSize(sizeWindow.height(), sizeWindow.height())
    #     # self.image = QImage(size, QImage.Format_RGB32)    

    def paintEvent(self, event):
        # self.image.size = self.size()
        self.root.image.fill(Qt.white)
        if self.horizontal:
            self.lines = createGrid(self.size(), self.step, True, True, self.max_time)
        else:
            self.lines = createGrid(self.size(), self.step, True, False, self.max_time)
        self.whiteLines = createGaps(self.size(), self.step, self.max_time)
        for el in [self, self.root.image]:
            painter = QPainter(el)
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
            sizeWindow = self.size()
            if (self.max_time == -1):
                number_vertical_lines = (sizeWindow.width() - x0) // self.step + 1  # количество вертикальных линий
            else:
                number_vertical_lines = self.max_time + 3
            y0 = sizeWindow.height() - 50 
            for i in range(number_vertical_lines):
                if len(str(i+1)) < 2:
                        offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
                else:
                        offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины
                painter.drawText(int(self.step + self.step * i + offset[0]), int(y0 + offset[1]), f'{i}')

            # отрисовка стрелок
            for i in range(len(self.graph.AdjacencyMatrix)):
                for j in range(len(self.graph.AdjacencyMatrix)):
                    # если существует связь
                    if (self.graph.AdjacencyMatrix[i][j] != 0 and
                       (not np.isnan(self.graph.Points[i][0])) and
                       (not np.isnan(self.graph.Points[j][0]))):
                        triangle_source = calculate_arrow_points(self.graph.Points[i], self.graph.ArrowPoints[i][j], 0)
                        if triangle_source is not None:
                            # выбор цвета в зависимости от выбора критического пути
                            if (self.graph.AdjacencyMatrix[i][j] == 2):
                                painter.setBrush(QColor("red"))
                                painter.setPen(QColor("red"))
                            elif (self.graph.AdjacencyMatrix[i][j] == 1):
                                painter.setBrush(QColor("black"))
                                painter.setPen(QColor("black"))
                            painter.drawPolygon(triangle_source)

                            pen = QPen()
                            if (self.graph.AdjacencyMatrix[i][j] == 2):
                                pen.setBrush(QColor("red"))
                                pen.setColor(QColor("red"))
                            elif (self.graph.AdjacencyMatrix[i][j] == 1):
                                pen.setBrush(QColor("black"))
                                pen.setColor(QColor("balck"))
                            painter.setPen(pen)
                            if (self.late_time == True):  # в поздних сроках
                                pen.setStyle(Qt.PenStyle.DashLine)
                                painter.setPen(pen)
                                painter.drawLine(QPointF(self.graph.Points[i][0], self.graph.Points[i][1]), triangle_source[1])
                                pen.setStyle(Qt.PenStyle.SolidLine)
                                painter.setPen(pen)
                                painter.drawLine(triangle_source[1], QPointF(self.graph.Points[j][0], self.graph.Points[j][1]))
                            else:  # в ранних сроках
                                pen.setStyle(Qt.PenStyle.SolidLine)
                                painter.setPen(pen)
                                painter.drawLine(QPointF(self.graph.Points[i][0], self.graph.Points[i][1]), triangle_source[1])
                                pen.setStyle(Qt.PenStyle.DashLine)
                                painter.setPen(pen)
                                painter.drawLine(triangle_source[1], QPointF(self.graph.Points[j][0], self.graph.Points[j][1]))
                                pen.setStyle(Qt.PenStyle.SolidLine)
                                painter.setPen(pen)

            # отрисовка вершин и цифр
            painter.setPen(QPen(QColor("black"), 2.5))

            for i in range(len(self.graph.Points)):
                # если вершина существует
                if (not np.isnan(self.graph.Points[i][0])):

                    if (i != self.illumination):
                        painter.setBrush(QColor("white"))# обеспечиваем закрашивание вершин графа
                    else:
                        painter.setBrush(QColor(127, 255, 212, 255))# обеспечиваем закрашивание вершин графа

                    
                    painter.drawEllipse(int(self.graph.Points[i][0]-self.graph.RadiusPoint), int(self.graph.Points[i][1]-self.graph.RadiusPoint), 
                                        int(2*self.graph.RadiusPoint), int(2*self.graph.RadiusPoint))
                    if len(str(i+1)) < 2:
                        offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
                    else:
                        offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины               
                    painter.drawText(int(self.graph.Points[i][0] + offset[0]), int(self.graph.Points[i][1] + offset[1]), f'{i}')

            self.graph_in.PeopleWeights = self.GetNumberOfPeople()

    def save(self,i):
        strTemp = str(i)+".jpg"
        self.root.image.save('encrypted_data/'+strTemp)

    def checkEvent3(self):
        mistakes = checker.checkTask3(self.graph, self.graph.CorrectWeights, self.start_coordination_X, self.step)
        return mistakes

    def checkEvent4(self):
        mistakes = checker.checkTask4(self.graph, self.graph.CorrectWeights, self.start_coordination_X, self.step)
        return mistakes

    def mousePressEvent(self, event):
        # нажатие на ЛКМ
        if (self.functionAble == "Добавить вершину"):
            controller.CAddPointGrid(
                self.graph, event, Qt.LeftButton, self.start_coordination_X, self.step, None)

        elif (self.functionAble == "Добавить связь"):
            self.TempPoints = np.append(self.TempPoints, self.graph.IsCursorOnPoint(
                event.pos().x(), event.pos().y()))  # добавить в массив выбранных вершин
            self.illumination = self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())

            # если число выбранных вершин 2
            if len(self.TempPoints) == 2:
                # проверка, если пользователь случайно нажал дважды по одной и той же вершине
                if (self.TempPoints[0] != self.TempPoints[1]):
                    controller.CAddConnection(
                        self.graph, event, Qt.LeftButton, self.TempPoints)
                self.TempPoints = np.empty(0)  # очистить массив
                self.illumination = -1 #очистить  подсветку

        elif (self.functionAble == "Удалить связь"):
            self.TempPoints = np.append(self.TempPoints, self.graph.IsCursorOnPoint(
                event.pos().x(), event.pos().y()))  # добавить в массив выбранных вершин
            self.illumination = self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())

            # если число выбранных вершин 2
            if len(self.TempPoints) == 2:
                controller.CDeleteConnection(
                    self.graph, event, Qt.LeftButton, self.TempPoints)
                self.TempPoints = np.empty(0)  # очистить массив
                self.illumination = -1 

        elif (self.functionAble == "Удалить вершину"):

            controller.CDeletePoint(self.graph, event, Qt.LeftButton)
            self.illumination = -1

        elif (self.functionAble == "Переместить вершины"):
            self.FixedPoint = controller.CIsCursorOnPoint(
                self.graph, event, Qt.LeftButton)
            self.illumination = -1
            self.TempPoints = np.empty(0)

        elif (self.functionAble == "Добавить пунктирную связь"):
            self.FixedArrowPoint = controller.CIsCursorOnArrowPoint(
                self.graph, event, Qt.LeftButton)  

        self.update()

    def mouseMoveEvent(self, event):
        if (self.functionAble == "Переместить вершины"):
            controller.CMovePointGrid(self.graph, event, Qt.LeftButton,
                                   self.FixedPoint, self.start_coordination_X, self.step, None)                               
        elif (self.functionAble == "Добавить пунктирную связь"):
            controller.CMoveArrowPointGrid(
                self.graph, event, Qt.LeftButton, self.FixedArrowPoint, self.start_coordination_X, self.step)

        self.update()


class Display5(Display):
    def __init__(self, root, graph_in, step = 50, max_time = -1, horizontal = True, **kwargs):
        super().__init__(root, graph_in, step, max_time, horizontal,**kwargs)
          
        self.i = self.root.i

    def paintEvent(self, event):
        self.root.images[self.i].fill(Qt.white)
        if self.horizontal:
            self.lines = createGrid(self.size(), self.step, True, True)
        else:
            self.lines = createGrid(self.size(), self.step, True, False)
        self.whiteLines = createGaps(self.size(), self.step)
        for el in [self, self.root.images[self.i]]:
            painter = QPainter(el)
            painter.setRenderHint(painter.Antialiasing) # убирает пикселизацию

            # отрисовка сетки
            painter.setPen(self.colorGrid)
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
            sizeWindow = self.size()
            number_vertical_lines = (sizeWindow.width() - x0) // self.step + 1  # количество вертикальных линий
            y0 = sizeWindow.height() - 50 
            for i in range(number_vertical_lines):
                if len(str(i+1)) < 2:
                        offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
                else:
                        offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины
                painter.drawText(int(self.step + self.step * i + offset[0]), int(y0 + offset[1]), f'{i}')

            # отрисовка стрелок
            for p1, p2 in self.graph.AdjacencyList.items():
                (x1, y1) = self.graph.Points[p1]
                (x2, y2) = self.graph.Points[p2]
                triangle_source = calculate_arrow_points((x1, y1), self.graph.Arrows[(p1, p2)], 0)
                if triangle_source is not None:
                    painter.drawPolygon(triangle_source)
                    if (self.late_time == None):  # в зависимости от резерва
                        if (len(self.base_graph.R) > p1[0]) and (self.base_graph.R[p1[0]] > 0):
                            painter.setPen(Qt.PenStyle.SolidLine)
                            painter.drawLine(QPointF(x1, y1), triangle_source[1])
                            painter.setPen(Qt.PenStyle.DashLine)
                            painter.drawLine(triangle_source[1], QPointF(x2, y2))
                            painter.setPen(Qt.PenStyle.SolidLine)
                        else:
                            painter.setPen(Qt.PenStyle.DashLine)
                            painter.drawLine(QPointF(x1, y1), triangle_source[1])
                            painter.setPen(Qt.PenStyle.SolidLine)
                            painter.drawLine(triangle_source[1], QPointF(x2, y2))
                    elif (self.late_time == True):  # в поздних сроках
                        painter.setPen(Qt.PenStyle.DashLine)
                        painter.drawLine(QPointF(x1, y1), triangle_source[1])
                        painter.setPen(Qt.PenStyle.SolidLine)
                        painter.drawLine(triangle_source[1], QPointF(x2, y2))
                    else:  # в ранних сроках
                        painter.setPen(Qt.PenStyle.SolidLine)
                        painter.drawLine(QPointF(x1, y1), triangle_source[1])
                        painter.setPen(Qt.PenStyle.DashLine)
                        painter.drawLine(triangle_source[1], QPointF(x2, y2))
                        painter.setPen(Qt.PenStyle.SolidLine)

            # отрисовка вершин и цифр
            painter.setPen(QPen(QColor("black"), 2.5))

            for (digit, id), (x, y) in self.graph.Points.items(): 
                painter.setBrush(QColor("white"))# обеспечиваем закрашивание вершин графа
                painter.drawEllipse(int(x-self.graph.Radius), int(y-self.graph.Radius), 
                                    int(2*self.graph.Radius), int(2*self.graph.Radius))
                if len(str(digit+1)) < 2:
                    offset = [-(5*len(str(digit+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
                else:
                    offset = [-(5*len(str(digit+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины               
                painter.drawText(int(x + offset[0]), int(y + offset[1]), f'{digit}')

        self.graph_in.PeopleWeights = self.GetNumberOfPeople()
            
    def mousePressEvent(self, event):
        # нажатие на ЛКМ
        if (self.functionAble == "Удалить последовательность"):
            if event.button() ==  Qt.LeftButton:
                p = self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())
                if p != None:
                    (x, y) = self.graph.Points[p]
                    self.graph.DeletePointsSequence(y)

        elif (self.functionAble == "Переместить вершины"):
            if event.button() == Qt.LeftButton:
                self.FixedPoint = self.graph.IsCursorOnPoint(event.pos().x(), event.pos().y())

        elif (self.functionAble == "Добавить пунктирную связь"):
            if event.button() == Qt.LeftButton:
                self.FixedArrowPoint = self.graph.IsCursorOnArrowPoint(event.pos().x(), event.pos().y()) 

        self.update()

    def mouseMoveEvent(self, event):
        if (self.functionAble == "Переместить вершины"):
            wasFinded = False
            i = 0
            while(not wasFinded):
                i += 1 
                if event.pos().x() <= self.start_coordination_X+i*self.step:
                    wasFinded = True

            XonGrid = self.start_coordination_X
            if (abs(event.pos().x() >= self.start_coordination_X+(i-3/2)*self.step) and 
                abs(event.pos().x() < self.start_coordination_X+(i-1/2)*self.step)):
                    XonGrid = self.start_coordination_X+(i-1)*self.step
            elif (abs(event.pos().x() >= self.start_coordination_X+(i-1/2)*self.step) and 
                  abs(event.pos().x() < self.start_coordination_X+(i+3/2)*self.step)):
                XonGrid = self.start_coordination_X+i*self.step
            
            if event.buttons() == Qt.LeftButton and self.FixedPoint != None:
                self.graph.MoveAllPointsFixedY(self.FixedPoint, XonGrid) 

        elif (self.functionAble == "Добавить пунктирную связь"):
            wasFinded = False 
            i = 0
            while(not wasFinded):
                i += 1 
                if event.pos().x() <= self.start_coordination_X+i*self.step:
                    wasFinded = True
             
            XonGrid = self.start_coordination_X
            if (abs(event.pos().x() >= self.start_coordination_X+(i-3/2)*self.step) and 
                abs(event.pos().x() < self.start_coordination_X+(i-1/2)*self.step)):
                XonGrid = self.start_coordination_X+(i-1)*self.step
            elif (abs(event.pos().x() >= self.start_coordination_X+(i-1/2)*self.step) and 
                  abs(event.pos().x() < self.start_coordination_X+(i+3/2)*self.step)):
                XonGrid = self.start_coordination_X+i*self.step

            if event.buttons() == Qt.LeftButton and self.FixedArrowPoint != None:
                self.graph.MoveArrowPointFixedY(self.FixedArrowPoint[0], self.FixedArrowPoint[1], XonGrid)

        self.update()

    def _drawQLineEdits(self):
        self.QLineEdits = dict()
        for p1, p2 in self.graph.AdjacencyList.items():
            (x1, y1) = self.graph.Points[p1]
            (x2, y2) = self.graph.Points[p2]

            # определим где отрисовать вес ребра/стрелки               
            offset = 25
            x = ((int)(x1) + (int)(x2)) / 2 - offset
            y = ((int)(y1) + (int)(y2)) / 2 - offset 

            self.QLineEdits[(p1, p2)] = (QLineEdit(self))
            self.QLineEdits[(p1, p2)].setAlignment(Qt.AlignHCenter)

            font = 'Times'
            font_size = 12
            self.QLineEdits[(p1, p2)].setFont(QFont(font, font_size))
            
            self.QLineEdits[(p1, p2)].move(int(x), int(y))
            self.QLineEdits[(p1, p2)].resize(50,50)

            self.QLineEdits[(p1, p2)].setStyleSheet("border :2px solid black;")
            
            self.QLineEdits[(p1, p2)].setInputMask("00")
            self.QLineEdits[(p1, p2)].show()

    def GetNumberOfPeople(self):
        if not(self.QLineEdits is None):
            self.PeopleWeights = dict()
            for k, v in self.QLineEdits.items():
                try:
                    self.PeopleWeights[k] = int(v.text())
                except ValueError:
                    pass
            return self.PeopleWeights
        else:
            return None

    def checkEvent5Part1(self, id) -> bool:
        return checker.checkTask5Part1(self.graph, self.base_graph, id)

    def checkEvent5Part2(self, id) -> bool:
        return checker.checkTask5Part2(self.graph, self.base_graph, self.base_graph.CorrectWeights, self.start_coordination_X, self.step, id)

    def checkEvent5Part3(self, id) -> bool:
        return checker.checkTask5Part3(self.base_graph, self.base_graph.SquadsPeopleToWork, self, id)


class Display6(Display5):
    def __init__(self, root, graph_in, step = 50, max_time = -1, horizontal = True, **kwargs):
        super().__init__(root, graph_in, step, max_time, horizontal,**kwargs)
          
        self.i = self.root.i

    def paintEvent(self, event):
        self.root.images[self.i].fill(Qt.white)
        if self.horizontal:
            self.lines = createGrid(self.size(), self.step, True, True)
        else:
            self.lines = createGrid(self.size(), self.step, True, False)
        self.whiteLines = createGaps(self.size(), self.step)
        for el in [self, self.root.images[self.i]]:
            painter = QPainter(el)
            painter.setRenderHint(painter.Antialiasing) # убирает пикселизацию

            # отрисовка сетки
            painter.setPen(self.colorGrid)
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
            sizeWindow = self.size()
            number_vertical_lines = (sizeWindow.width() - x0) // self.step + 1  # количество вертикальных линий
            y0 = sizeWindow.height() - 50 
            for i in range(number_vertical_lines):
                if len(str(i+1)) < 2:
                        offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
                else:
                        offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины
                painter.drawText(int(self.step + self.step * i + offset[0]), int(y0 + offset[1]), f'{i}')

            # отрисовка стрелок
            for p1, p2 in self.graph.AdjacencyList.items():
                (x1, y1) = self.graph.Points[p1]
                (x2, y2) = self.graph.Points[p2]
                triangle_source = calculate_arrow_points((x1, y1), self.graph.Arrows[(p1, p2)], 0)
                if triangle_source is not None:
                    painter.drawPolygon(triangle_source)

                    cos_sign = x2 - x1
                    sin_sign = y2 - y1
                    offset = 10
                    if ((cos_sign >= 0 and sin_sign >= 0) or (cos_sign <= 0 and sin_sign <= 0)):
                        x = ((int)(x1) + (int)(x2)) / 2 + offset
                    else:
                        x = ((int)(x1) + (int)(x2)) / 2 - offset
                    y = ((int)(y1) + (int)(y2)) / 2 - offset
                    painter.drawText(int(x), int(y), f'{self.graph.PeopleWeights[(p1, p2)]}')

                    if (self.late_time == None):  # в зависимости от резерва
                        if (len(self.base_graph.R) > i) and (self.base_graph.R[i] > 0):
                            painter.setPen(Qt.PenStyle.SolidLine)
                            painter.drawLine(QPointF(x1, y1), triangle_source[1])
                            painter.setPen(Qt.PenStyle.DashLine)
                            painter.drawLine(triangle_source[1], QPointF(x2, y2))
                            painter.setPen(Qt.PenStyle.SolidLine)
                        else:
                            painter.setPen(Qt.PenStyle.DashLine)
                            painter.drawLine(QPointF(x1, y1), triangle_source[1])
                            painter.setPen(Qt.PenStyle.SolidLine)
                            painter.drawLine(triangle_source[1], QPointF(x2, y2))
                    elif (self.late_time == True):  # в поздних сроках
                        painter.setPen(Qt.PenStyle.DashLine)
                        painter.drawLine(QPointF(x1, y1), triangle_source[1])
                        painter.setPen(Qt.PenStyle.SolidLine)
                        painter.drawLine(triangle_source[1], QPointF(x2, y2))
                    else:  # в ранних сроках
                        painter.setPen(Qt.PenStyle.SolidLine)
                        painter.drawLine(QPointF(x1, y1), triangle_source[1])
                        painter.setPen(Qt.PenStyle.DashLine)
                        painter.drawLine(triangle_source[1], QPointF(x2, y2))
                        painter.setPen(Qt.PenStyle.SolidLine)

            # отрисовка вершин и цифр
            painter.setPen(QPen(QColor("black"), 2.5))
            # отрисовка вершин и цифр
            painter.setPen(QPen(QColor("black"), 2.5))

            for (digit, id), (x, y) in self.graph.Points.items(): 
                painter.setBrush(QColor("white"))# обеспечиваем закрашивание вершин графа
                painter.drawEllipse(int(x-self.graph.Radius), int(y-self.graph.Radius), 
                                    int(2*self.graph.Radius), int(2*self.graph.Radius))
                if len(str(i+1)) < 2:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
                else:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины               
                painter.drawText(int(x + offset[0]), int(y + offset[1]), f'{digit}')
            self.root.widgetRight.update()
    

        for (digit, id), (x, y) in self.graph.Points.items(): 
            painter.setBrush(QColor("white"))# обеспечиваем закрашивание вершин графа
            painter.drawEllipse(int(x-self.graph.Radius), int(y-self.graph.Radius), 
                                int(2*self.graph.Radius), int(2*self.graph.Radius))
            if len(str(i+1)) < 2:
                offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
            else:
                offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины               
            painter.drawText(int(x + offset[0]), int(y + offset[1]), f'{digit}')

class DrawHist(QWidget):
    def __init__(self, root, graph, step = 25):

        super().__init__()
        self.root = root
        self.step = step
        self.stepAlg = 100
        self.graph = graph
        self.intervals = np.array([])
        self.firstShow = True
    
    def paintEvent(self, event):
        if self.firstShow:
            self.image_hist = QImage(self.size(), QImage.Format_RGB32)
            self.firstShow = False
        self.image_hist.fill(Qt.white)
        for el in [self, self.image_hist]:
            self.lines = createGrid(self.size(), self.step, True, True, )
            self.whiteLines = createGaps(self.size(), self.step)
            painter = QPainter(el)
            painter.setPen(QColor(0, 0, 255, 90))
            painter.drawLines(self.lines)
            font_size = 12

            # отрисовка нумерации осей сетки
            painter.setPen(QColor("black"))
            x0 = self.step
            sizeWindow = QRect(QApplication.desktop().screenGeometry())
            number_vertical_lines = (self.size().width() - x0) // self.step + 1  # количество вертикальных линий
            y0 = 42*self.step
            for i in range(number_vertical_lines):
                if len(str(i+1)) < 2:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
                else:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины
                painter.drawText(int(x0 + self.step + self.step * i + offset[0]), int(-self.step/2+y0 + offset[1]), f'{i}')

            # отрисовка нумерации осей сетки
            #x0 = 0
            sizeWindow = QRect(QApplication.desktop().screenGeometry())
            #number_vertical_lines = (self.size().height() - y0) // self.step + 1  # количество вертикальных линий
            #y0 = sizeWindow.height()-195
            print(number_vertical_lines)
            for i in range(number_vertical_lines):
                if len(str(i+1)) < 2:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 3), 5*font_size/8] # определим смещение по длине строки номера вершины
                else:
                    offset = [-(5*len(str(i+1))*font_size/7.8 - 2.5 - 5), 5*font_size/8] # определим смещение по длине строки номера вершины
                painter.drawText(int(x0 + self.step + offset[0]-7), int(self.step/3+y0 - self.step * (i+1) - offset[1]/2), f'{i}')
            # подпись осей
            font = painter.font()
            font.setPixelSize(20)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(int(self.size().width()/2), int(self.size().height()-10), "Время")
            
            painter.translate(20, int(self.size().height()/2))
            painter.rotate(-90)
            painter.drawText(0,0, "Кол-во людей")
            
            painter.rotate(90)
            painter.translate(-20, -int(self.size().height()/2))

            intervals = np.zeros(self.root.max_possible_time+1)
            for p in range(len(self.graph)):
                AdjacencyList = self.graph[p].PeopleWeights
                ArrowsList = self.graph[p].Arrows
                #print(ArrowsList)
                if AdjacencyList is not None:
                    for (p1, p2), w in AdjacencyList.items():
                        (x1, y1) = self.graph[p].Points[p1]
                        (x2, y2) = self.graph[p].Points[p2]
                        (ax,ay) = ArrowsList[p1,p2]
                        for k in range(len(intervals)):
                            if k*self.stepAlg >= x1 and x2 >= (k+1)*self.stepAlg:
                                if ax <= k*self.stepAlg or ax == 140+(k-1)*self.stepAlg:
                                    intervals[k-1] += w
            y0 = y0 -self.step
            painter.setPen(QPen(QColor("red"), 3))
            lines = []
            for i in range(len(intervals)-1):
                lines.append(QLineF(x0+self.step*(i+1), y0-intervals[i]*self.step, x0 + self.step*(i+2), y0-intervals[i]*self.step))
            painter.drawLines(lines)

            linesVert = []
            for i in range(1,len(intervals)):
                if intervals[i] != intervals[i-1]:
                    linesVert.append(QLineF(x0+self.step*(i+1), y0-intervals[i]*self.step, x0+self.step*(i+1), y0-intervals[i-1]*self.step))
            painter.drawLines(linesVert)

    def save(self):
        self.image_hist.save('encrypted_data/6_hist.jpg')