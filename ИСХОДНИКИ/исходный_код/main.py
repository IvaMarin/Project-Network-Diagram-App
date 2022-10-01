from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from utils.calculator import Ui_calculator
from utils.info import Ui_program_info
from utils.notepad import NotepadWidget
from PyQt5.QtWidgets import QMessageBox
from utils.menu import Tasks
from utils.help import HelpWidget
from utils.first_launch.first_launch_widget import show_first_launch_widget
from utils.encrypt.encrypt_module import decrypt_file
from docx2pdf import convert
from utils.report.pdf_widget import PdfWidget
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from pathlib import Path
from message_box_creator import message_box_create

import sys
import os
import oschmod
import win32event
import win32comext.shell.shell as shell
import basedir_paths as bp


def variant_is_exist(variant: str):
    variants = [name[7:] for name in os.listdir("encrypted_data")]
    return variant in variants


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi(bp.main_window_path, self)
        self.setStyleSheet(f"#MainWindow{{background-image:url({bp.background_image_path});"
                           "background-size: cover;}"
                           "#menubar{background-color: rgb(126, 167, 255)}")
        self.key_path = None
        self.mode = "student"
        self.action_delete_report.setVisible(False)
        self.action_save_as_docx.setVisible(False)
        self.action_save_as_pdf.setVisible(False)
        self.menu_save_as.menuAction().setVisible(False)
        self.action_import_report.setVisible(False)
        self.addMenuBar()

        self.setWindowTitle("Расчёт показателей надёжности")
        self.setWindowIcon(QtGui.QIcon(bp.join(bp.images_path, "vuc.ico")))
        self.pdf_widget = None

        try:
            if not os.path.exists(bp.encrypted_data_path):
                os.mkdir(bp.encrypted_data_path)
            for dir_path, dir_name, filenames in os.walk(bp.encrypted_data_path):
                for filename in filenames:
                    tmp_path = bp.join(dir_path, filename)
                    oschmod.set_mode(tmp_path, 0o666)
            if not os.path.exists(bp.reports_path):
                os.mkdir(bp.reports_path)
            for dir_path, dir_name, filenames in os.walk(bp.reports_path):
                for filename in filenames:
                    tmp_path = bp.join(dir_path, filename)
                    oschmod.set_mode(tmp_path, 0o666)
            if not os.path.exists(bp.tmp_path):
                os.mkdir(bp.tmp_path)
            for dir_path, dir_name, filenames in os.walk(bp.tmp_path):
                for filename in filenames:
                    tmp_path = bp.join(dir_path, filename)
                    oschmod.set_mode(tmp_path, 0o666)
        except Exception:
            pass

        try:
            is_first_launch = self.is_first_launch()
            self.main_widget = QtWidgets.QWidget()
            uic.loadUi(bp.main_widget_path, self.main_widget)
            self.main_widget.label.setStyleSheet(f"background-image:url({bp.main_label_image});")
            self.main_widget.setObjectName("menu_widget")
            self.main_widget.start_button.clicked.connect(self.start)
            if is_first_launch:
                show_first_launch_widget(self, self.main_widget)
            else:
                self.setCentralWidget(self.main_widget)
        except Exception as e:
            print(str(e))


    def addMenuBar(self):
        self.action_report_print.triggered.connect(self.print_report)
        self.action_save_report.triggered.connect(self.save_report)
        self.action_import_report.triggered.connect(self.import_report)
        self.action_watch_report.triggered.connect(self.watch_report)
        self.action_delete_report.triggered.connect(self.delete_report)
        self.action_save_as_docx.triggered.connect(self.save_report_as_docx)
        self.action_save_as_pdf.triggered.connect(self.save_report_as_pdf)
        self.call_calc.triggered.connect(self.calling_calc)
        self.about_developers.triggered.connect(self.calling_info)
        self.call_notepad.triggered.connect(self.calling_notepad)
        self.teacher.triggered.connect(self.enter_key)
        self.student.triggered.connect(lambda: self.change_mode("student"))
        self.help_student.triggered.connect(self.calling_student_help)
        self.help_teacher.triggered.connect(self.calling_teacher_help)

    def calling_student_help(self):
        if not self.check_key(self.key_path):
            self.change_mode("student")
        print("call student help")
        self.student_help = HelpWidget("student")
        self.student_help.show()

    def calling_teacher_help(self):
        if not self.check_key(self.key_path):
            self.change_mode("student")
        print("call teacher help")
        self.student_help = HelpWidget("teacher")
        self.student_help.show()

    def change_mode(self, mode: str):
        if self.mode == mode:
            return
        if mode == "teacher":
            if self.centralWidget().objectName() == "task_widget":
                self.centralWidget().teachers_hint.show()
            self.setStyleSheet(f"#MainWindow{{background-image:url({bp.background_image_path});"
                                      "background-size: cover;}"
                                      "#menubar{background-color: rgb(13, 170, 0)}")
            self.setWindowTitle("Расчёт показателей надёжности(Преподаватель)")
            self.action_delete_report.setVisible(True)
            self.action_save_as_docx.setVisible(True)
            self.action_save_as_pdf.setVisible(True)
            self.menu_save_as.menuAction().setVisible(True)
            self.action_import_report.setVisible(True)
        elif mode == "student":
            if self.centralWidget().objectName() == "task_widget":
                self.centralWidget().teachers_hint.hide()
            self.key_path = None
            self.setStyleSheet(f"#MainWindow{{background-image:url({bp.background_image_path});"
                               "background-size: cover;}"
                               "#menubar{background-color: rgb(126, 167, 255)}")
            self.setWindowTitle("Расчёт показателей надёжности")
            self.action_delete_report.setVisible(False)
            self.action_save_as_docx.setVisible(False)
            self.action_save_as_pdf.setVisible(False)
            self.menu_save_as.menuAction().setVisible(False)
            self.action_import_report.setVisible(False)
        self.mode = mode

    def enter_key(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName()[0]
        if file_name == "":
            return
        if self.check_key(file_name):
            self.key_path = file_name
            self.change_mode("teacher")
        else:
            self.change_mode("student")

    def check_key(self, key_path) -> bool:
        try:
            with open(key_path, "rb") as file:
                secret_key = file.read()
            teacher_token = decrypt_file(bp.encrypted_data_path, "teacher_token.txt")
            if teacher_token == b"ERROR_DECRYPT":
                return False
            if secret_key == teacher_token:
                return True
        except Exception:
            return False

    def watch_report(self):
        file_name = (
            QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите отчёт', bp.reports_path, 'TXT(*.txt)')[0]
        )
        if file_name == "":
            return

        report = decrypt_file(bp.reports_path, os.path.basename(file_name),
                              decrypt_file(bp.encrypted_data_path, "teacher_token.txt").decode())
        if report == b"ERROR_DECRYPT":
            message_box_create("Просмотр отчёта", "Не удалось дешифровать отчёт", QMessageBox.Critical)
            return

        docx_path = os.path.abspath(bp.join(bp.tmp_path, "tmp_report.docx"))
        try:
            with open(docx_path, "wb") as decrypted_file:
                decrypted_file.write(report)

            pdf_path = os.path.abspath(bp.join(bp.tmp_path, "tmp_report.pdf"))
            convert(docx_path, pdf_path)
            self.pdf_widget = PdfWidget(pdf_path)
            self.pdf_widget.show()

            os.remove(docx_path)
        except Exception:
            message_box_create("Просмотр отчёта", "Не удалась операция просмотра отчёта", QMessageBox.Critical)

        try:
            os.remove(docx_path)
        except Exception:
            return

    def print_report(self):
        file_name = (
            QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите отчёт', bp.reports_path, 'TXT(*.txt)')[0]
        )
        if file_name == "":
            return

        report = decrypt_file(bp.reports_path, os.path.basename(file_name),
                              decrypt_file(bp.encrypted_data_path, "teacher_token.txt").decode())
        if report == b"ERROR_DECRYPT":
            message_box_create("Печать отчёта", "Не удалось дешифровать отчёт", QMessageBox.Critical)
            return

        try:
            with open(bp.join(bp.tmp_path, "tmp_report.doc"), "wb") as decrypted_file:
                decrypted_file.write(report)

            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                handle = shell.ShellExecuteEx(
                    fMask=256 + 64,
                    lpVerb='printto',
                    lpFile=os.path.abspath(bp.join(bp.tmp_path, "tmp_report.doc")),
                    lpParameters=printer.printerName()
                )
                win32event.WaitForSingleObject(handle['hProcess'], -1)
                os.remove(bp.join(bp.tmp_path, "tmp_report.doc"))
            else:
                os.remove(bp.join(bp.tmp_path, "tmp_report.doc"))
        except Exception:
            message_box_create("Печать отчёта", "Ошибка печати отчёта", QMessageBox.Critical)
            try:
                os.remove(bp.join(bp.tmp_path, "tmp_report.doc"))
            except Exception:
                return

    def save_report(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл для сохранения',
                                                          bp.reports_path, 'TXT(*.txt)')[0]
        if file_name == "":
            return

        pre_name = os.path.basename(file_name)
        new_file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранение файла', pre_name, 'TXT(*.txt)')[0]
        if new_file_name == "" or os.path.abspath(file_name) == os.path.abspath(new_file_name):
            return
        try:
            with open(file_name, "rb") as input_file, open(new_file_name, "wb") as output_file:
                content = input_file.read()
                output_file.write(content)
        except Exception:
            message_box_create("Сохранение отчёта", "Ошибка сохранения отчёта", QMessageBox.Critical)
            return

    def import_report(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл для импорта',
                                                          bp.reports_path, 'TXT(*.txt)')[0]
        if file_name == "":
            return

        pre_name = bp.join(bp.reports_path, os.path.basename(file_name))
        new_file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Импорт файла', pre_name, 'TXT(*.txt)')[0]
        if new_file_name == "" or os.path.abspath(file_name) == os.path.abspath(new_file_name):
            return
        try:
            with open(file_name, "rb") as input_file, open(new_file_name, "wb") as output_file:
                content = input_file.read()
                output_file.write(content)
        except Exception:
            message_box_create("Импорт отчёта", "Ошибка импорта отчёта", QMessageBox.Critical)
            return

    def delete_report(self):
        file_name = (
            QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите отчёт', bp.reports_path, 'TXT(*.txt)')[0]
        )
        if file_name == "":
            return
        try:
            os.remove(file_name)
        except Exception:
            message_box_create("Удаление отчёта", "Ошибка удаления отчёта", QMessageBox.Critical)
            return

    def save_report_as_docx(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите отчёт',
                                                          bp.reports_path, 'TXT(*.txt)')[0]
        if file_name == "":
            return

        report = decrypt_file(bp.reports_path, os.path.basename(file_name),
                              decrypt_file(bp.encrypted_data_path, "teacher_token.txt").decode())
        if report == b"ERROR_DECRYPT":
            message_box_create("Преобразование отчёта в doc", "Не удалось дешифровать отчёт", QMessageBox.Critical)
            return

        pre_name = str(Path(os.path.basename(file_name)).with_suffix(".docx"))
        new_file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранение файла', pre_name, 'word(*.docx *.doc)')[0]
        if new_file_name == "":
            return
        try:
            with open(new_file_name, "wb") as decrypted_file:
                decrypted_file.write(report)
        except Exception:
            message_box_create("Преобразование отчёта в doc", "Ошибка преобразования отчёта", QMessageBox.Critical)
            return

    def save_report_as_pdf(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите отчёт',
                                                          bp.reports_path, 'TXT(*.txt)')[0]
        if file_name == "":
            return

        report = decrypt_file(bp.reports_path, os.path.basename(file_name),
                              decrypt_file(bp.encrypted_data_path, "teacher_token.txt").decode())
        if report == b"ERROR_DECRYPT":
            message_box_create("Преобразование отчёта в pdf", "Не удалось дешифровать отчёт", QMessageBox.Critical)
            return

        try:
            with open(bp.join(bp.tmp_path, "tmp_report.docx"), "wb") as decrypted_file:
                decrypted_file.write(report)

            pre_name = str(Path(os.path.basename(file_name)).with_suffix(".pdf"))
            new_file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранение файла', pre_name, 'PDF files (*.pdf)')[0]
            if new_file_name == "":
                return

            docx_path = os.path.abspath(bp.join(bp.tmp_path, "tmp_report.docx"))
            pdf_path = os.path.abspath(new_file_name)
            convert(docx_path, pdf_path)
            os.remove(docx_path)
        except Exception:
            message_box_create("Преобразование отчёта в pdf", "Ошибка преобразования отчёта", QMessageBox.Critical)
            try:
                os.remove(docx_path)
            except Exception:
                pass

    def calling_calc(self):
        if not self.check_key(self.key_path):
            self.change_mode("student")
        print("call calculator")
        self.calculator = QtWidgets.QWidget()
        self.ui = Ui_calculator()
        self.ui.setupUi(self.calculator)
        self.calculator.show()

    def calling_info(self):
        if not self.check_key(self.key_path):
            self.change_mode("student")
        print("call info")
        self.program_info = QtWidgets.QWidget()
        self.ui = Ui_program_info()
        self.ui.setupUi(self.program_info)
        self.program_info.show()

    def calling_notepad(self):
        if not self.check_key(self.key_path):
            self.change_mode("student")
        print("call notepad")
        self.notepad = NotepadWidget()
        self.notepad.show()

    @staticmethod
    def is_first_launch() -> bool:
        if not os.path.exists(bp.first_launch_txt_path):
            raise Exception("Файл first_launch.txt не существует. Требуется переустановить программу")
        with open(bp.first_launch_txt_path, "r") as fd:
            content = fd.read()
            if content == "true":
                return True
            elif content == "false":
                return False
            else:
                raise Exception("Повреждён файл first_launch.txt. Требуется переустановить программу")

    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        msg = QMessageBox(self)
        msg.setWindowTitle("Выход")
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы действительно хотите выйти ?")
        buttonAceptar = msg.addButton("Да, хочу", QMessageBox.YesRole)
        buttonCancelar = msg.addButton("Отменить", QMessageBox.RejectRole)
        msg.setDefaultButton(buttonAceptar)
        msg.exec_()
        if msg.clickedButton() == buttonCancelar:
            e.ignore()
        print("exit programm")

    def start(self):
        if not self.check_key(self.key_path):
            self.change_mode("student")
        print("click start")
        arg_dict = {"name": self.main_widget.input_name.text(),
                    "group": self.main_widget.input_group.text()}
        variant: str = self.main_widget.input_variant.text()
        variants = os.listdir('encrypted_data')
        if variant.isdigit() and variant_is_exist(variant):
            menu = Tasks(arg_dict, variant, self)
            menu.setObjectName("task_widget")
            self.setCentralWidget(menu)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Вариант не существует")
            msg.setText("Заданный вариант отсутствует в базе вариантов программы")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()


def application():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


application()
