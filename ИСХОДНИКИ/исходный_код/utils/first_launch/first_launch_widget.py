from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from pathlib import Path
from utils.encrypt.encrypt_module import initial_decrypt_file, aes_encrypt, aes_generate_key
from message_box_creator import message_box_create

import os
import basedir_paths as bp


def find_files(catalog: Path) -> list[Path]:
    res = []
    for root, dirs, files in os.walk(catalog.resolve()):
        res += [Path(os.path.join(root, name)) for name in files
                if Path(name).suffix.lower() in ['.json', '.jpg', '.txt']]
    return res


def show_first_launch_widget(main_window: QtWidgets.QMainWindow, next_widget: QtWidgets.QWidget):
    main_window.setCentralWidget(FirstLaunchWidget(main_window, next_widget))


class FirstLaunchWidget(QtWidgets.QWidget):
    def __init__(self, main_window, next_widget):
        super(QtWidgets.QWidget, self).__init__()
        self.main_window = main_window
        self.next_widget = next_widget

        self.setWindowTitle("Первоначальная дешифровка файлов")
        self.setGeometry(0, 0, 900, 800)

        font = QtGui.QFont()
        font.setPointSize(12)
        font.style()

        self.select_key_file_button = QtWidgets.QPushButton(self)
        self.select_key_file_button.setGeometry(400, 400, 400, 100)
        self.select_key_file_button.setText("Выберите файл-ключ")
        self.select_key_file_button.setStyleSheet("background-color: rgb(224, 234, 255);")
        self.select_key_file_button.setFont(font)
        self.select_key_file_button.clicked.connect(lambda: self.select_key(self.main_window, self.next_widget))

    def select_key(self, main_window, next_widget):
        file_name = QtWidgets.QFileDialog.getOpenFileName()[0]
        if file_name == "":
            return

        if not os.path.exists(file_name):
            message_box_create("Первоначальная дешифровка файлов", "Выбранный ключ-файл не существует",
                               QMessageBox.Critical)
            return

        try:
            with open(file_name, "rb") as file:
                key = file.read()
        except Exception:
            message_box_create("Первоначальная дешифровка файлов", "Выбранный ключ-файл повреждён",
                               QMessageBox.Critical)
            return

        try:
            found_files = find_files(Path(bp.encrypted_data_path))
        except Exception:
            message_box_create("Первоначальная дешифровка файлов", "Не удалось дешифровать файлы программы",
                               QMessageBox.Critical)
            return

        for file in found_files:
            try:
                content = initial_decrypt_file(file, key.decode())
            except Exception:
                message_box_create("Первоначальная дешифровка файлов",
                                   "Выбранный ключ-файл не подходит для дешифровки файлов", QMessageBox.Critical)
                return
            if content == b"ERROR_DECRYPT":
                message_box_create("Первоначальная дешифровка файлов",
                                   "Выбранный ключ-файл не подходит для дешифровки файлов", QMessageBox.Critical)
                return
            nonce, cipher_content, tag = aes_encrypt(content, aes_generate_key())
            try:
                with open(file.resolve(), "wb") as output_file:
                    output_file.write(nonce)
                    output_file.write(tag)
                    output_file.write(cipher_content)
            except Exception:
                message_box_create("Первоначальная дешифровка файлов", "Не удалось зашифровать файлы программы",
                                   QMessageBox.Critical)
                return
        try:
            with open(bp.first_launch_txt_path, "w") as fd:
                fd.write("false")
        except Exception:
            message_box_create("Первоначальная дешифровка файлов",
                               "Файлы программы повреждены. Необходимо переустановить программу", QMessageBox.Critical)

        main_window.setCentralWidget(next_widget)
