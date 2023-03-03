from processing_tables.dto import DTO

class Mapper():
    def __init__(self):
        # маппа всех полей класса
        self.dictionaryParametrs = None

    def dtoToString(self, dto):
        self.dictionaryParametrs = dto.__dict__
        listData = []
        parametr = None
        print("IN")
        for key in self.dictionaryParametrs:
            
            if type(self.dictionaryParametrs[key]) == str:
                # обработка int поля
                parametr = self.dictionaryParametrs[key]
            elif type(self.dictionaryParametrs[key]) == list:
                # обработка tuple поля
                parametr = ''
                for i in self.dictionaryParametrs[key]:
                    parametr = parametr + str(i) + ' '
                if parametr[-1] == ' ':
                    parametr = parametr[:-1]

            listData.append(parametr)

        return listData
    
    def stringToDto(self, listData):
        dto = DTO()
        self.dictionaryParametrs = dto.__dict__

        i = 0
        for key in self.dictionaryParametrs:

            if type(self.dictionaryParametrs[key]) == str:
                self.dictionaryParametrs[key] = listData[i]
            elif type(self.dictionaryParametrs[key]) == list:
                self.dictionaryParametrs[key] = listData[i].split(' ')
                if self.dictionaryParametrs[key][-1] == '':
                    self.dictionaryParametrs[key] = self.dictionaryParametrs[key][:-1]
                
            i = i + 1

        return dto