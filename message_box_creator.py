from PyQt5.QtWidgets import QMessageBox


def message_box_create(window_title: str, text: str, icon: QMessageBox.Icon):
    print(text)
    msg_box = QMessageBox()
    msg_box.setWindowTitle(window_title)
    msg_box.setText(text)
    msg_box.setIcon(icon)
    msg_box.exec_()
