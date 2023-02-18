from fpdf import FPDF

class Report(FPDF):

    def header(self):
        file = open("student_info.txt", 'r')
        surname = file.readline().split(" ")
        variant = file.readline()
        group = file.readline()
        file.close()
        
        fio = surname[0]
        for i in range(1, len(surname)):
            fio = fio + " " + surname[i][0] + '.'

        # Logo
        self.image('report/logo_mac_mai-min.png', 15, 8, 30)
        self.image('report/logo_mca-min.png', 252, 8, 30)
        # Arial bold 15
        self.set_x(40)
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)
        # Move to the right
        self.cell(80)
        # Title
        self.multi_cell(100, 10, "Вариант №" + variant + "ФИО: " + fio + "\nГруппа " + group, 0, 0, 'C')
        # Line break
        self.ln(10)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # DejaVu 8
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 8)
        # Page number
        self.cell(0, 10, 'Стр. ' + str(self.page_no()), 0, 0, 'C')

# pdf = Report(orientation='L', unit='mm', format='A4')

# pdf.output("T1.pdf")