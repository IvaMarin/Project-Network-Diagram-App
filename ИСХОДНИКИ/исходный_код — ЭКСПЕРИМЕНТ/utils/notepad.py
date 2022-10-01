from PyQt5 import QtWidgets, QtGui
import basedir_paths as bp


class NotepadWidget(QtWidgets.QWidget):
    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        self.setWindowIcon(QtGui.QIcon(bp.join(bp.images_path, "vuc.ico")))
        self.setWindowTitle("Блокнот")
        self.setGeometry(500, 500, 400, 500)

        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setGeometry(0, 27, 400, 473)

        self.font_size_box = QtWidgets.QSpinBox(self)
        self.font_size_box.setGeometry(20, 0, 40, 20)
        self.font_size_box.setValue(20)
        self.font_size_box.valueChanged.connect(self.set_font_size)

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        self.text_edit.resize(e.size().width(), e.size().height() - 27)
        print("notebook resize")

    def set_font_size(self):
        value = self.font_size_box.value()
        self.text_edit.setFontPointSize(value)
