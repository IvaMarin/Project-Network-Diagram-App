import os
from PyQt5 import QtGui, QtWebEngineWidgets, QtCore


class PdfWidget(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, pdf_path: str, enc):
        super(PdfWidget, self).__init__()
        self.pdf_path = pdf_path
        self.enc = enc
        self.setWindowTitle("Просмотр отчёта")
        self.settings().setAttribute(
            QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        self.settings().setAttribute(
            QtWebEngineWidgets.QWebEngineSettings.PdfViewerEnabled, True)
        self.resize(900, 500)
        self.load(QtCore.QUrl.fromUserInput(self.pdf_path))
        
    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        try:
            os.remove(self.pdf_path)
            self.enc.reEncrypt()
        except Exception:
            return
