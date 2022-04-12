# Model составляющая MVC (Граф)
# (?) - излишний функционал
# "несуществющие вершины" - вершины в середине списка индексов вершин, которые были удалены (далее без ковычек)
import numpy as np


# класс "граф"
class Graph:
    # конструктор графа; параметры: радиус вершины
    def __init__(self, RadiusPoint):
        # математические характеристики графа
        self.AmountPoints = 0  # число вершин (?)
        self.PointsIsVisible = np.array(object=[], dtype=int)  # массив значений существующих вершин
        self.ConnectedPoints = np.array(object=[], dtype=int)  # массив индексов связанных вершин

        # графические характеристики графа
        self.RadiusPoint = RadiusPoint  # радиус вершины
        self.CoordCentrePoint = np.array(object=[], dtype=list)  # массив координат центров вершин графа

    # добавить вершину; параметры: координата х, координата у
    def AddPoint(self, x, y):
        # для каждой вершины (вне зависимости от существования)
        for i in range(self.PointsIsVisible):
            # если вершина не существует
            if self.PointsIsVisible[i] == False:
                self.PointsIsVisible[i] = True  # сделать вершину существующей
                self.CoordCentrePoint[i][0] = x  # добавить координату х центра вершины графа
                self.CoordCentrePoint[i][1] = y  # добавить координату y центра вершины графа
                self.AmountPoints += 1  # инкрементировать количество вершин (?)
                return
        # если не было не существующей вершины
        self.PointsIsVisible = np.append(True)
        self.CoordCentrePoint = np.append([x, y])  # добавить координаты центра вершины графа
        self.AmountPoints += 1  # инкрементировать количество вершин (?)

    # находится ли курсор на вершине; параметры: координата курсора х, координата курсора у
    # вернуть -1, если курсор ни на одной вершине
    # вернуть номер вершины, на которой находится курсор
    def IsCursorOnPoint(self, x, y):
        # по каждой паре координат центра вершины
        for i in range(self.CoordCentrePoint):
            # если нашлась пара координат центра вершины, в окрестности радиуса вершины которой попал курсор
            if ((x >= self.CoordCentrePoint[i][0] - self.RadiusPoint and x <= self.CoordCentrePoint[i][
                0] + self.RadiusPoint) or
                    (y >= self.CoordCentrePoint[i][1] - self.RadiusPoint and y <= self.CoordCentrePoint[i][
                        1] + self.RadiusPoint)):
                return i  # вернуть индекс вершины, в которую попал курсор
        return -1  # вернуть -1, если не нашлась такая пара координат

    # удалить вершину; параметры: индекс удаляемой вершины
    def DeletePoint(self, index):
        # если курсор не наведен на вершину
        if index == -1:
            return  # ничего не делать
        self.PointIsVisible[index] = False
        self.AmountPoints -= 1  # декрементировать количество вершин (?)
        indexDeletedElements = []  # список удаляемых индексов
        # итерироваться по парам связанных вершин
        for i in range(0, self.ConnectedPoints, 2):
            # если следующий индекс не выходит за рамки массива
            if i + 1 < len(self.ConnectedPoints):
                # если в паре есть удаляемая вершина
                if self.ConnectedPoints[i] == index or self.ConnectedPoints[i + 1] == index:
                    # добавить индексы удаляемых элементов
                    indexDeletedElements.append([i, i + 1])
            # иначе, если следующий индекс выходит за рамки массива
            else:
                if self.ConnectedPoints[i] == index:
                    # добавить индекс удаляемого элемента
                    indexDeletedElements.append([i])
        self.ConnectedPoints = np.delete(self.ConnectedPoints, indexDeletedElements)  # удалить все выделенные элементы

    # связать вершины; параметры: индекс вершины
    def ConnectPoints(self, index):
        # если курсор не наведен на вершину
        if index == -1:
            return  # ничего не делать
        self.ConnectedPoints = np.append(self.ConnectedPoints, index)  # добавить связываемую вершину
        # если число связанных вершин четное
        if len(self.ConnectedPoints) % 2 == 0:
            # обойти массив связанных вершин с шагом 2
            for i in range(0, len(self.ConnectedPoints), 2):
                # найдена точная пара
                if self.ConnectedPoints[i] == self.ConnectedPoints[-2] and self.ConnectedPoints[i + 1] == \
                        self.ConnectedPoints[-1]:
                    # удалить последнюю пару
                    self.ConnectedPoints = np.delete(self.ConnectedPoints, -2)
                    self.ConnectedPoints = np.delete(self.ConnectedPoints, -1)
                    break

    # удалить связь между вершинами; параметры: индекс первой вершины, индекс второй вершины
    def DeleteConnection(self, firstIndex, secondIndex):
        # если курсор не наведен хотя бы на одну из вершин
        if firstIndex == -1 or secondIndex == -1:
            return  # ничего не делать
        # итерироваться по парам связанных вершин
        for i in range(0, self.ConnectedPoints, 2):
            # если следующий индекс не выходит за рамки массива
            if i + 1 < len(self.ConnectedPoints):
                # если в паре есть удаляемые вершины
                if self.ConnectedPoints[i] == firstIndex and self.ConnectedPoints[i + 1] == secondIndex:
                    # удалить пару элементов
                    indexDeletedElements = np.delete(indexDeletedElements, i)
                    indexDeletedElements = np.delete(indexDeletedElements, i)
                    break

    # переместить вершиеу; параметры: номер вершины, координата х, координата y
    def MovePoint(self, index, x, y):
        # если курсор не наведен на вершину
        if index == -1:
            return  # ничего не делать
        # присовить новые значения координат центра вершины
        self.CoordCentrePoint[index][0] = x
        self.CoordCentrePoint[index][1] = y
