import os


def join(*args):
    return os.path.join(*args).replace(os.path.sep, "/")


basedir = os.path.dirname(__file__)
main_window_path = join(basedir, "main_window.ui")
main_label_image = join(basedir, "images", "main_label.png")
background_image_path = join(basedir, "images", "background.jpg")
encrypted_data_path = join(basedir, "encrypted_data")
reports_path = join(basedir, "reports")
tmp_path = join(basedir, "tmp")
main_widget_path = join(basedir, "main_widget.ui")
images_path = join(basedir, "images")
first_launch_txt_path = join(basedir, "utils", "first_launch", "first_launch.txt")
report_template_docx_path = join(basedir, "utils", "report", "report_template.docx")
