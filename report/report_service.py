from PyPDF2 import PdfWriter, PdfReader
from report import pdf_viewer as pdf_viewer

import os


class ReportService():

    def __init__(self, password):
        self.password = password
        self.viewer = pdf_viewer.Viewer()

    def add_text(self, report, text, x=65):
        # report.add_font('DejaVu', '', 'resources/fonts/DejaVuSansCondensed.ttf', uni=True)
        report.set_font('DejaVu', '', 16)
        report.set_x(x)
        report.multi_cell(170, 10, text, 0, 1, "C")

    def add_image(self, report, path_image):

        try:
            report.image(path_image, 25, 60, 240)
        except:
            print(path_image + ' not found')

    def add_hist(self, report, path_image):
        try:
            report.image(path_image, 80, 60, h=130)
        except:
            print(path_image + ' not found')

    def create_task_page(self, report, text, path_image, hist='N'):

        report.add_page()
        self.add_text(report, text)
        if hist != 'H':
            self.add_image(report, path_image)
        else:
            self.add_hist(report, path_image)
        return report

    def pdf_encry(self, pdf_path="pdf_encry_decry/1.pdf"):

        print("PASS" + self.password)

        out = PdfWriter()
        pdf = PdfReader(pdf_path)

        num = len(pdf.pages)

        for i in range(num):
            page = pdf.pages[i]
            out.add_page(page)

        try:
            out.encrypt(self.password)
            with open(pdf_path, "wb") as f:
                out.write(f)
            print("PDF зашифрован и записан!")
        except:
            print("PDF не зашифровался или не записался!")

    def pdf_decry(self, pdf_path="pdf_encry_decry/1.pdf"):

        print("PASS" + self.password)

        out = PdfWriter()
        pdf = PdfReader(pdf_path)

        # Check if the opened pdf is actually Encrypted
        if pdf.is_encrypted:
            pdf.decrypt(self.password)

            for i in range(len(pdf.pages)):
                page = pdf.pages[i]
                out.add_page(page)

            with open(pdf_path, "wb") as f:
                out.write(f)

            print("PDF расшифрован!")
        else:
            print("PDF уже расшифрован!")

    def pdf_show(self, path, loading):
        self.viewer.show_PDF(path, loading)

    def pdf_save(self, folder_source, path_to_save):

        print("DIR source      " + os.path.abspath(folder_source))
        print("DIR save        " + path_to_save)

        get_files = os.listdir(folder_source)

        for g in get_files:
            print(g)
            os.replace(os.path.abspath(folder_source) +
                       "/" + g, path_to_save + "/" + g)
