from data_base_maneger import DataBaseManager
from dto import DTO
from mapper import Mapper

class TableService():
    def __init__(self):
        self.dataBaseManager = DataBaseManager('processing_tables/project_db.db')
        self.mapper = Mapper()

    # создание записи в табицу вариантов
    def createVariant(self, dto):
        try:
            data = self.mapper.dtoToString(dto);
            self.dataBaseManager.createVariant(data)
            print(f'''[INFO] SQLite -----> CREATE: запись {data} создана.''') 
        except Exception as e:
            print(f'''[WARR] SQLite -----> CREATE: не удалось создать запись.\n
                (Ошибка: {e})''')   
    # чтение записи из табицы вариантов
    def readVariant(self, variant):
        try:
            data = self.dataBaseManager.readVariant(variant)
            dto = self.mapper.stringToDto(data)
            print(f'''[INFO] SQLite -----> READ: запись {data} прочитана.''') 
            return dto
        except Exception as e:
            print(f'''[WARR] SQLite -----> READ: не удалось прочитать запись. Вариант:{variant}.\n
                (Ошибка: {e})''') 
        
    # обновление варианта
    def updateVariant(self, variant, dto):       
        try:
            data = self.mapper.dtoToString(dto);
            self.dataBaseManager.updateVariant(variant, data)
            print(f'''[INFO] SQLite -----> UPDATE: запись {data} обновлена.''') 
        except Exception as e:
            print(f'''[WARR] SQLite -----> UPDATE: не удалось обновить запись. Вариант:{variant}.\n
                (Ошибка: {e})''') 
    
    # удаление записи из табицы вариантов
    def deleteVariant(self, variant):
        try:
            self.dataBaseManager.deleteVariant(variant)
            print(f'''[INFO] SQLite -----> DELETE: запись {variant} удалена.''') 
        except Exception as e:
            print(f'''[WARR] SQLite -----> DELETE: не удалось удалить запись. Вариант:{variant}.\n
                (Ошибка: {e})''') 
            
    # чтение всех записей вариантов         
    def readAll(self):
        try:
            data = self.dataBaseManager.readAll()
            print(data)
            print(f'''[INFO] SQLite -----> READ ALL: записи успешно прочитаны.''') 
        except Exception as e:
            print(f'''[WARR] SQLite -----> READ ALL: не удалось прочитать записи.\n
                (Ошибка: {e})''') 
    
    # удаление всех записей вариантов 
    def deleteAll(self):
        try:
            self.dataBaseManager.deleteAll()
            print(f'''[INFO] SQLite -----> DELETE ALL: записи успешно удалены.''') 
        except Exception as e:
            print(f'''[WARR] SQLite -----> DELETE ALL: не удалось удалить записи.\n
                (Ошибка: {e})''') 




