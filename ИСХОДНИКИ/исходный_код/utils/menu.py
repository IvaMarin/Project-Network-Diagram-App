from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import *
from utils.report.report_generator import *
from utils.figure import Figure
from message_box_creator import message_box_create
from math import exp
import datetime
import json
import basedir_paths as bp
import time



class Tasks(QtWidgets.QWidget):
    def __init__(self, personal_data, variant_number: str, parent):
        super(QtWidgets.QWidget, self).__init__()
        self.timer_start = time.perf_counter()
        self.timer_result = 0
        self.start_time = datetime.datetime.now().time().isoformat()[:8]
        self.cur_figure = None
        self.diff_center = (0, 0)
        self.personal_data = personal_data
        self.answer_status = [False for i in range(7)]
        self.variant = variant_number
        self.parent = parent
        self.current_page = 8
        self.setWindowTitle("задание")
        self.setGeometry(0, 0, 900, 800)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(200, 35, 700, 700)
        self.label.setStyleSheet('border-style: solid; border-width: 5px; border-color: black;')
        # self.task_img = QtGui.QPixmap(f"variants/variant{variant_number}/variant{variant_number}.jpg")
        self.task_img = QtGui.QPixmap()
        try:
            self.task_img.loadFromData(
                decrypt_file(bp.join(bp.encrypted_data_path, f"variant{variant_number}"),
                             f"variant{variant_number}.jpg"), "jpg")
        except FileNotFoundError:
            pass
        self.label.setPixmap(self.task_img)
        self.label.setScaledContents(True)

        font = QtGui.QFont()
        font.setPointSize(15)

        font_for_tytle = QtGui.QFont()
        font_for_tytle.setPointSize(20)

        self.teachers_hint = QtWidgets.QPushButton(self)
        self.teachers_hint.setGeometry(1050, 560, 130, 50)
        self.teachers_hint.setText("Подсказка")
        self.teachers_hint.setFont(font)
        self.teachers_hint.setStyleSheet("background-color: rgb(224, 234, 255);")
        if self.parent.mode == "student":
            self.teachers_hint.hide()

        self.task_button = QtWidgets.QPushButton(self)
        self.task_button.setGeometry(1050, 20, 130, 50)
        self.task_button.setText("Задание")
        self.task_button.setFont(font)
        self.task_button.setStyleSheet("background-color: rgb(110, 160, 250);")

        self.point1_button = QtWidgets.QPushButton(self)
        self.point1_button.setGeometry(1050, 80, 130, 50)
        self.point1_button.setText("Пункт 1")
        self.point1_button.setFont(font)
        self.point1_button.setStyleSheet("background-color: rgb(224, 234, 255);")

        self.point2_button = QtWidgets.QPushButton(self)
        self.point2_button.setGeometry(1050, 140, 130, 50)
        self.point2_button.setText("Пункт 2")
        self.point2_button.setFont(font)
        self.point2_button.setStyleSheet("background-color: rgb(224, 234, 255);")

        self.point3_button = QtWidgets.QPushButton(self)
        self.point3_button.setGeometry(1050, 200, 130, 50)
        self.point3_button.setText("Пункт 3")
        self.point3_button.setFont(font)
        self.point3_button.setStyleSheet("background-color: rgb(224, 234, 255);")

        self.point4_button = QtWidgets.QPushButton(self)
        self.point4_button.setGeometry(1050, 260, 130, 50)
        self.point4_button.setText("Пункт 4")
        self.point4_button.setFont(font)
        self.point4_button.setStyleSheet("background-color: rgb(224, 234, 255);")

        self.point5_button = QtWidgets.QPushButton(self)
        self.point5_button.setGeometry(1050, 320, 130, 50)
        self.point5_button.setText("Пункт 5")
        self.point5_button.setFont(font)
        self.point5_button.setStyleSheet("background-color: rgb(224, 234, 255);")

        self.point6_button = QtWidgets.QPushButton(self)
        self.point6_button.setGeometry(1050, 380, 130, 50)
        self.point6_button.setText("Пункт 6")
        self.point6_button.setFont(font)
        self.point6_button.setStyleSheet("background-color: rgb(224, 234, 255);")

        self.point7_button = QtWidgets.QPushButton(self)
        self.point7_button.setGeometry(1050, 440, 130, 50)
        self.point7_button.setText("Пункт 7")
        self.point7_button.setFont(font)
        self.point7_button.setStyleSheet("background-color: rgb(224, 234, 255);")

        self.check_button = QtWidgets.QPushButton(self)
        self.check_button.setGeometry(1050, 500, 130, 50)
        self.check_button.setText("Проверить")
        self.check_button.setFont(font)
        self.check_button.setStyleSheet("background-color: rgb(224, 234, 255);")
        self.check_button.hide()

        self.end_button = QtWidgets.QPushButton(self)
        self.end_button.setGeometry(1050, 680, 130, 50)
        self.end_button.setText("Завершить")
        self.end_button.setFont(font)
        self.end_button.setStyleSheet("background-color: rgb(224, 234, 255);")
        self.list_of_trying = [0 for i in range(7)]
        self.point0 = []
        self.point1 = []
        self.point2 = []
        self.point3 = []
        self.point4 = []
        self.point5 = []
        self.point6 = []
        self.point7 = []
        # point 0
        self.point0.append(self.label)
        # point 1
        self.paint_label = QtWidgets.QLabel(self)
        self.paint_label.setGeometry(30, 150, 1000, 600)
        canvas = QtGui.QPixmap(self.paint_label.size())
        canvas.fill(Qt.GlobalColor.white)
        self.canvas = canvas
        self.paint_label.setPixmap(canvas)
        self.paint_label.hide()
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.GlobalColor.black
        self.lastPoint = QPoint()
        self.draw_mode = "moving"
        self.figure_is_selected = False
        self.paint_label.mousePressEvent = self.mouse_press_event
        self.paint_label.mouseMoveEvent = self.mouse_move_event
        self.paint_label.mouseReleaseEvent = self.mouse_release_event
        self.prev_object = (0, 0)
        self.point1.append(self.paint_label)
        self.figure_array: [Figure] = []
        self.add_figure_button = QtWidgets.QPushButton(self)
        self.add_figure_button.setGeometry(250, 100, 150, 40)
        self.add_figure_button.setText("Добавить")
        self.add_figure_button.setFont(font)
        self.add_figure_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.add_figure_button.hide()
        self.add_figure_button.clicked.connect(self.add_figure)
        self.point1.append(self.add_figure_button)

        self.disconnect_figure = QtWidgets.QPushButton(self)
        self.disconnect_figure.setGeometry(730, 100, 150, 40)
        self.disconnect_figure.setText("Разъединить")
        self.disconnect_figure.setFont(font)
        self.disconnect_figure.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.disconnect_figure.hide()
        self.disconnect_figure.clicked.connect(self.disconnecting_figure)
        self.point1.append(self.disconnect_figure)

        self.delete_figure_button = QtWidgets.QPushButton(self)
        self.delete_figure_button.setGeometry(410, 100, 150, 40)
        self.delete_figure_button.setText("Удалить")
        self.delete_figure_button.setFont(font)
        self.delete_figure_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.delete_figure_button.hide()
        self.delete_figure_button.clicked.connect(self.delete_figure)
        self.point1.append(self.delete_figure_button)

        self.connect_figure = QtWidgets.QPushButton(self)
        self.connect_figure.setGeometry(570, 100, 150, 40)
        self.connect_figure.setText("Соединить")
        self.connect_figure.setFont(font)
        self.connect_figure.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.connect_figure.hide()
        self.connect_figure.clicked.connect(self.connecting_figure)
        self.point1.append(self.connect_figure)


        # self.draw_mode2_button = QtWidgets.QPushButton(self)
        # self.draw_mode2_button.setGeometry(400, 100, 70, 40)
        # self.draw_mode2_button.setText("/")
        # self.draw_mode2_button.setFont(font)
        # self.draw_mode2_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        # self.draw_mode2_button.hide()
        # self.draw_mode2_button.clicked.connect(lambda: self.change_draw_mode(2))
        # self.point1.append(self.draw_mode2_button)
        #
        # self.draw_mode3_button = QtWidgets.QPushButton(self)
        # self.draw_mode3_button.setGeometry(320, 100, 70, 40)
        # self.draw_mode3_button.setFont(font)
        # self.draw_mode3_button.setStyleSheet("background-image : url(utils/eraser.png);")
        # self.draw_mode3_button.hide()
        # self.draw_mode3_button.clicked.connect(lambda: self.change_draw_mode(3))
        # self.point1.append(self.draw_mode3_button)

        self.point1_label1 = QtWidgets.QLabel(self)
        self.point1_label1.setGeometry(200, 0, 800, 100)
        self.point1_label1.setFont(font_for_tytle)
        self.point1_label1.setText("Анализ функционирования системы и разработка\n      структурной схемы надежности (ССН)")
        self.point1_label1.setStyleSheet("color: white;")
        self.point1_label1.hide()
        self.point1.append(self.point1_label1)

        # point 2
        self.point2_label1 = QtWidgets.QLabel(self)
        self.point2_label1.setGeometry(200, 0, 800, 100)
        self.point2_label1.setFont(font_for_tytle)
        self.point2_label1.setText("Определение выражения для расчета вероятности\n              безотказной работы (ВБР) системы")
        self.point2_label1.setStyleSheet("color: white")
        self.point2_label1.hide()
        self.point2.append(self.point2_label1)

        self.point2_input = QtWidgets.QLineEdit(self)
        self.point2_input.setGeometry(100, 155, 930, 50)
        self.point2_input.setFont(font)
        self.point2_input.setStyleSheet("background-color: rgb(224, 234, 255);")
        self.point2_input.hide()
        self.point2.append(self.point2_input)

        self.point2_label2 = QtWidgets.QLabel(self)
        self.point2_label2.setGeometry(10, 155, 80, 50)
        self.point2_label2.setText("P(t)=")
        self.point2_label2.setStyleSheet("color: white")
        self.point2_label2.setFont(font_for_tytle)
        self.point2_label2.hide()
        self.point2.append(self.point2_label2)

        # point 3
        self.point3_label1 = QtWidgets.QLabel(self)
        self.point3_label1.setGeometry(200, 0, 800, 100)
        self.point3_label1.setFont(font_for_tytle)
        self.point3_label1.setText("Расчет показателей безотказности системы")
        self.point3_label1.setStyleSheet("color: white")
        self.point3_label1.hide()
        self.point3.append(self.point3_label1)

        self.point3_label2 = QtWidgets.QLabel(self)
        self.point3_label2.setGeometry(110, 105, 180, 50)
        self.point3_label2.setText("Т ср=")
        self.point3_label2.setStyleSheet("color: white")
        self.point3_label2.setFont(font_for_tytle)
        self.point3_label2.hide()
        self.point3.append(self.point3_label2)

        self.point3_input2 = QtWidgets.QLineEdit(self)
        self.point3_input2.setGeometry(200, 105, 600, 50)
        self.point3_input2.setFont(font_for_tytle)
        self.point3_input2.setStyleSheet("background-color: rgb(224, 234, 255);")
        self.point3_input2.hide()
        self.point3.append(self.point3_input2)

        self.point3_label3 = QtWidgets.QLabel(self)
        self.point3_label3.setGeometry(130, 205, 180, 50)
        self.point3_label3.setText("λ=")
        self.point3_label3.setStyleSheet("color: white")
        self.point3_label3.setFont(font_for_tytle)
        self.point3_label3.hide()
        self.point3.append(self.point3_label3)

        self.point3_input3 = QtWidgets.QLineEdit(self)
        self.point3_input3.setGeometry(200, 205, 600, 50)
        self.point3_input3.setFont(font_for_tytle)
        self.point3_input3.setStyleSheet("background-color: rgb(224, 234, 255);")
        self.point3_input3.hide()
        self.point3.append(self.point3_input3)

        self.point3_label4 = QtWidgets.QLabel(self)
        self.point3_label4.setGeometry(130, 305, 180, 50)
        self.point3_label4.setText("Λ=")
        self.point3_label4.setStyleSheet("color: white")
        self.point3_label4.setFont(font_for_tytle)
        self.point3_label4.hide()
        self.point3.append(self.point3_label4)

        self.point3_input4 = QtWidgets.QLineEdit(self)
        self.point3_input4.setGeometry(200, 305, 600, 50)
        self.point3_input4.setFont(font_for_tytle)
        self.point3_input4.setStyleSheet("background-color: rgb(224, 234, 255);")
        self.point3_input4.hide()
        self.point3.append(self.point3_input4)

        self.point3_label5 = QtWidgets.QLabel(self)
        self.point3_label5.setGeometry(110, 405, 80, 50)
        self.point3_label5.setText("T o=")
        self.point3_label5.setStyleSheet("color: white")
        self.point3_label5.setFont(font_for_tytle)
        self.point3_label5.hide()
        self.point3.append(self.point3_label5)

        self.point3_input5 = QtWidgets.QLineEdit(self)
        self.point3_input5.setGeometry(200, 405, 600, 50)
        self.point3_input5.setFont(font_for_tytle)
        self.point3_input5.setStyleSheet("background-color: rgb(224, 234, 255);")
        self.point3_input5.hide()
        self.point3.append(self.point3_input5)

        # point 4
        self.point4_label1 = QtWidgets.QLabel(self)
        self.point4_label1.setGeometry(200, 0, 800, 100)
        self.point4_label1.setFont(font_for_tytle)
        self.point4_label1.setText("Расчет ВБР системы за наработку t = 500 ч")
        self.point4_label1.setStyleSheet("color: white")
        self.point4_label1.hide()
        self.point4.append(self.point4_label1)

        self.point4_label2 = QtWidgets.QLabel(self)
        self.point4_label2.setGeometry(70, 105, 180, 50)
        self.point4_label2.setText("P(t=500ч) =")
        self.point4_label2.setStyleSheet("color: white")
        self.point4_label2.setFont(font_for_tytle)
        self.point4_label2.hide()
        self.point4.append(self.point4_label2)

        self.point4_input1 = QtWidgets.QLineEdit(self)
        self.point4_input1.setGeometry(260, 105, 550, 50)
        self.point4_input1.setFont(font_for_tytle)
        self.point4_input1.setStyleSheet("background-color: rgb(224, 234, 255);")
        self.point4_input1.hide()
        self.point4.append(self.point4_input1)

        # point5
        self.point5_label1 = QtWidgets.QLabel(self)
        self.point5_label1.setGeometry(200, 0, 800, 100)
        self.point5_label1.setFont(font_for_tytle)
        self.point5_label1.setText("Расчет 90 - процентной наработки до отказа")
        self.point5_label1.setStyleSheet("color: white")
        self.point5_label1.hide()
        self.point5.append(self.point5_label1)

        self.point5_label2 = QtWidgets.QLabel(self)
        self.point5_label2.setGeometry(70, 105, 180, 50)
        self.point5_label2.setText("t(γ=90%) =")
        self.point5_label2.setStyleSheet("color: white")
        self.point5_label2.setFont(font_for_tytle)
        self.point5_label2.hide()
        self.point5.append(self.point5_label2)

        self.point5_input1 = QtWidgets.QLineEdit(self)
        self.point5_input1.setGeometry(260, 105, 550, 50)
        self.point5_input1.setFont(font_for_tytle)
        self.point5_input1.setStyleSheet("background-color: rgb(224, 234, 255);")
        self.point5_input1.hide()
        self.point5.append(self.point5_input1)

        # point6
        self.point6_label1 = QtWidgets.QLabel(self)
        self.point6_label1.setGeometry(200, 0, 800, 100)
        self.point6_label1.setFont(font_for_tytle)
        self.point6_label1.setText("Расчет среднего времени восстановления системы")
        self.point6_label1.setStyleSheet("color: white")
        self.point6_label1.hide()
        self.point6.append(self.point6_label1)

        self.point6_label2 = QtWidgets.QLabel(self)
        self.point6_label2.setGeometry(40, 105, 198, 50)
        self.point6_label2.setText("T вост сист =")
        self.point6_label2.setStyleSheet("color: white")
        font15 = QtGui.QFont()
        font15.setPointSize(14)
        self.point6_label2.setFont(font_for_tytle)
        self.point6_label2.hide()
        self.point6.append(self.point6_label2)

        self.point6_input1 = QtWidgets.QLineEdit(self)
        self.point6_input1.setGeometry(260, 105, 550, 50)
        self.point6_input1.setFont(font_for_tytle)
        self.point6_input1.setStyleSheet("background-color: rgb(224, 234, 255);")
        self.point6_input1.hide()
        self.point6.append(self.point6_input1)

        # point7
        self.point7_label1 = QtWidgets.QLabel(self)
        self.point7_label1.setGeometry(200, 0, 800, 100)
        self.point7_label1.setFont(font_for_tytle)
        self.point7_label1.setText("Расчет коэффициента готовности системы")
        self.point7_label1.setStyleSheet("color: white")
        self.point7_label1.hide()
        self.point7.append(self.point7_label1)

        self.point7_label2 = QtWidgets.QLabel(self)
        self.point7_label2.setGeometry(170, 105, 130, 50)
        self.point7_label2.setText("К г =")
        self.point7_label2.setStyleSheet("color: white")
        self.point7_label2.setFont(font_for_tytle)
        self.point7_label2.hide()
        self.point7.append(self.point7_label2)

        self.point7_input1 = QtWidgets.QLineEdit(self)
        self.point7_input1.setGeometry(260, 105, 550, 50)
        self.point7_input1.setFont(font_for_tytle)
        self.point7_input1.setStyleSheet("background-color: rgb(224, 234, 255);")
        self.point7_input1.hide()
        self.point7.append(self.point7_input1)

        self.add_button_func()

    def change_draw_mode(self):
        self.draw_mode = 1 if self.draw_mode == 0 else 0

    def clear_paint_label(self):
        self.paint_label.pixmap().fill(Qt.GlobalColor.white)

        self.update()

    def mouse_release_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.draw_mode == "moving":
            self.cur_figure = None
            self.drawing = False

    def mouse_press_event(self, event):
        painter = QtGui.QPainter(self.paint_label.pixmap())
        painter.setPen(QtGui.QPen(self.brushColor, self.brushSize))
        font = QtGui.QFont()
        font.setPointSize(17)
        painter.setFont(font)
        # if left mouse button is pressed
        if event.button() == Qt.MouseButton.LeftButton and self.draw_mode == "moving":
            # make drawing flag true
            # make last point to the point of cursor
            self.lastPoint = event.pos()
            cur_vertex = (self.lastPoint.x(), self.lastPoint.y())
            print("debug1", self.drawing)
            self.cur_figure = self.find_figure(cur_vertex)
            if self.cur_figure is None:
                return
            else:
                print(f"find figure {self.cur_figure.number}")
                self.diff_center = (
                cur_vertex[0] - self.cur_figure.vertex[0], cur_vertex[1] - self.cur_figure.vertex[1])
                self.drawing = True
        elif event.button() == Qt.MouseButton.LeftButton and self.draw_mode == "connecting":
            if not self.figure_is_selected:
                self.lastPoint = event.pos()
                cur_vertex = (self.lastPoint.x(), self.lastPoint.y())
                print("debug connect1")
                self.cur_figure = self.find_figure(cur_vertex)
                if self.cur_figure is not None:
                    self.figure_is_selected = True
            else:
                print("debug connect2")
                self.lastPoint = event.pos()
                cur_vertex = (self.lastPoint.x(), self.lastPoint.y())
                print("debug1", self.drawing)
                second_figure = self.find_figure(cur_vertex)
                if second_figure is None:
                    return
                self.figure_is_selected = False
                if second_figure.number > self.cur_figure.number:
                    second_figure.add_link(self.cur_figure)
                else:
                    self.cur_figure.add_link(second_figure)
                for figure in self.figure_array:
                    figure.draw_links(painter)
                for figure in self.figure_array:
                    figure.draw_figure(painter)
                self.update()
        elif event.button() == Qt.MouseButton.LeftButton and self.draw_mode == "disconnecting":
            if not self.figure_is_selected:
                self.lastPoint = event.pos()
                cur_vertex = (self.lastPoint.x(), self.lastPoint.y())
                print("debug connect1")
                self.cur_figure = self.find_figure(cur_vertex)
                if self.cur_figure is not None:
                    self.figure_is_selected = True
            else:
                print("debug connect2")
                self.lastPoint = event.pos()
                cur_vertex = (self.lastPoint.x(), self.lastPoint.y())
                second_figure = self.find_figure(cur_vertex)
                if second_figure is None:
                    return
                self.figure_is_selected = False
                if second_figure.number > self.cur_figure.number:
                    second_figure.remove_link(self.cur_figure)
                else:
                    self.cur_figure.remove_link(second_figure)
                self.clear_paint_label()
                for figure in self.figure_array:
                    figure.draw_links(painter)
                for figure in self.figure_array:
                    figure.draw_figure(painter)
                self.update()

    def mouse_move_event(self, event):
        if (
                event.buttons() and Qt.MouseButton.LeftButton) and self.drawing and self.cur_figure is not None and self.draw_mode == "moving":
            painter = QtGui.QPainter(self.paint_label.pixmap())
            painter.setPen(QtGui.QPen(self.brushColor, self.brushSize))
            font = QtGui.QFont()
            font.setPointSize(17)
            painter.setFont(font)
            cur_vertex = (event.pos().x() - self.diff_center[0], event.pos().y() - self.diff_center[1])
            print("debug2", cur_vertex)
            self.cur_figure.vertex = cur_vertex
            self.clear_paint_label()
            for figure in self.figure_array:
                figure.draw_links(painter)
            for figure in self.figure_array:
                figure.draw_figure(painter)
            self.update()

    def add_button_func(self):
        self.point1_button.clicked.connect(lambda: self.set_point('1'))
        self.point2_button.clicked.connect(lambda: self.set_point('2'))
        self.point3_button.clicked.connect(lambda: self.set_point('3'))
        self.point4_button.clicked.connect(lambda: self.set_point('4'))
        self.point5_button.clicked.connect(lambda: self.set_point('5'))
        self.point6_button.clicked.connect(lambda: self.set_point('6'))
        self.point7_button.clicked.connect(lambda: self.set_point('7'))
        self.task_button.clicked.connect(lambda: self.set_point('task'))
        self.check_button.clicked.connect(lambda: self.check_answer(self.current_page))
        self.end_button.clicked.connect(self.end)
        self.teachers_hint.clicked.connect(lambda: self.call_hint(self.current_page))

    def check_answer(self, page_number):
        try:
            answer_content = decrypt_file(bp.join(bp.encrypted_data_path, f"variant{self.variant}", "programm"),
                                          "answer.json").decode()
            if answer_content == "ERROR_DECRYPT":
                message_box_create("Ошибка недоработанного варианта", "Решение для данного варианта повреждены в базе",
                                   QMessageBox.Information)
                return
            json_data = json.loads(answer_content)
            # with open(f"variants/variant{self.variant}/programm/answer.json") as f:
            #     json_data = json.load(f)
        except FileNotFoundError:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка недоработанного варианта")
            msg.setText("Решения для данного варианта отсутствует в базе")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            return
        except json.decoder.JSONDecodeError:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка недоработанного варианта")
            msg.setText("Решения для данного варианта повреждены в базе")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            return
        self.list_of_trying[page_number - 1] += 1
        if page_number == 1:
            links = self.get_all_links()
            if links == json_data["point1"]:
                self.answer_status[page_number - 1] = True
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен верно.")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
            else:
                self.answer_status[page_number - 1] = False
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен не верно!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
        elif page_number == 2:
            t = 100
            try:
                for i, val in enumerate(json_data["lambda"], 1):
                    exec(f"l{i}={val}")
            except Exception:
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText("Лямбы не заданы в ответах программы, нужно их задать")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                return

            student_answer = self.point2_input.text()
            real_answer = json_data["point2"]
            try:
                real_answer = real_answer.replace("^", "**")
                real_answer = eval(real_answer)
            except Exception:
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText("Выражение написано неправильно в ответах программы")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                return
            try:
                student_answer = student_answer.replace("^", "**")
                student_answer = eval(student_answer)
            except Exception:
                msg = QMessageBox()
                msg.setWindowTitle("Выражение написано неправильно")
                msg.setText("Выражение написано неправильно, посмотрите как нужно его писать в инструкции")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                return

            if abs(student_answer - real_answer) < 1e-3:
                self.answer_status[page_number - 1] = True
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен верно.")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
            else:
                self.answer_status[page_number - 1] = False
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен не верно!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
        elif page_number == 3:
            try:
                student_answer = [float(self.point3_input2.text()), float(self.point3_input3.text()),
                                  float(self.point3_input4.text()), float(self.point3_input5.text())]
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("Пустые поля")
                msg.setText("Введите все числа")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.list_of_trying[page_number - 1] -= 1
                return
            check_list = [abs(i[0] - i[1]) <= 1e-5 for i in zip(student_answer, json_data["point3"])]
            if all(check_list):
                self.answer_status[page_number - 1] = True
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен верно.")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
            else:
                self.answer_status[page_number - 1] = False
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен не верно!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
        elif page_number == 4:
            try:
                student_answer = float(self.point4_input1.text())
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("Пустые поля")
                msg.setText("Введите все числа")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.list_of_trying[page_number - 1] -= 1
                return
            if (student_answer - json_data["point4"]) <= 1e-5:
                self.answer_status[page_number - 1] = True
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен верно.")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
            else:
                self.answer_status[page_number - 1] = False
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен не верно!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
        elif page_number == 5:
            try:
                student_answer = float(self.point5_input1.text())
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("Пустые поля")
                msg.setText("Введите все числа")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.list_of_trying[page_number - 1] -= 1
                return
            if abs(student_answer - json_data["point5"]) <= 1e-3:
                self.answer_status[page_number - 1] = True
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен верно.")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
            else:
                self.answer_status[page_number - 1] = False
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен не верно!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
        elif page_number == 6:
            try:
                student_answer = float(self.point6_input1.text())
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("Пустые поля")
                msg.setText("Введите все числа")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.list_of_trying[page_number - 1] -= 1
                return
            if abs(student_answer - json_data["point6"]) <= 1e-3:
                self.answer_status[page_number - 1] = True
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен верно.")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
            else:
                self.answer_status[page_number - 1] = False
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен не верно!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
        elif page_number == 7:
            try:
                student_answer = float(self.point7_input1.text())
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("Пустые поля")
                msg.setText("Введите все числа")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.list_of_trying[page_number - 1] -= 1
                return
            if (student_answer - json_data["point7"]) <= 1e-5:
                self.answer_status[page_number - 1] = True
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен верно.")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
            else:
                self.answer_status[page_number - 1] = False
                msg = QMessageBox()
                msg.setWindowTitle("Проверка")
                msg.setText("Пункт решен не верно!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()

    def call_hint(self, page_number):
        if page_number == 8:
            return
        self.hint = QtWidgets.QWidget()
        self.hint.resize(1000, 500)
        label = QtWidgets.QLabel(self.hint)
        label.setGeometry(0, 0, 1000, 500)
        pixmap = QtGui.QPixmap()
        try:
            pixmap.loadFromData(decrypt_file(bp.join(bp.encrypted_data_path, f"variant{self.variant}", "solve"),
                                             f"task{page_number}.jpg"), "jpg")
            label.setPixmap(pixmap)
            self.hint.setWindowTitle(f"решение варианта {self.variant} пункт {page_number}")
        except Exception:
            self.hint.setWindowTitle(f"отсутствует решение варианта {self.variant} пункт {page_number}")
        self.hint.show()

    def clear_page(self):
        points = self.point0 + self.point1 + self.point2 + self.point3 + self.point4 + self.point5 + self.point6 + self.point7
        for elem in points:
            elem.hide()

    def set_point(self, page: str):
        if page != str(self.current_page) and not self.parent.check_key(self.parent.key_path):
            self.parent.change_mode("student")

        if page != "task":
            self.check_button.show()
        else:
            self.check_button.hide()

        if page == "task":
            self.current_page = 8
            self.clear_page()
            self.label.show()
        elif page == "1":
            self.current_page = 1
            self.clear_page()
            for elem in self.point1:
                elem.show()
        elif page == "2":
            self.current_page = 2
            self.clear_page()
            for elem in self.point2:
                elem.show()
        elif page == "3":
            self.current_page = 3
            self.clear_page()
            for elem in self.point3:
                elem.show()
        elif page == "4":
            self.current_page = 4
            self.clear_page()
            for elem in self.point4:
                elem.show()
        elif page == "5":
            self.current_page = 5
            self.clear_page()
            for elem in self.point5:
                elem.show()
        elif page == "6":
            self.current_page = 6
            self.clear_page()
            for elem in self.point6:
                elem.show()
        elif page == "7":
            self.current_page = 7
            self.clear_page()
            for elem in self.point7:
                elem.show()
        self.repainting_points(page)

    def repainting_points(self, new_point: str):
        new_point = 8 if new_point == 'task' else int(new_point)
        all_point = [self.point1_button, self.point2_button, self.point3_button, self.point4_button,
                     self.point5_button, self.point6_button, self.point7_button, self.task_button]
        for point in all_point:
            point.setStyleSheet("background-color: rgb(224, 234, 255);")
        all_point[new_point - 1].setStyleSheet("background-color: rgb(110, 160, 250);")

    def save_report(self):
        start_summary_second = int(self.start_time[0:2]) * 3600 + int(self.start_time[3:5]) * 60 + \
                               int(self.start_time[3:5])
        end_summary_second = int(self.end_time[0:2]) * 3600 + int(self.end_time[3:5]) * 60 + int(self.end_time[3:5])
        diff_second = end_summary_second - start_summary_second
        if abs(diff_second - self.timer_result) <= 120:
            scam = ''
        else:
            scam = 'студент изменил время системы и пытается обмануть'
        # img_path = "tmp/tmp_img.jpg"
        # img1 = self.paint_label.pixmap().save("tmp/tmp_img.jpg")
        report_output_path = (
            bp.join(bp.reports_path,
                    f"{self.personal_data['group']}_{'_'.join(self.personal_data['name'].split())}.txt")
        )
        template_context = TemplateContext(bp.report_template_docx_path, report_output_path)
        template_context_elements = []
        template_context_elements.append(TemplateContextElement("fioStudent", self.personal_data['name']))
        template_context_elements.append(TemplateContextElement("group", self.personal_data['group']))
        template_context_elements.append(
            TemplateContextElement("date", '.'.join(reversed(str(datetime.date.today()).split('-')))))
        template_context_elements.append(TemplateContextElement("variant", str(self.variant)))
        template_context_elements.append(TemplateContextElement("scam", scam))
        template_context_elements.append(TemplateContextElement("start_time", self.start_time))
        template_context_elements.append(TemplateContextElement("end_time", self.end_time))
        template_context_elements.append(TemplateContextElement("timer", self.timer_result))

        tmp_task_img_path = bp.join(bp.tmp_path, "task_img.jpg")
        try:
            with open(tmp_task_img_path, "wb") as fd:
                content = decrypt_file(bp.join(bp.encrypted_data_path, f"variant{self.variant}"),
                                       f"variant{self.variant}.jpg")
                if content == b"ERROR_DECRYPT":
                    message_box_create("Сохранение отчёта", "Повреждены данные программы", QMessageBox.Information)
                    return
                fd.write(content)
        except Exception:
            message_box_create("Сохранение отчёта", "Повреждены данные программы", QMessageBox.Information)
            return
        template_context_elements.append(TemplateContextElement("task", tmp_task_img_path, True, 200, 150))
        # template_context_elements.append(TemplateContextElement("task", f"variants/variant{self.variant}/variant{self.variant}.jpg", True))

        answer1_img_path = bp.join(bp.tmp_path, "answer1_img.jpg")
        self.paint_label.pixmap().save(answer1_img_path)
        template_context_elements.append(TemplateContextElement("answer1", answer1_img_path, True))

        template_context_elements.append(TemplateContextElement("answer2", self.point2_input.text()))

        template_context_elements.append(TemplateContextElement("answer31", self.point3_input2.text()))
        template_context_elements.append(TemplateContextElement("answer32", self.point3_input3.text()))
        template_context_elements.append(TemplateContextElement("answer33", self.point3_input4.text()))
        template_context_elements.append(TemplateContextElement("answer34", self.point3_input5.text()))

        template_context_elements.append(TemplateContextElement("answer4", self.point4_input1.text()))

        template_context_elements.append(TemplateContextElement("answer5", self.point5_input1.text()))

        template_context_elements.append(TemplateContextElement("answer6", self.point6_input1.text()))

        template_context_elements.append(TemplateContextElement("answer7", self.point7_input1.text()))

        template_context_elements.append(TemplateContextElement("try1", str(self.list_of_trying[0])))
        template_context_elements.append(TemplateContextElement("try2", str(self.list_of_trying[1])))
        template_context_elements.append(TemplateContextElement("try3", str(self.list_of_trying[2])))
        template_context_elements.append(TemplateContextElement("try4", str(self.list_of_trying[3])))
        template_context_elements.append(TemplateContextElement("try5", str(self.list_of_trying[4])))
        template_context_elements.append(TemplateContextElement("try6", str(self.list_of_trying[5])))
        template_context_elements.append(TemplateContextElement("try7", str(self.list_of_trying[6])))

        template_context.fill_parameters(template_context_elements)
        template_context.generate_report()

        os.remove(tmp_task_img_path)
        os.remove(answer1_img_path)

    def end(self):
        if not all(self.answer_status) and self.parent.mode != "teacher":
            msg = QMessageBox()
            msg.setWindowTitle("Завершение работы")
            msg.setText("Не все пункты решены верно")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            return
        msg = QMessageBox(self)
        msg.setWindowTitle("Завершение работы")
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы действительно хотите завершить работу ?")
        buttonAceptar = msg.addButton("Да, хочу", QMessageBox.YesRole)
        buttonCancelar = msg.addButton("Отменить", QMessageBox.RejectRole)
        msg.setDefaultButton(buttonAceptar)
        msg.exec_()

        if msg.clickedButton() == buttonAceptar:
            self.timer_result = time.perf_counter() - self.timer_start
            self.end_time = datetime.datetime.now().time().isoformat()[:8]
            self.save_report()
            end_msg = QMessageBox()
            end_msg.setWindowTitle("Отчёт сохранён")
            end_msg.setText(
                f"Отчёт сохранён как {self.personal_data['group']}_{'_'.join(self.personal_data['name'].split())}")
            end_msg.setIcon(QMessageBox.Information)
            end_msg.exec_()
            self.parent.change_mode("student")
            self.parent.main_widget = QtWidgets.QWidget()
            uic.loadUi(bp.main_widget_path, self.parent.main_widget)
            self.parent.main_widget.label.setStyleSheet(f"background-image:url({bp.main_label_image});")
            self.parent.main_widget.start_button.clicked.connect(self.parent.start)
            self.parent.setCentralWidget(self.parent.main_widget)
        elif msg.clickedButton() == buttonCancelar:
            pass
        print("end of task")

    def add_figure(self):
        painter = QtGui.QPainter(self.paint_label.pixmap())
        painter.setPen(QtGui.QPen(self.brushColor, self.brushSize))
        font = QtGui.QFont()
        font.setPointSize(17)
        painter.setFont(font)
        self.figure_array.append(Figure((30, 30), 50, 50, len(self.figure_array) + 1))
        self.figure_array[-1].draw_figure(painter)
        self.update()

    def delete_figure(self):
        print("delete figure")

        if len(self.figure_array) == 0:
            return

        self.clear_paint_label()
        del self.figure_array[-1]
        painter = QtGui.QPainter(self.paint_label.pixmap())
        painter.setPen(QtGui.QPen(self.brushColor, self.brushSize))
        font = QtGui.QFont()
        font.setPointSize(17)
        painter.setFont(font)
        for figure in self.figure_array:
            figure.draw_links(painter)
        for figure in self.figure_array:
            figure.draw_figure(painter)

    def connecting_figure(self):
        self.disconnect_figure.setStyleSheet("background-color: rgb(255, 255, 255);")
        if self.draw_mode == "moving" or self.draw_mode == "disconnecting":
            self.figure_is_selected = False
            self.draw_mode = "connecting"
            self.connect_figure.setStyleSheet("background-color: rgb(110, 160, 250);")
            self.paint_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        elif self.draw_mode == "connecting":
            self.cur_figure = None
            self.drawing = False
            self.paint_label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.draw_mode = "moving"
            self.connect_figure.setStyleSheet("background-color: rgb(255, 255, 255);")

    def disconnecting_figure(self):
        self.connect_figure.setStyleSheet("background-color: rgb(255, 255, 255);")
        if self.draw_mode == "moving" or self.draw_mode == "connecting":
            self.figure_is_selected = False
            self.draw_mode = "disconnecting"
            self.disconnect_figure.setStyleSheet("background-color: rgb(110, 160, 250);")
            self.paint_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        elif self.draw_mode == "disconnecting":
            self.cur_figure = None
            self.drawing = False
            self.paint_label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.draw_mode = "moving"
            self.disconnect_figure.setStyleSheet("background-color: rgb(255, 255, 255);")

    def find_figure(self, vertex: tuple):
        for figure in self.figure_array:
            left = figure.vertex[0]
            rigth = left + figure.w
            top = figure.vertex[1]
            bottom = top + figure.h
            if left <= vertex[0] <= rigth and top <= vertex[1] <= bottom:
                return figure
        return None

    def get_all_links(self):
        links = {}
        for figure in self.figure_array:
            links[str(figure.number)] = set()
        for figure in self.figure_array:
            for link_figure_number in figure.links.keys():
                links[str(link_figure_number)].add(figure.number)
                links[str(figure.number)].add(link_figure_number)
        for figure in self.figure_array:
            links[str(figure.number)] = sorted(list(links[str(figure.number)]))
        return links
