import sys, math
import numpy as np

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QDockWidget, QVBoxLayout, QGridLayout, QAction
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


        self.stretchLout = QVBoxLayout()
        self.stretchLout.addStretch()
        self.grid.addLayout(self.stretchLout, 9, 0)
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
        dock = QDockWidget("Справка")
        dock.setWidget(manual)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

        display = Display()
        self.setCentralWidget(display)

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



if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())