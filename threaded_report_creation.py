from PyQt5.QtCore import QThread, pyqtSignal


class ThreadedReportCreation(QThread):
    countChanged = pyqtSignal(int)

    def __init__(self, mainWindow, window6, encrypt, parent=None):
        QThread.__init__(self, parent)
        self.mainWindow = mainWindow
        self.window6 = window6
        self.encrypt = encrypt

    def run(self):
        """Report creation."""

        self.window6._finishTimer()
        self.window6.widgetRight.save()
        self.encrypt.addFileInZip('6_hist.jpg')

        for i in range(len(self.window6.images)):
            strTemp = str(6)+str(i)+".jpg"
            self.window6.images[i].save('encrypted_data/'+strTemp)

        for i in range(len(self.window6.images)):
            strTemp = str(6)+str(i)+".jpg"
            self.encrypt.addFileInZip(strTemp)

        self.mainWindow.creatReport(self.countChanged)

        self.window6.backMainMenu()
