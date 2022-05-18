import numpy as np

from PyQt5.QtCore import QPointF

# функции для определения точек пересечения отрезков
def onSegment(p, q, r):
    if ( (q.x() <= max(p.x(), r.x())) and (q.x() >= min(p.x(), r.x())) and
           (q.y() <= max(p.y(), r.y())) and (q.y() >= min(p.y(), r.y()))):
        return True
    return False

def orientation(p, q, r):
    val = (float(q.y() - p.y()) * (r.x() - q.x())) - (float(q.x() - p.x()) * (r.y() - q.y()))
    if (val > 0):
        return 1
    elif (val < 0):
        return 2
    else:
        return 0
 
def doIntersect(p1,q1,p2,q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
 
    if ((o1 != o2) and (o3 != o4)):
        return True
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True
    return False

# функция для опредения координат точки пересечения 
# и проверки на то, не является ли точка пересечения лишь вершиной графа
def find_point_and_check(p1,q1,p2,q2):
    if (q1.y() - p1.y() != 0): 
        q = (q1.x() - p1.x()) / (p1.y() - q1.y());   
        sn = (p2.x() - q2.x()) + (p2.y() - q2.y()) * q 
        # if (not sn): 
        #     return False 
        fn = (p2.x() - p1.x()) + (p2.y() - p1.y()) * q 
        n = fn / sn
    else:
        # if (not(p2.y() - q2.y())): 
        #     return False 
        n = (p2.y() - p1.y()) / (p2.y() - q2.y()) 
    dot = (p2.x() + (q2.x() - p2.x()) * n, p2.y() + (q2.y() - p2.y()) * n ) # точка пересечения
    if (dot[0] != p1.x() and dot[0] != q1.x() and dot[0] != p2.x() and dot[0] != q2.x() and
        dot[1] != p1.y() and dot[1] != q1.y() and dot[1] != p2.y() and dot[1] != q2.y()):
        return True

# проверка первого задания
def checkTask1(Graph, CorrectAdjacencyMatrix):
    CountOfNodes = 0
    CurrentCountOfConnections = 0
    CorrectCountOfConnections = 0
    mistakes = [] # список ошибок:
                  #     1 - вершины слишком близко
                  #     2 - неверное количество вершин
                  #     3 - неверное количество связей
                  #     4 - неверные связи
                  #     5 - связи пересекаются

    do_intersect = False
    for i in range(len(Graph.Points)):
        # считаем число точек
        if (not np.isnan(Graph.Points[i][0])):
            CountOfNodes += 1

        # и заодно проверяем не находятся ли точки слишком близко
        if (not do_intersect):
            for j in range(len(Graph.Points)):
                if (j != i and (Graph.Points[j][0] + Graph.RadiusPoint >= Graph.Points[i][0] - Graph.RadiusPoint and 
                                Graph.Points[j][0] - Graph.RadiusPoint <= Graph.Points[i][0] + Graph.RadiusPoint and
                                Graph.Points[j][1] + Graph.RadiusPoint >= Graph.Points[i][1] - Graph.RadiusPoint and 
                                Graph.Points[j][1] - Graph.RadiusPoint <= Graph.Points[i][1] + Graph.RadiusPoint)):
                    mistakes.append(1)
                    do_intersect = True
                    break

    if (CountOfNodes != len(CorrectAdjacencyMatrix)):
        mistakes.append(2)

    # считаем число связей в графе студента
    for i in range(len(Graph.AdjacencyMatrix)):
        for j in range(len(Graph.AdjacencyMatrix[i])):
            if Graph.AdjacencyMatrix[i][j] == 1:
                CurrentCountOfConnections += 1

    # считаем число связей в правильном графе
    for i in range(len(CorrectAdjacencyMatrix)):
        for j in range(len(CorrectAdjacencyMatrix[i])):
            if CorrectAdjacencyMatrix[i][j] == 1:
                CorrectCountOfConnections += 1

    if CorrectCountOfConnections != CurrentCountOfConnections:
        mistakes.append(3)
        mistakes.append(4)
    elif (len(Graph.AdjacencyMatrix) == len(CorrectAdjacencyMatrix[i])):
        wrong_connections = False
        for i in range(len(Graph.AdjacencyMatrix)):
            for j in range(len(Graph.AdjacencyMatrix[i])):
                if Graph.AdjacencyMatrix[i][j] != CorrectAdjacencyMatrix[i][j]:
                    wrong_connections = True
                    mistakes.append(4)
                    break
            if (wrong_connections):
                break
    else:
        mistakes.append(4)

    # проверим на пересечение рёбер
    for i, row1 in enumerate(Graph.AdjacencyMatrix):
        for j, col1 in enumerate(row1):
            if col1 == 1:
                for k, row2 in enumerate(Graph.AdjacencyMatrix):
                    for l, col2 in enumerate(row2):
                        if col2 == 1:
                            p1 = QPointF(Graph.Points[i][0],Graph.Points[i][1])
                            q1 = QPointF(Graph.Points[j][0],Graph.Points[j][1])
                            p2 = QPointF(Graph.Points[k][0],Graph.Points[k][1])
                            q2 = QPointF(Graph.Points[l][0],Graph.Points[l][1])
                            if (((i, j) != (k, l)) and doIntersect(p1, q1, p2, q2) and find_point_and_check(p1, q1, p2, q2)):
                                mistakes.append(5)
                                return mistakes
    return mistakes