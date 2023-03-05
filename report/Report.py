# Этот класс используется для отображения отчетов
# Класс унаследован от библиотеки FPDF
# Переопределены методы описания коллонтитулов

from fpdf import FPDF

class Report(FPDF):

    # Функция описания верхнего коллонтитула
    def header(self):
        # считывание нформации о студенте из файла
        file = open("student_info.txt", 'r') 

        surname = file.readline().split(" ")
        variant = file.readline()
        group = file.readline()
        file.close()
        
        fio = surname[0]
        for i in range(1, len(surname)):
            fio = fio + " " + surname[i][0] + '.'

        # Подключение логотипов МАИ и АКМ
        # self.image('report/logo_mac_mai-min.png', 15, 8, 30)
        # self.image('report/logo_mca-min.png', 252, 8, 30)

        # шрифт DejaVu 8
        self.set_x(0)
        self.add_font('DejaVu', '', 'resources/fonts/DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)
        # Move to the right
        self.cell(40)
        # Title
        self.multi_cell(100, 10, "ВАРИАНТ №" + variant + "ФИО: " + fio + "\nВЗВОД: " + group, 0, 0, 'L')
        # Line break
        self.ln(10)

    # Функция описания нижнего коллонтитула
    def footer(self):
        # позиция 1.5 см от нижнего края
        self.set_y(-15)
        # шрифт DejaVu 8
        #self.add_font('DejaVu', '', 'resources/fonts/DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)
        # номера страниц
        self.cell(0, 10, 'Стр. ' + str(self.page_no()), 0, 0, 'C')
