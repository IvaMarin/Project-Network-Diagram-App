import sys
import numpy as np

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QDockWidget, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPainter, QImage, QColor
from PyQt5.QtCore import Qt, QRect, QPointF



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
        self.label_5 = QLabel("")
        self.label_6 = QLabel("*ЛКМ - левая кнопка мыши")
        self.label_7 = QLabel("*ПКМ - правая кнопка мыши")
        self.label_8 = QLabel("*СКМ - средняя кнопка мыши")

        self.grid = QGridLayout()

        self.grid.addWidget(self.label_1)
        self.grid.addWidget(self.label_2)
        self.grid.addWidget(self.label_3)
        self.grid.addWidget(self.label_4)
        self.grid.addWidget(self.label_5)
        self.grid.addWidget(self.label_6)
        self.grid.addWidget(self.label_7)
        self.grid.addWidget(self.label_8)


        self.stretchLout = QVBoxLayout()
        self.stretchLout.addStretch()
        self.grid.addLayout(self.stretchLout, 8, 0)
        self.setLayout(self.grid)



# класс, реализующий виджет для создания графа
class Display(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        

    def initUI(self):
        self.cntPoints = 0 # число вершин в графе
        self.r = 30 # радиус вершины
        self.points = np.array(object = [], dtype = QPointF) # массив координат центров вершин графа
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
                if (i + 1 < len(self.marked)):
                    painter.drawLine((int)(self.points[self.marked[i]].x()),
                                 (int)(self.points[self.marked[i]].y()),
                                 (int)(self.points[self.marked[i+1]].x()),
                                 (int)(self.points[self.marked[i+1]].y()))
            

        # обеспечиваем закрашивание вершин графа
        painter.setBrush(QColor(0, 0, 0))

        # отрисовываем вершины и цифры
        for i in range(self.cntPoints):
            painter.drawEllipse(self.points[i], self.r, self.r)
            painter.setPen(QColor("white"))
            painter.drawText(self.points[i] + QPointF(-2.5, 5), f'{i}') # '+ QPointF(-2.5, 5)' нужно, чтобы цифры немного сдвинуть
            painter.setPen(QColor(0, 0, 0))


    def mousePressEvent(self, event):
        # нажатие на СКМ собавляет новую вершину
        if (event.button() == Qt.MiddleButton):
            self.points = np.append(self.points, QPointF)
            self.points[self.cntPoints] = event.pos()
            self.cntPoints += 1

        # смотрим на все вершины и проверяем не нажали ли на них ПКМ
        # если да, то добавляем в marked
        # окно чувствительности 20x20
        for i in range(self.cntPoints):
            if ((event.button() == Qt.RightButton) and 
                (event.pos().x() >= self.points[i].x() - 20 and event.pos().x() <= self.points[i].x() + 20 and
                 event.pos().y() >= self.points[i].y() - 20 and event.pos().y() <= self.points[i].y() + 20)):
                self.marked = np.append(self.marked, i)
                break
  
        self.update()


    def mouseMoveEvent(self, event):
        # смотрим на все вершины и проверяем не двигают ли их
        # если да, то добавляем новые координаты в points
        # окно чувствительности 20x20
        for i in range(self.cntPoints):
            if (event.pos().x() >= self.points[i].x() - 20 and event.pos().x() <= self.points[i].x() + 20 and
                event.pos().y() >= self.points[i].y() - 20 and event.pos().y() <= self.points[i].y() + 20):
                self.points[i] = event.pos()
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


        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.show()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())