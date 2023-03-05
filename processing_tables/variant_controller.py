from processing_tables.dto import DTO
from processing_tables.table_service import TableService
import re
import os

class VariantController():
    def __init__(self):
        self.tableService = TableService()

    def fileToDTO(self, response = 'variant_table_data.txt'):

        dto = DTO()
        dictionaryParametrs = dto.__dict__


        file = open(response,'r+')
        try:
            # работа с файлом
            listData = []
            lines = file.readlines()
            for line in lines:
                l = re.split(' |\n', line)
                try:
                    while True:
                        l.remove('')
                except:
                    pass

                listData.append(l)
            
            while len(listData) < len(dictionaryParametrs):
                listData.append([''])
                
            i = 0
            for key in dictionaryParametrs:
                if type(dictionaryParametrs[key]) == str:
                    dictionaryParametrs[key] = listData[i][0]
                elif type(dictionaryParametrs[key]) == list:
                    dictionaryParametrs[key] = listData[i]
                i = i + 1

        finally:
            file.close()

        try:
            os.remove(response)
            print(f'[INFO] FILE {response} DELETED')
        except:
            print(f'[WARN] TROUBLE WITH FILE {response}')
        
        return dto
    
    def DTOToFile(self, dto):
        dictionaryParametrs = dto.__dict__

        fileName = 'variant_dto_data.txt'
        f = open(fileName,'a+')
        try:
            # работа с файлом
            print('[INFO] OPEN FILE')
            # собираем матрицу данных
            listData = []
            maxLength = 0
            for key in dictionaryParametrs:
                if type(dictionaryParametrs[key]) == list:
                    listData.append(dictionaryParametrs[key])
                    if len(dictionaryParametrs[key]) > maxLength:
                        maxLength = len(dictionaryParametrs[key])

            # length = len(listData[0])

            for i in listData:
                while len(i) < maxLength:
                    i.append(-1)

            listCollInRow = [] 
            listCollInRow = list(map(list, zip(*listData)))
            for i in listCollInRow:
                try:
                    while True:
                        i.remove(-1)
                except:
                    pass

            for row in listCollInRow:
                f.write(' '.join([a for a in row]) + '\n')
            print('[INFO] SAVE TABLE IN FILE ----> Успешно')
        finally:
            f.close()
            print('[INFO] CLOSE FILE')
        return fileName

    def createVariant(self, response):
        dto = self.fileToDTO(response)
        self.tableService.createVariant(dto)

    def readVariant(self, response = 1):
        dto = self.tableService.readVariant(response)
        fileName = self.DTOToFile(dto)
        return fileName

    def updateVariant(self, response):
        dto = self.fileToDTO(response)
        self.tableService.updateVariant(dto)

    def deleteVariant(self, responce):
        self.tableService.deleteVariant(responce)

    def getAllNumberOfVariant(self):
        numberOfVariant = self.tableService.getAllNumberOfVariant()
        return numberOfVariant
        
