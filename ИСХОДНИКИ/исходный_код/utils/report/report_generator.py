from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docx.shared import Mm
from message_box_creator import message_box_create
from PyQt5.QtWidgets import QMessageBox
from utils.encrypt.encrypt_module import *

import basedir_paths as bp


class TemplateContextElement:

    """
    key - ключ в шаблоне отчета
    value - значение, которое будет подставлено в отчет вместо ключа
    is_image - флаг, который показывает является ли value путём до изображения
    """
    def __init__(self, key: str, value: str, is_image: bool = False, width: int = 150, height: int = 80):
        self.key = key
        self.value = value
        self.is_image = is_image
        self.width = width
        self.height = height


class TemplateContext:

    """
    path_to_template - путь до шаблона отчета
    path_to_result - путь до зашифрованного варианта отчета. Сделать в формате ФИО_подразделение_дата (формат любой)
    """
    def __init__(self, path_to_template: str, path_to_result: str):
        self.context = {}
        self.input_doc = DocxTemplate(path_to_template)
        self.path_to_result = path_to_result
        self.output_doc = None

    """
    Заполнение параметров шаблона
    template_context_elements: List[TemplateContextElement] - список параметров для шаблона
    """
    def fill_parameters(self, template_context_elements):
        for elem in template_context_elements:
            if elem.is_image:
                self.context[elem.key] = InlineImage(self.input_doc, elem.value, width=Mm(elem.width), height=Mm(elem.height))
            else:
                self.context[elem.key] = elem.value

    """
    Генерация отчета в зашифрованном виде
    """
    def generate_report(self):
        self.input_doc.render(self.context)
        tmp_path_report = bp.join(bp.tmp_path, "report.docx")
        self.input_doc.save(tmp_path_report)
        try:
            with open(tmp_path_report, "rb") as input_file, open(self.path_to_result, "wb") as output_file:
                content = input_file.read()
                teacher_token = decrypt_file(bp.encrypted_data_path, "teacher_token.txt")
                nonce, cipher_content, tag = aes_encrypt(content, teacher_token)
                output_file.write(nonce)
                output_file.write(tag)
                output_file.write(cipher_content)
        except Exception:
            message_box_create("Генерация отчёта", "Повреждены данные программы", QMessageBox.Information)
        try:
            os.remove(tmp_path_report)
        except Exception:
            return


if __name__ == "__main__":
    template_context = TemplateContext("report_template.docx", "Пупкин_АСУ-301_11-11-2011.docx")
    template_context_elements = []
    template_context_elements.append(TemplateContextElement("fioStudent", "Пупкин"))
    template_context_elements.append(TemplateContextElement("group", "АСУ-301"))
    template_context_elements.append(TemplateContextElement("date", "11.11.2011"))
    template_context_elements.append(TemplateContextElement("numberVariant", "4"))
    template_context_elements.append(TemplateContextElement("inputData", "kot-leopold.jpg", True))
    template_context_elements.append(TemplateContextElement("task1", "Задание1"))
    template_context_elements.append(TemplateContextElement("answer1", "kot-leopold.jpg", True))
    template_context_elements.append(TemplateContextElement("countErrors1", "1"))
    template_context_elements.append(TemplateContextElement("task2", "Задание2"))
    template_context_elements.append(TemplateContextElement("answer2", "kot-leopold.jpg", True))
    template_context_elements.append(TemplateContextElement("countErrors2", "2"))
    template_context_elements.append(TemplateContextElement("task3", "Задание3"))
    template_context_elements.append(TemplateContextElement("answer3", "kot-leopold.jpg", True))
    template_context_elements.append(TemplateContextElement("countErrors3", "3"))
    template_context_elements.append(TemplateContextElement("task4", "Задание4"))
    template_context_elements.append(TemplateContextElement("answer4", "kot-leopold.jpg", True))
    template_context_elements.append(TemplateContextElement("countErrors4", "4"))
    template_context_elements.append(TemplateContextElement("task5", "Задание5"))
    template_context_elements.append(TemplateContextElement("answer5", "kot-leopold.jpg", True))
    template_context_elements.append(TemplateContextElement("countErrors5", "5"))
    template_context_elements.append(TemplateContextElement("task6", "Задание6"))
    template_context_elements.append(TemplateContextElement("answer6", "kot-leopold.jpg", True))
    template_context_elements.append(TemplateContextElement("countErrors6", "6"))
    template_context_elements.append(TemplateContextElement("task7", "Задание7"))
    template_context_elements.append(TemplateContextElement("answer7", "kot-leopold.jpg", True))
    template_context_elements.append(TemplateContextElement("countErrors7", "7"))
    template_context.fill_parameters(template_context_elements)
    template_context.generate_report()
