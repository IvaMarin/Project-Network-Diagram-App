class ReportService():

    def __init__(self):
        pass

    def add_text(self, report, text, x = 65):
        report.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        report.set_font('DejaVu', '', 16)
        report.set_x(x)
        report.multi_cell(170, 10, text, 0, 1, "C")

    def add_image(self, report, path_image):
        try:
            report.image(path_image, 25, 60, 240)
        except:
            print(path_image + ' not found')

    def create_task_page(self, report, text, path_image):
        report.add_page()
        self.add_text(report, text)
        self.add_image(report, path_image)
        return report
    

