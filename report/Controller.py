from report import Report as rep
from report import Service as serv

import os

class ReportController():
    
    def __init__(self, password = "password"):
        self.report = rep.Report(orientation='L', unit='mm', format='A4')

        self.title = ""
        self.text_information_student = ""
        self.password = password

        self.folder_source = "report_answer//"
        self.pdf_is_maked = False

        self.service = serv.ReportService(self.password)

    def set_title(self, title):
        self.title = title

    def set_information_student(self, information_student):
        self.text_information_student = information_student


    def create_start_page(self):

        self.report.add_page()
        #self.report.add_font('DejaVu', '', 'resources/fonts/DejaVuSansCondensed.ttf', uni=True)
        self.report.set_font('DejaVu', '', 14)
        self.report.cell(190, 20, "", ln=1)
        self.report.set_x(65)
        self.report.multi_cell(170, 10, self.title, 1, "C")

        

    def create_report(self, list_pictures = [], list_teach_enter=[], path_folder = 'encrypted_data/', title = "", information_student = "", is_show=True):

        if self.pdf_is_maked == False:
            self.set_title(title)
            self.set_information_student(information_student)
            self.create_start_page()

            self.report.add_page()
            #self.report.add_font('DejaVu', '', 'resources/fonts/DejaVuSansCondensed.ttf', uni=True)
            self.report.set_font('DejaVu', '', 14)
            self.report.cell(190, 20, "", ln=1)
            
            self.service.add_text(self.report, "Статус выполненных заданий", 100)
            self.report.ln(10)
            text_1 = " выполнено."
            text_2 = " выполнено при помощи перподавателя."

            self.report.set_x(15)
            for i in range(len(list_teach_enter)):
                if (list_teach_enter[i]):
                    text = text_2
                else:
                    text = text_1
                self.service.add_text(self.report, "Задание №" + str(i+1) + text)
                

            for i in range(len(list_pictures)-1):
                if len(list_pictures[i]) == 1:
                    self.service.create_task_page(self.report, "Задание №" +  str(i+1), list_pictures[i][0])

                else:
                    for j in range(len(list_pictures[i])):
                        self.service.create_task_page(self.report, "Задание №" +  str(i+1) + " (отделение " + str(j+1) + ")", list_pictures[i][j])
                
            
            self.service.create_task_page(self.report, "Гистограмма", list_pictures[6][0], 'H')

            name_report = self.text_information_student +'.pdf'
            path_report = path_folder + name_report
            save_time_path = self.folder_source + name_report

            self.report.output(path_report)
            self.report.output(save_time_path)

            self.pdf_is_maked = True
            # #показ отчета студенту
            # if is_show:
            #     self.service.pdf_show(save_time_path)
            print(save_time_path)
            self.encrypt(save_time_path)
        
        self.show_current()


    def show_current(self):
        
        name_report = self.text_information_student +'.pdf'
        save_time_path = self.folder_source + name_report

        self.decrypt(save_time_path)
        self.service.pdf_show(save_time_path)
        self.encrypt(save_time_path)


    def whatch_report(self, path):
        #распоковка отчета
        try:
            self.service.pdf_decry(path)
        except:
            print("Ошибка обработки файла " + path)
        
        try:
            self.service.pdf_show(path)
        except:
            print("Ошибка просмотра")
        
        #запоковка отчета
        try:
            self.service.pdf_encry(path)
        except:
            print("Ошибка обработки файла " + path)

    def save_report(self, path_to_save):
        try:
            self.service.pdf_save(self.folder_source, path_to_save)
        except Exception as e:
            print(e)
            print("Проблема с сохранением файла!")

        

    def encrypt(self, path):
        try:
            self.service.pdf_encry(path)
        except:
            print("Ошибка обработки файла " + path)


    def decrypt(self, path):
        try:
            self.service.pdf_decry(path)
        except:
            print("Ошибка обработки файла " + path)