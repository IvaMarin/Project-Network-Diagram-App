import os
from PyQt5 import QtGui, QtWebEngineWidgets, QtCore


class PdfWidget(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, pdf_path: str, enc):
        print("Вот тут херня 1")
        super(PdfWidget, self).__init__()
        print("Вот тут херня 2")
        self.pdf_path = pdf_path
        print("Вот тут херня 3")
        self.enc = enc
        print("Вот тут херня 4")
        self.setWindowTitle("Просмотр отчёта")
        print("Вот тут херня 5")
        self.settings().setAttribute(
            QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        print("Вот тут херня 6")
        self.settings().setAttribute(
            QtWebEngineWidgets.QWebEngineSettings.PdfViewerEnabled, True)
        print("Вот тут херня 7")
        self.resize(900, 500)
        print("Вот тут херня 8")
        self.load(QtCore.QUrl.fromUserInput(self.pdf_path))
        print("Вот тут херня 9")
        
    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        try:
            os.remove(self.pdf_path)
            self.enc.reEncrypt()
        except Exception:
            return
