import sys, math
import numpy as np

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QDockWidget, QVBoxLayout, QGridLayout, QAction, QPushButton, QMessageBox
from PyQt5.QtGui import QPainter, QImage, QColor, QCursor, QPolygonF
from PyQt5.QtCore import Qt, QRect, QPointF



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

# функции для определения точек пересечения отрезков
def onSegment(p, q, r):
    if ( (q.x() <= max(p.x(), r.x())) and (q.x() >= min(p.x(), r.x())) and
           (q.y() <= max(p.y(), r.y())) and (q.y() >= min(p.y(), r.y()))):
        return True
    return False
 
def orientation(p, q, r):
    val = (float(q.y() - p.y()) * (r.x() - q.x())) - (float(q.x() - p.x()) * (r.y() - q.y()))
    if (val > 0):
        return 1
    elif (val < 0):
        return 2
    else:
        return 0
 
def doIntersect(p1,q1,p2,q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
 
    if ((o1 != o2) and (o3 != o4)):
        return True
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True
    return False

# функция для опредения координат точки пересечения 
# и проверки на то ,что точка пересечения не является лишь вершиной графа
def find_point_and_check(p1,q1,p2,q2):
    if (q1.y() - p1.y() != 0): 
        q = (q1.x() - p1.x()) / (p1.y() - q1.y());   
        sn = (p2.x() - q2.x()) + (p2.y() - q2.y()) * q 
        if (not sn): 
            return False 
        fn = (p2.x() - p1.x()) + (p2.y() - p1.y()) * q 
        n = fn / sn
    else:
        if (not(p2.y() - q2.y())): 
            return False 
        n = (p2.y() - p1.y()) / (p2.y() - q2.y()) 
    dot = (p2.x() + (q2.x() - p2.x()) * n, p2.y() + (q2.y() - p2.y()) * n ) # точка пересечения
    if (dot[0] != p1.x() and dot[0] != q1.x() and dot[0] != p2.x() and dot[0] != q2.x() and
        dot[1] != p1.y() and dot[1] != q1.y() and dot[1] != p2.y() and dot[1] != q2.y()):
        return True



# класс, реализующий виджет 'Справка'
class Instructions(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.label_1 = QLabel("Инструкция: ")
        self.label_2 = QLabel("1. Добавить вершину - нажмите СКМ* в любом месте поля")
        self.label_3 = QLabel("2. Соединить вершины - нажать ПКМ* по двум вершинам")
        self.label_4 = QLabel("3. Переместить вершину - удерживайте ЛКМ* любую созданную вершину")
        self.label_5 = QLabel("4. Удалить вершину - наведите курсор мыши на удаляемую вершину и нажмите delete на клавиатуре")
        self.label_6 = QLabel("")
        self.label_7 = QLabel("*ЛКМ - левая кнопка мыши")
        self.label_8 = QLabel("*ПКМ - правая кнопка мыши")
        self.label_9 = QLabel("*СКМ - средняя кнопка мыши")

        self.button = QPushButton("Проверить")

        self.grid = QGridLayout()

        self.grid.addWidget(self.label_1)
        self.grid.addWidget(self.label_2)
        self.grid.addWidget(self.label_3)
        self.grid.addWidget(self.label_4)
        self.grid.addWidget(self.label_5)
        self.grid.addWidget(self.label_6)
        self.grid.addWidget(self.label_7)
        self.grid.addWidget(self.label_8)
        self.grid.addWidget(self.label_9)
        self.grid.addWidget(self.button)


        self.stretchLout = QVBoxLayout()
        self.stretchLout.addStretch()
        self.grid.addLayout(self.stretchLout, 10, 0)
        self.setLayout(self.grid)

    

# класс, реализующий виджет для создания графа
class Display(QWidget):

    def __init__(self):
        super().__init__()

        self.grabKeyboard() # захват нажатий на клавиатуре
        self.initUI()

    def initUI(self):
        self.cntPoints = 0 # число вершин в графе
        self.r = 30 # радиус вершины
        self.points = np.array(object = [], dtype = list) # массив координат центров вершин графа
        self.marked = np.array(object = [], dtype = int) # массив индексов связанных вершин

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))

        # как только были отмечены для соединения две вершины, начинаем отрисовывать ребра
        if (len(self.marked) >= 2):
            painter.setPen(QColor(0, 0, 0))
            painter.setPen(Qt.PenStyle.SolidLine) # тут можно использовать Qt.PenStyle.DashLine для пунктирных линий
            # проходимся по массиву с шагом 2 и соединяем отмеченные вершины
            # тут берутся актуальные координаты из массива points
            for i in range(0, len(self.marked), 2):
                # проверка на случай, если число отмеченных вершин нечетное
                # а именно, чтобы индекс текущей парной вершины была в массиве
                if (i + 1 < len(self.marked) and (self.points[self.marked[i]][1] == True and self.points[self.marked[i+1]][1])):
                    arrowhead_polygon = calculate_arrow_points(self.points[self.marked[i]][0], 
                                                               self.points[self.marked[i+1]][0])

                    if arrowhead_polygon is not None:
                        painter.setBrush(QColor(0, 0, 0))
                        painter.drawPolygon(arrowhead_polygon)
                        painter.setPen(QColor(0, 0, 0))
                        painter.setPen(Qt.PenStyle.SolidLine)

                    painter.drawLine((int)(self.points[self.marked[i]][0].x()),
                                 (int)(self.points[self.marked[i]][0].y()),
                                 (int)(self.points[self.marked[i+1]][0].x()),
                                 (int)(self.points[self.marked[i+1]][0].y()))            

        # обеспечиваем закрашивание вершин графа
        painter.setBrush(QColor(0, 0, 0))

        # отрисовываем вершины и цифры
        offset = QPointF(-2.5, 5)
        for i in range(self.cntPoints):
            if (self.points[i][1] == True):
                painter.drawEllipse(self.points[i][0], self.r, self.r)
                painter.setPen(QColor("white"))
                painter.drawText(self.points[i][0] + offset, f'{i}')
                painter.setPen(QColor(0, 0, 0))

    def keyPressEvent(self, event):
        cursor = QCursor()
        sensitivity = 80
        for i in range(self.cntPoints):
            if ((event.key() == Qt.Key_Delete) and 
                (cursor.pos().x() >= self.points[i][0].x() - sensitivity and cursor.pos().x() <= self.points[i][0].x() + sensitivity and
                 cursor.pos().y() >= self.points[i][0].y() - sensitivity and cursor.pos().y() <= self.points[i][0].y() + sensitivity)):
                self.points[i][1] = False
                index = []
                for j in range(0, len(self.marked), 2):
                    if (j + 1 < len(self.marked) and (self.marked[j] == i or self.marked[j+1] == i)):
                        index.append([j, j+1])
       
                self.marked = np.delete(self.marked, index)
                break

        self.update()

    def mousePressEvent(self, event):
        # нажатие на СКМ собавляет новую вершину
        add = True
        if (event.button() == Qt.MiddleButton):
            for i in range(len(self.points)): 
                if self.points[i][1] == False:
                    self.points[i][0] = event.pos()
                    self.points[i][1] = True
                    add = False
                    break
            if (add):
                self.points = np.append(self.points, QPointF)
                self.points[self.cntPoints] = [event.pos(), True]
                self.cntPoints += 1

        # смотрим на все вершины и проверяем не нажали ли на них ПКМ
        # если да, то добавляем в marked
        # окно чувствительности rxr
        for i in range(self.cntPoints):
            if ((event.button() == Qt.RightButton) and 
                (event.pos().x() >= self.points[i][0].x() - self.r and event.pos().x() <= self.points[i][0].x() + self.r and
                 event.pos().y() >= self.points[i][0].y() - self.r and event.pos().y() <= self.points[i][0].y() + self.r)):
                self.marked = np.append(self.marked, i)
                break

        self.update()

    def mouseMoveEvent(self, event):
        # смотрим на все вершины и проверяем не двигают ли их
        # если да, то добавляем новые координаты в points
        # окно чувствительности rxr
        for i in range(self.cntPoints):
            if (event.pos().x() >= self.points[i][0].x() - self.r and event.pos().x() <= self.points[i][0].x() + self.r and
                event.pos().y() >= self.points[i][0].y() - self.r and event.pos().y() <= self.points[i][0].y() + self.r):
                self.points[i][0] = event.pos()
                break

        self.update()

    def check(self, Points, ConnectedPoints):
        # параметры, которые должны быть получены из вариантов
        correct_number_of_nodes = 10
        correct_connections = [ (0, 1),
                                (0, 2),
                                (0, 3),
                                (1, 2), 
                                (1, 4), 
                                (2, 5), 
                                (2, 7), 
                                (3, 4), 
                                (3, 6), 
                                (4, 5),
                                (4, 6), 
                                (5, 7),
                                (5, 8),
                                (6, 8),
                                (7, 9), 
                                (8, 9) ]

        msg = QMessageBox()
        cnt = 0
        do_intersect = False
        error_string = ""
        correct = True
        no_warnings = True
        for i in range(self.cntPoints):
            # считаем число точек 
            if (Points[i][1] == True):
                cnt += 1
            # и заодно проверяем не находятся ли точки слишком близко
            for j in range(self.cntPoints):
                if ((not do_intersect) and j != i and (Points[j][0].x() + self.r >= Points[i][0].x() - self.r and 
                                                       Points[j][0].x() - self.r <= Points[i][0].x() + self.r and
                                                       Points[j][0].y() + self.r >= Points[i][0].y() - self.r and 
                                                       Points[j][0].y() - self.r <= Points[i][0].y() + self.r)):
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Внимание!")
                    msg.setInformativeText("Некоторые вершины находятся слишком близко друг к другу.")
                    msg.setWindowTitle("Результат")
                    msg.exec_()
                    no_warnings = False
                    do_intersect = True # нужно, чтобы остановить вывод других warning-ов
                    break

        if (cnt != correct_number_of_nodes):
            error_string += "Неверное число вершин.\n"
            correct = False

        # считаем число связей
        cnt = len(correct_connections)
        if (len(ConnectedPoints) % 2 == 0):
            cur_cnt = len(ConnectedPoints)/2
        else:
            cur_cnt = (len(ConnectedPoints) - 1)/2

        if cnt != cur_cnt:
            error_string += "Неверное число связей.\n"
            correct = False

        for i in range(0, len(ConnectedPoints), 2):
            if (i + 1 < len(ConnectedPoints) and (Points[ConnectedPoints[i]][1] == True and Points[ConnectedPoints[i+1]][1])):
                if (ConnectedPoints[i], ConnectedPoints[i+1]) in correct_connections:
                    cnt -= 1
      
        if (cnt != 0):
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка!")
            error_string += "Неверные связи.\n"
            correct = False
            msg.setInformativeText(error_string)
            msg.setWindowTitle("Результат")
            msg.exec_()

        # в случае если все проверки были пройдены, проверим на пересечение рёбер
        if (correct and no_warnings):
            do_intersect = False
            for i in correct_connections:
                for j in correct_connections:
                    p1 = QPointF(self.points[i[0]][0].x(), self.points[i[0]][0].y())
                    q1 = QPointF(self.points[i[1]][0].x(), self.points[i[1]][0].y())
                    p2 = QPointF(self.points[j[0]][0].x(), self.points[j[0]][0].y())
                    q2 = QPointF(self.points[j[1]][0].x(), self.points[j[1]][0].y())  
                    if ((not do_intersect) and (j != i) and doIntersect(p1, q1, p2, q2) and find_point_and_check(p1, q1, p2, q2)):
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("Внимание!")
                        msg.setInformativeText("Граф построен верно, но рёбра не должны пересекаться.")
                        msg.setWindowTitle("Результат")
                        msg.exec_()
                        do_intersect = True
                        correct = False
                        no_warnings = False
                        break
                if(do_intersect):
                    break

        if (correct and no_warnings):
            msg.setIcon(QMessageBox.Information)
            msg.setText("Отлично!")
            msg.setInformativeText("Всё верно.")
            msg.setWindowTitle("Результат")
            msg.exec_()
        
        

# класс, реализующий окно приложения
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.move(0, 0)

        # узнаем ширину и высоту монитора
        rec = QRect(QApplication.desktop().screenGeometry())
        height = rec.height()
        width = rec.width()

        # вписываем во весь экран
        self.resize(width, height)
        
        # другой вариант
        # self.showFullScreen()

        self.setWindowTitle('Редактор графов')

        manual = Instructions()
        manual.button.clicked.connect(self.call_check)
        dock = QDockWidget("Справка")
        dock.setWidget(manual)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

        self.display = Display()
        self.setCentralWidget(self.display)

        exitAction = QAction('Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Закрыть приложение')
        exitAction.triggered.connect(self.close)

        panelAction = dock.toggleViewAction()
        panelAction.setStatusTip('Справка')
        panelAction.setShortcut('Ctrl+I')
        panelAction.setStatusTip('Открыть меню справки')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Файл')
        fileMenu.addAction(panelAction)
        fileMenu.addAction(exitAction)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.show()

    def call_check(self):
        self.display.check(self.display.points, self.display.marked)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())