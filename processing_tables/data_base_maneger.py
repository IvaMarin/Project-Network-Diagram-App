import sqlite3

class DataBaseManager(object):
    # инициализация базы данных
    def __init__(self, database):
        self.connect = sqlite3.connect(database)
        # создание таблицы (вызывается 1 раз, дальше комментируется)
        # self.connect.execute(''' CREATE TABLE variants (
        #     variant INT,
        #     cipher_of_works text,
        #     performers text,
        #     number_of_performers text,
        #     duration text,
        #     number_of_division text,
        #     number_of_people text
        #     )
        # ''')
        # self.connect.commit()
        self.cursor = self.connect.cursor()

    # произвольный запрос
    def query(self, arg):
        self.cursor.execute(arg)
        self.connect.commit()
        return self.cursor
    
    # закрытие
    def __del__(self):
        self.connect.close()
    
    #########################
    # ЗАПРОСЫ К БАЗЕ ДАННЫХ #
    #########################
    # создание новой записи варианта
    def createVariant(self, args):
        sql = '''INSERT INTO variants 
            (variant, cipher_of_works, performers, number_of_performers, duration, number_of_division, number_of_people)
            values(?, ?, ?, ?, ?, ?, ?);'''
        self.cursor.execute(sql, args)
        self.connect.commit()

    # выборка данных из таблицы варианта
    def readVariant(self, arg):
        sql = 'SELECT * FROM variants WHERE variant = ' + str(arg) + ';'
        self.cursor.execute(sql)
        variant = self.cursor.fetchone()
        return variant
    
    # обновление информации в таблице варианта
    def updateVariant(self, arg, args):
        # sql = 'UPDATE variants SET (variant, cipher_of_works, performers, number_of_performers, duration, number_of_division, number_of_people) VALUES (?, ?, ?, ?, ?, ?, ?) WHERE variant = ' + str(arg) + ';'
        # self.cursor.execute(sql, args)
        # self.connect.commit()
        self.deleteVariant(arg)
        self.createVariant(args)

    # удаление таблицы варианта
    def deleteVariant(self, arg):
        sql = 'DELETE FROM variants WHERE variant = ' + str(arg) + ';'
        self.cursor.execute(sql)
        self.connect.commit()

    # получить все записи
    def readAll(self):
        sql = 'SELECT * FROM variants;'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data


    # удалить все записи
    def deleteAll(self):
        sql = 'DELETE FROM variants;'
        self.cursor.execute(sql)
        self.connect.commit()
        




