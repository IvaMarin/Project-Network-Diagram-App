import numpy as np
import sqlite3 as sl




class BDReadWrite():
    def __init__(self, nameBD = "varForGraph"):
        self.con = sl.connect(nameBD)
        

    def creatTable(self, numTable = 16, nameTable = "VAR", nameCol = ['id_num_var', 'job_code', 'num_squad', 'num_peop_do_work', 'duration_work']):
        self.listNameTable = []
        self.listNameTable.append("VARIANTS") #название главной таблицы мб и не нужна 
        self.listNameCol = nameCol # название колонок в таблице 
        # with self.con: # генерация таблицы вариантов (главной таблицы)
        #     self.con.execute("""
        #         CREATE TABLE IF NOT EXISTS VARIANTS (
        #             id_var INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        #             id_num_var INTEGER NOT NULL,
        #             FOREIGN KEY (id_num_var) REFERENCES auth(id_num_var)
        #         );
        #     """)
        SQLRequests = []
        for i in range(1, numTable+1): # если без + 1 то будет с 1 до 15 // генерация скрипта для создания нужного количества таблиц
            self.listNameTable.append(nameTable + str(i))# сохраняем список таблиц из бд
            strSQLRequests = "CREATE TABLE IF NOT EXISTS " + nameTable + str(i) + " (" + self.genNameCol() +");"
            SQLRequests.append(strSQLRequests)

        for i in SQLRequests: # генерация таблиц 
            self.con.execute(i)
            
    def genNameCol(self): # генерим строку  
        strNameCol = "\n\t" + self.listNameCol[0] + " INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"# так как праймери кей(ПК) его вставляем отдельно в строку
        srtId_num_var = self.listNameCol.pop(0) # сохраняем название колонки ПК и удаляем из списка
        for count, nameCol in enumerate(self.listNameCol):# обрабатываем оставшийся список
            if count == len(self.listNameCol) - 1: # когда последняя строка  добавляем без запятой
                strNameCol += strNameCol + "\n\t" +nameCol  +" INTEGER"
            else:
                strNameCol += strNameCol + "\n\t" +nameCol  +" INTEGER," # вставляем названия всех колонок (генерим строку)
            
        self.listNameCol.insert(0, srtId_num_var) # возвращаем ПК в список
        print("strNameCol = ", strNameCol)
        return strNameCol
        

    def dropAllTables(self):# удаляем все таблицы если они существуют 
        while self.listNameTable:
            self.con.executescript('DROP TABLE IF EXISTS ' + self.listNameTable[-1]) #drop table if exists tab1
            self.listNameTable.pop()
    
    def dropTable(self, nameTable):# удаляем конкретную таблицу если она существует 
        self.con.executescript('DROP TABLE IF EXISTS ' + nameTable)  

    def insertStrInTable(self, nameTable = "VAR1", row = []): # вставка строки (в виде списка) в БД
        colName = self.con.executescript('PRAGMA table_info(' + nameTable + ');')
        print(colName)

        if nameTable == "" or nameTable or row:
            return


        # self.con.executescript('INSERT INTO IF EXISTS ' + nameTable + ' VALUES()')
        # #PRAGMA table_info(table_name)

        # self.con.commit()
            


# str = """
#         CREATE TABLE USER (
#             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             age INTEGER
#         );
#             """
# print(str)

# PRAGMA foreign_keys=on;
# CREATE TABLE books(
    # Id INTEGER PRIMARY KEY,
    # title TEXT NOT NULL,
    # count_page INTEGER NOT NULL CHECK (count_page >0),
    # price REAL CHECK (price >0),
    # auth_id INTEGER NOT NULL,
    # FOREIGN KEY (auth_id) REFERENCES auth(id)
# );
# CREATE TABLE auth(
    # id INTEGER PRIMARY KEY,
    # name TEXT NOT NULL,
    # age INTEGER  CHECK (age >16)
# );
if __name__ == "__main__":
    testBD = BDReadWrite()
    testBD.creatTable()
    testBD.insertStrInTable()

    testBD.dropAllTables()

