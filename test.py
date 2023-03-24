import os
import sys

from PIL.ImageQt import ImageQt
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton
import tempfile

from pdf2image import convert_from_path


class PrintDemo(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(192, 128))
        self.setWindowTitle("Print Demo")

        printButton = QPushButton('Print', self)
        printButton.clicked.connect(self.onPrint)
        printButton.resize(128, 32)
        printButton.move(32, 48)

    def onPrint(self):
        self.printDialog()

    def printDialog(self):
        filePath, filter = QFileDialog.getOpenFileName(self, 'Open file', '', 'PDF (*.pdf)')
        if not filePath:
            return
        file_extension = os.path.splitext(filePath)[1]

        if file_extension == ".pdf":
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                with tempfile.TemporaryDirectory() as path:
                    images = convert_from_path(filePath, dpi=300, output_folder=path)
                    painter = QPainter()
                    painter.begin(printer)
                    for i, image in enumerate(images):
                        if i > 0:
                            printer.newPage()
                        rect = painter.viewport()
                        qtImage = ImageQt(image)
                        qtImageScaled = qtImage.scaled(rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        painter.drawImage(rect, qtImageScaled)
                    painter.end()
        else:
            pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = PrintDemo()
    mainWin.show()
    sys.exit(app.exec_())





# from processing_tables.dto import DTO
# import re
# import numpy as np 
# from processing_tables.variant_controller import VariantController
# import os


# def purge(dir, pattern):
#     for f in os.listdir(dir):
#         if re.search(pattern, f):
#             print(os.path.join(dir, f))
#             os.remove(os.path.join(dir, f))

# purge('test_dir/1/', f'state_{0}')


# pathToEncry = os.path.abspath(os.curdir) + '/report_answer'
# files = os.listdir(pathToEncry)
# photoFiles = [file for file in files if ".txt" in file]
# print(photoFiles)

# vc = VariantController()

# vc.getAllNumberOfVariant()



# dto = DTO()
# dto.cipherOfWorks = [1, 2, 3, 4]
# dto.duration = [2, 4, 5, 6]
# dto.performers = [2, 3, 8, 9]
# dto.numberOfPerformers = [3, 4, 5, 6]
# dto.numberOfDivision = [8, 6]
# dto.numberOfPeople = [5, 5]
# dictionaryParametrs = dto.__dict__

# listData = []

# for key in dictionaryParametrs:
#     if type(dictionaryParametrs[key]) == list:
#         listData.append(dictionaryParametrs[key]) 



# length = len(listData[0])

# for i in listData:
#     while len(i) < length:
#         i.append(-1)

# print(listData)
# l = [] 
# l = list(map(list, zip(*listData)))
# for i in l:
#     try:
#         while True:
#             i.remove(-1)
#     except:
#         pass
# print(l)

# fileName = 'variant_table_data.txt'
# lis = [['1', '2', '3'], ['4', '3'], ['9', '7', '6', '5', '4'], ['1'], ['2'], ['3'], ['4'], ['5']]

# f = open(fileName,'a+')
# try:
#     # работа с файлом
#     f.write('1' + '\n')
#     print("OK write")
# finally:
#     f.close()

# f = open(fileName,'a+')
# try:
#     # работа с файлом
#     listData = lis

#     for row in listData:
#         f.write(' '.join([a for a in row]) + '\n')
#     print("OK write")
# finally:
#     f.close()

# f = open(fileName,'r+')
# try:
#     # работа с файлом
#     listData = []
#     lines = f.readlines()
#     for line in lines:
#         l = re.split(' |\n', line)
#         try:
#             l.remove('')
#         except:
#             pass
#         print(l)
#         listData.append(l)
    
#     print(listData)

    
#     i = 0
#     for key in dictionaryParametrs:
#         if type(dictionaryParametrs[key]) == str:
#             dictionaryParametrs[key] = listData[i][0]
#         elif type(dictionaryParametrs[key]) == list:
#             dictionaryParametrs[key] = listData[i]
#         print(i)
#         i = i + 1
    
#     print(dto.cipherOfWorks)
#     print(dto.duration)
#     print(dto.variant)

# finally:
#     f.close()