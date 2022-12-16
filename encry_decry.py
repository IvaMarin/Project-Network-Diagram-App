import os 
import zipfile # либа для работы с архивами .zip
import pyzipper # либа для шифрования архивов, работает на основе либы zipfile 

class encrypt_decrypt():
    def __init__(self):
        self.secret_password = b'pirat_encrypt123' # пароль для архива
        self.pathToEncry = os.path.abspath(os.curdir) + '\\encrypted_data' # путь до дирриктории в которой лежат файлы которые нужно шифровать
        self.pathToDecry = os.path.abspath(os.curdir) # путь до дирриктории куда надо положить расшифрованную папку
        self.exceptToZipFile = [] # файлы которые не нужно шифровать в данной дирректории encry_decry.py

    def encryptAll(self, nameZipFile = 'encrypted_data.zip'): # функция шифрования всех нужных нам файлов
        print("\n")
        print(self.pathToEncry)
        print("\n")
        files = os.listdir(self.pathToEncry)

        print(files)

        for filename in self.exceptToZipFile: # удаление из списка файлов для шифрования файлы исключения 
            files.remove(filename)

        with pyzipper.AESZipFile(nameZipFile,
                                'w',
                                compression=pyzipper.ZIP_LZMA,
                                encryption=pyzipper.WZ_AES) as zf: # открываем архиф и далее работаем с ним после окончания with он закроется сам
            zf.setpassword(self.secret_password) # устанавливаем пароль 

            for file in files: # добавляем файлы в архив 
                zf.write('encrypted_data\\' + file)

        self.clearDir()
        
    def decryptAll(self, nameZipFile = 'encrypted_data.zip'): # расшифровываем весь архив 
        with pyzipper.AESZipFile(nameZipFile, 'r', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) \
                as extracted_zip:
                
            
            extracted_zip.extractall(path=self.pathToDecry ,pwd=self.secret_password)
        self.delZipFile(fileName='encrypted_data.zip')

    def addFileInZip(self, fileName, nameZipFile = 'encrypted_data.zip'): # добавление файла в существующий архив по имени этого файла
        if fileName in self.exceptToZipFile:
            print("Файл находится в списке исключений")
            return
        with pyzipper.AESZipFile(nameZipFile,
                                'a',
                                compression=pyzipper.ZIP_LZMA,
                                encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(self.secret_password)

            zf.write('encrypted_data\\' + fileName)

        self.delFile(fileName)

    def extractFileFromZip(self, fileName, nameZipFile = 'encrypted_data.zip'): # извлечение файла по имени из архива

        with pyzipper.AESZipFile(nameZipFile, 'r', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) \
                as extracted_zip:
                fileName = 'encrypted_data' '/' + fileName # нельзя использовать слеши как в пути в виндус с экранированием нужно юзать / он сам поменяется на то что нужно для архива (в винде на \\)
                extracted_zip.extract(member=fileName, path=self.pathToDecry ,pwd=self.secret_password)


    def clearDir(self):# удаляем все файлы вне архива кроме файлов исключений (.py и .zip)
        print("\n")
        print(self.pathToEncry)
        print("\n")
        files = os.listdir(self.pathToEncry)

        print(files)

        zipFiles = [file for file in files if ".zip" in file]

        for filename in self.exceptToZipFile: # удаление из списка файлов для удаления файлы исключения 
            files.remove(filename)

        for filename in zipFiles: # удаление из списка файлов для удаления файлы .zip 
            files.remove(filename)

        for file in files:
            if os.path.isfile(self.pathToEncry + '\\' + file): 
                print(file)
                os.remove(self.pathToEncry + '\\' + file) 
                print("success") 
            else: 
                print("File doesn't exists!")

    def delFile(self, fileName): #  удаляем файл по названию не из архива

        files = os.listdir(self.pathToEncry)

        zipFiles = [file for file in files if ".zip" in file]

        if fileName in self.exceptToZipFile or fileName in zipFiles:
            print("Файл находится в списке исключений")
            return
        else: 
            os.remove(self.pathToEncry + '\\' + fileName) 
    
    def delZipFile(self, fileName):# удаление zip архив по названию файла

        if fileName in self.exceptToZipFile:
            print("Файл находится в списке исключений")
            return
        else: 
            os.remove(fileName) 

    def delImaFromZip(self, nameZipFile = 'encrypted_data.zip'): # удаление изображений из архива
        self.decryptAll()
        files = os.listdir(self.pathToEncry)
        photoFiles = [file for file in files if ".jpg" in file]
        for file in photoFiles:
            self.delFile(file)
        self.encryptAll()

    def extractAllDocxFile(self):
        self.decryptAll()
        files = os.listdir(self.pathToEncry)
        docxFiles = [file for file in files if ".docx" in file]
        for filename in docxFiles: #  
            files.remove(filename)
        for filename in files:
            self.addFileInZip(fileName=filename)

    def reEncrypt(self):
        self.decryptAll()
        self.encryptAll()





# if __name__ == "__main__":
    
#     encry_decry = encrypt_decrypt()
#     # encry_decry.encryptAll()

#     # input()

#     # encry_decry.addFileInZip("test1.json")
#     # encry_decry.delFile("test1.json")
#     # encry_decry.extractFileFromZip("test.json")


#     encry_decry.decryptAll()

 



    