import os 
import zipfile # либа для работы с архивами .zip
import pyzipper # либа для шифрования архивов, работает на основе либы zipfile 

class encrypt_decrypt():
    def __init__(self):
        self.secret_password = b'pirat_encrypt123' # пароль для архива
        self.pathToEncry = os.path.abspath(os.curdir)# + '\\encrypted_data' # путь до дирриктории в которой лежат файлы которые нужно шифровать
        self.exceptToZipFile = ['encry_decry.py'] # файлы которые не нужно шифровать в данной дирректории

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
                zf.write(file)

        self.clearDir()
        
    def decryptAll(self, nameZipFile = 'encrypted_data.zip'): # расшифровываем весь архив 
        with pyzipper.AESZipFile(nameZipFile, 'r', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) \
                as extracted_zip:
            try:
                extracted_zip.extractall(path=self.pathToEncry ,pwd=self.secret_password)
            except RuntimeError as ex:
                print(ex)

    def addFileInZip(self, fileName, nameZipFile = 'encrypted_data.zip'): # добавление файла в существующий архив по имени этого файла
        if fileName in self.exceptToZipFile:
            print("Файл находится в списке исключений")
            return
        with pyzipper.AESZipFile(nameZipFile,
                                'a',
                                compression=pyzipper.ZIP_LZMA,
                                encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(self.secret_password)

            zf.write(fileName)

    def extractFileInZip(self, fileName, nameZipFile = 'encrypted_data.zip'): # извлечение файла по имени из архива

        with pyzipper.AESZipFile(nameZipFile, 'r', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) \
                as extracted_zip:
            try:
                extracted_zip.extract(member=fileName, path=self.pathToEncry ,pwd=self.secret_password)
            except RuntimeError as ex:
                print(ex)

    def clearDir(self):
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
            if os.path.isfile(file): 
                print(file)
                os.remove(file) 
                print("success") 
            else: 
                print("File doesn't exists!")

    def delFile(self, fileName):

        files = os.listdir(self.pathToEncry)

        zipFiles = [file for file in files if ".zip" in file]

        if fileName in self.exceptToZipFile or fileName in zipFiles:
            print("Файл находится в списке исключений")
            return
        else: 
            os.remove(fileName) 



if __name__ == "__main__":
    
    encry_decry = encrypt_decrypt()
    encry_decry.encryptAll()

    # input()

    # encry_decry.addFileInZip("test.json")

    # encry_decry.decryptAll()

    #encry_decry.extractFileInZip("test.json")



    