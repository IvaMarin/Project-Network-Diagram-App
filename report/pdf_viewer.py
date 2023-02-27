from tkinter import *
from PIL import Image, ImageTk
from pdf2image import convert_from_path


class Viewer():

    def __init__(self):
        pass

    def show_PDF(self, path, loading):

        # Создаем контейнер ткинтера
        loading.emit(30)  # Процесс загрузки 30%
        root = Tk()

        # размер экрана
        monitor_height = root.winfo_screenheight()
        monitor_width = root.winfo_screenwidth()

        # Положение и размер окна (тут только ширина и высота)
        root.geometry(f"{monitor_width-20}x{monitor_height-20}")
        root.config(bg="gray70")
        root.title("Просмотр отчета")

        # Добавим скролл
        loading.emit(50)  # Процесс загрузки 50%
        scrol_y = Scrollbar(root, orient=VERTICAL)
        # Используем Text, чтобы добавлять изображения
        pdf = Text(root, yscrollcommand=scrol_y.set, bg="gray70")
        # упаковываем скрол направа
        # fill растягивает по указанному параметру в свободное место
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=pdf.yview)
        # Упаковываем наш пдф
        pdf.pack(fill=BOTH, padx=round(monitor_width*0.1), expand=True)

        # конвертируем страницы пдф в список изображений
        loading.emit(70)  # Процесс загрузки 70%
        print("!!!!!!!!" + path)

        pages = convert_from_path(path)
        # фотки пдф страниц
        photos = []
        # подгоняем под размер уаждцю фотку и собираем их в лист
        for i in range(len(pages)):
            # pages[i].save('report/image/page'+ str(i) +'.jpg', 'JPEG')
            # img = pages[i].resize((round(monitor_width*0.5), round((monitor_width*0.5)/1.4142)))

            img = pages[i].resize(
                (round(monitor_width*0.8), round((monitor_width*0.8)/1.4142)))
            photos.append(ImageTk.PhotoImage(img))

        # добавляем фотки в наш viewer
        loading.emit(90)  # Процесс загрузки 90%
        for photo in photos:
            pdf.image_create(END, image=photo)
            # отступ между страницами
            pdf.insert(END, '\n\n')

        loading.emit(100)  # Процесс загрузки 100%
        root.mainloop()
