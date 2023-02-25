# s = '1'
# ex = 32

# ex = ex + int(s)

# l = (1, "rrtt")

# print(l)

######################################################3
from dto import DTO
from table_service import TableService

dto = DTO()
dto.variant = 55
dto.cipherOfWorks = ['1-2', '1-4', '3-4']
dto.performers = [1, 23, 3]
dto.numberOfPerformers = [1, 2, 3]
dto.duration = [13, 12, 1]
dto.numberOfDivision = [1, 2]
dto.numberOfPeople = [4, 33]

serv = TableService()
serv.createVariant(dto)
serv.readVariant(55)

dto.variant = 55
dto.cipherOfWorks = ['5-6', '7-8', '7-9']
dto.numberOfPeople = [76, 55]

serv.updateVariant(55, dto)
serv.readVariant(55)

serv.readAll()
serv.deleteAll()
serv.readAll()



#########################
###################################


# class Foo():
#     def __init__(self):
#         self.one = 0
#         self.two = []
# f = Foo()

# d = f.__dict__
# print(d)

# data = (12, [1, 2, 3], '1 2 3')

# d['two'] = data[2].split(' ')
# print(f.two)

# i = 0
# for key in d:

#     d[key] = data[i]
#     i = i + 1

# print(d)
# print(f.one, " ", f.two)
# print(type(data[2]))

# print(d[1])

# print(d[0] == int)

# print(d[1] == tuple)

# f = 'jjnjnnjnl54321'
# f = f[:-1]

# d = ['m', 'r', '']
# if d[-1] == '':
#     d = d[:-1]
# print(d)