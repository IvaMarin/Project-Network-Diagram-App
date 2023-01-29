import report.Report as rep
import report.Service as serv

class ReportController():
    
    def __init__(self, text_information_student=None, path_logo=None, text_title=None):
        self.report = rep.Report(orientation='L', unit='mm', format='A4')

        self.report.add_page()
        self.report.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.report.set_font('DejaVu', '', 14)
        self.report.cell(190, 20, "", ln=1)
        self.report.set_x(65)
        self.report.multi_cell(170, 10, text_title, 1, "C")

        self.service = serv.ReportService()
        self.text_information_student = text_information_student



    def create_report(self, list_pictures, list_teach_enter=None):

        self.report.add_page()
        self.report.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
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
                    self.service.create_task_page(self.report, "Задание №" +  str(i+1) + " (часть " + str(j+1) + ")", list_pictures[i][j])
            
        
        self.service.create_task_page(self.report, "Гистограмма", list_pictures[6][0], 'H')

        name_report = self.text_information_student +'.pdf'
        self.report.output('encrypted_data/' + name_report)

        return name_report


    def whatch_report(self, report):
        pass