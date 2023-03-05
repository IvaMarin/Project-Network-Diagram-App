from PyQt5.QtCore import QThread, pyqtSignal


class ThreadedReportWatch(QThread):
    countChanged = pyqtSignal(int)

    def __init__(self, mainWindow, encrypt, report, parent=None):
        QThread.__init__(self, parent)
        self.mainWindow = mainWindow
        self.encrypt = encrypt
        self.report = report

    def run(self):
        """Report watch."""
        self.mainWindow.runWatchReport(self.report, self.countChanged)


