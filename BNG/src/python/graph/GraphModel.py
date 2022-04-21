# Model составляющая MVC (Граф)
# (?) - излишний функционал
# "несуществющие вершины" - вершины в середине списка индексов вершин, которые были удалены (далее без ковычек)
import numpy as np


# класс "граф"
from PyQt5.QtCore import QPointF


class Graph:
    # конструктор графа; параметры: радиус вершины
    def __init__(self, RadiusPoint):
        # математические характеристики графа
        self.AmountPoints = 0  # число вершин (?)
        self.PointsIsVisible = np.array(object=[], dtype=bool)  # массив значений существующих вершин
        self.ConnectedPoints = np.array(object=[], dtype=int)  # массив индексов связанных вершин
        self.deleteConnection = []

        # графические характеристики графа
        self.RadiusPoint = RadiusPoint  # радиус вершины
        self.CoordCentrePoint = np.array(object=[], dtype=list)  # массив координат центров вершин графа

    # добавить вершину; параметры: координата х, координата у

    def AddPoint(self, x, y, event):
        # для каждой вершины (вне зависимости от существования)
        for i in range(len(self.PointsIsVisible)):
            # если вершина не существует
            if self.PointsIsVisible[i] == False:
                self.PointsIsVisible[i] = True  # сделать вершину существующей
                self.CoordCentrePoint[i].setX(x)  # добавить координату х центра вершины графа
                self.CoordCentrePoint[i].setY(y)  # добавить координату y центра вершины графа
                self.AmountPoints += 1  # инкрементировать количество вершин (?)
                return
        # если не было не существующей вершины
        self.PointsIsVisible = np.append(self.PointsIsVisible, True)
        self.CoordCentrePoint = np.append(self.CoordCentrePoint, QPointF)  # добавить координаты центра вершины графа
        self.CoordCentrePoint[self.AmountPoints] = event.pos()
        self.AmountPoints += 1  # инкрементировать количество вершин (?)

    # находится ли курсор на вершине; параметры: координата курсора х, координата курсора у
    # вернуть -1, если курсор ни на одной вершине
    # вернуть номер вершины, на которой находится курсор
    # все ок тут!
    def IsCursorOnPoint(self, x, y):
        # по каждой паре координат центра вершины
        for i in range(len(self.CoordCentrePoint)):
            # если нашлась пара координат центра вершины, в окрестности радиуса вершины которой попал курсор
            if ((x >= self.CoordCentrePoint[i].x() - self.RadiusPoint and x <= self.CoordCentrePoint[i].x() + self.RadiusPoint) and
                    (y >= self.CoordCentrePoint[i].y() - self.RadiusPoint and y <= self.CoordCentrePoint[i].y() + self.RadiusPoint)):
                return i  # вернуть индекс вершины, в которую попал курсор
        return -1  # вернуть -1, если не нашлась такая пара координат

    # удалить вершину; параметры: индекс удаляемой вершины
    def DeletePoint(self, index):
        # если курсор не наведен на вершину
        if index == -1:
            return  # ничего не делать
        self.PointsIsVisible[index] = False
        self.AmountPoints -= 1  # декрементировать количество вершин (?)
        indexDeletedElements = []  # список удаляемых индексов
        # итерироваться по парам связанных вершин
        for i in range(0, len(self.ConnectedPoints), 2):
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
    # РАБОТАЕТ, НО ПОПРАВИТЬ КОСТЫЛИ
    def ConnectPoints(self, index):
        # если курсор не наведен на вершину
        if index == -1 or (len(self.ConnectedPoints) > 2 and index == self.ConnectedPoints[-1] and len(self.ConnectedPoints) % 2 == 1):
            return  # ничего не делать
        # добавляем индекс вершины в массив связей
        self.ConnectedPoints = np.append(self.ConnectedPoints, index)  # добавить связываемую вершину
        # print(self.ConnectedPoints)
        # если число связанных вершин четное
        print("Connection: ", self.ConnectedPoints)
        if len(self.ConnectedPoints) % 2 == 0:
            # обойти массив связанных вершин с шагом 2
            for i in range(0, len(self.ConnectedPoints) - 2, 2):
                # найдена точная пара
                # почему тут удаляет вершины в любом случае, сделать проход цикла до 2ух последних элементов
                if self.ConnectedPoints[i] == self.ConnectedPoints[-2] and self.ConnectedPoints[i + 1] == self.ConnectedPoints[-1] and len(self.ConnectedPoints) > 2:
                    # удалить последнюю пару
                    self.ConnectedPoints = np.delete(self.ConnectedPoints, -2)
                    self.ConnectedPoints = np.delete(self.ConnectedPoints, -1)
                    break



    # удалить связь между вершинами; параметры: индекс первой вершины, индекс второй вершины
    def DeleteConnection(self, index):

        # если курсор не наведен хотя бы на одну из вершин
        if index == -1:
            return  # ничего не делать

        self.deleteConnection.append(index)
        if len(self.deleteConnection) == 2:
            # итерироваться по парам связанных вершин
            for i in range(0, len(self.ConnectedPoints), 2):
                # если следующий индекс не выходит за рамки массива
                if i + 1 < len(self.ConnectedPoints):
                    # если в паре есть удаляемые вершины
                    if self.ConnectedPoints[i] == self.deleteConnection[0] and self.ConnectedPoints[i + 1] == self.deleteConnection[1]:
                        # удалить пару элементов
                        self.ConnectedPoints = np.delete(self.ConnectedPoints, i)
                        self.ConnectedPoints = np.delete(self.ConnectedPoints, i)
                        break
            self.deleteConnection.clear()


    # переместить вершиеу; параметры: номер вершины, координата х, координата y
    def MovePoint(self, index, x, y):
        # если курсор не наведен на вершину
        if index == -1:
            return  # ничего не делать
        # присовить новые значения координат центра вершины
        self.CoordCentrePoint[index].setX(x)
        self.CoordCentrePoint[index].setY(y)
