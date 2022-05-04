from enum import Enum
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
# и проверки на то ,что точка пересечения не является лишь вершиной графа
def find_point_and_check(p1,q1,p2,q2):
    if (q1.y() - p1.y() != 0): 
        q = (q1.x() - p1.x()) / (p1.y() - q1.y());   
        sn = (p2.x() - q2.x()) + (p2.y() - q2.y()) * q 
        if (not sn): 
            return False 
        fn = (p2.x() - p1.x()) + (p2.y() - p1.y()) * q 
        n = fn / sn
    else:
        if (not(p2.y() - q2.y())): 
            return False 
        n = (p2.y() - p1.y()) / (p2.y() - q2.y()) 
    dot = (p2.x() + (q2.x() - p2.x()) * n, p2.y() + (q2.y() - p2.y()) * n ) # точка пересечения
    if (dot[0] != p1.x() and dot[0] != q1.x() and dot[0] != p2.x() and dot[0] != q2.x() and
        dot[1] != p1.y() and dot[1] != q1.y() and dot[1] != p2.y() and dot[1] != q2.y()):
        return True

# SO_CLOSE - вершины слишком близко
# WRONG_COUNT_OF_NODES - неверное количество вершин
# WRONG_COUNT_OF_CONNECTIONS - неверное количество связей
# WRONG_CONNECTIONS - неверные связи
# EDGES_INTERSECT - связи пересекаются
class Mistake(Enum):
    SO_CLOSE = 1
    WRONG_COUNT_OF_NODES = 2
    WRONG_COUNT_OF_CONNECTIONS = 3
    WRONG_CONNECTIONS = 4
    EDGES_INTERSECT = 5

# checker
def checkTask1(Graph, CorrectAdjacencyMatrix):
    do_intersect = False
    correct = True
    no_warnings = True
    CountOfNodes = 0
    CurrentCountOfConnections = 0
    CorrectCountOfConnections = 0
    mistakes = np.empty((0)) # массив ошибок
    for i in range(len(Graph.Points)):
        # считаем число точек
        if (Graph.Points[i][0] != None):
            CountOfNodes += 1
        # и заодно проверяем не находятся ли точки слишком близко
        for j in range(len(Graph.Points)):
            if ((not do_intersect) and j != i and (Graph.Points[j][0] + Graph.RadiusPoint >= Graph.Points[i][0] - Graph.RadiusPoint and 
                                                   Graph.Points[j][0] - Graph.RadiusPoint <= Graph.Points[i][0] + Graph.RadiusPoint and
                                                   Graph.Points[j][1] + Graph.RadiusPoint >= Graph.Points[i][1] - Graph.RadiusPoint and 
                                                   Graph.Points[j][1] - Graph.RadiusPoint <= Graph.Points[i][1] + Graph.RadiusPoint)):
                mistakes = np.append(mistakes, Mistake(1))
                break

    if (CountOfNodes != len(CorrectAdjacencyMatrix)):
        mistakes = np.append(mistakes, Mistake(2))

    # считаем число связей в графе студента
    for i in range(len(Graph.AdjacencyMatrix)):
        for j in range(len(Graph.AdjacencyMatrix[i])):
            if Graph.AdjacencyMatrix[i][j] == 1:
                CurrentCountOfConnections += 1

    # считаем число связей в правильном графе
    for i in range(len(Graph.AdjacencyMatrix)):
        for j in range(len(Graph.AdjacencyMatrix[i])):
            if Graph.AdjacencyMatrix[i][j] == 1:
                CorrectCountOfConnections += 1

    if CorrectCountOfConnections != CurrentCountOfConnections:
        mistakes = np.append(mistakes, Mistake(3))

    if len(Graph.AdjacencyMatrix) <= len(CorrectAdjacencyMatrix):
        for i in range(len(Graph.AdjacencyMatrix)):
            for j in range(len(Graph.AdjacencyMatrix[i])):
                if Graph.AdjacencyMatrix[i][j] != CorrectAdjacencyMatrix[i][j]:
                    mistakes = np.append(mistakes, Mistake(4))
                    break
    else:
        for i in range(len(CorrectAdjacencyMatrix)):
            for j in range(len(CorrectAdjacencyMatrix)):
                if Graph.AdjacencyMatrix[i][j] != CorrectAdjacencyMatrix[i][j]:
                    mistakes = np.append(mistakes, Mistake(4))
                    break

    # в случае если все проверки были пройдены, проверим на пересечение рёбер
    if (len(mistakes) == 0):
        do_intersect = False
        for r1 in CorrectAdjacencyMatrix:
            for c1 in CorrectAdjacencyMatrix:
                for r2 in CorrectAdjacencyMatrix:
                    for c2 in CorrectAdjacencyMatrix:
                        p1 = QPointF(Graph.Points[r1][0],Graph.Points[r1][1])
                        q1 = QPointF(Graph.Points[c1][0],Graph.Points[c1][1])
                        p2 = QPointF(Graph.Points[r2][0],Graph.Points[r2][1])
                        q2 = QPointF(Graph.Points[c2][0],Graph.Points[c2][1])
                        if ((not do_intersect) and (j != i) and doIntersect(p1, q1, p2, q2) and find_point_and_check(p1, q1, p2, q2)):
                            mistakes = np.append(mistakes, Mistake(5))
                            do_intersect = True
                            correct = False
                            no_warnings = False
                            break
                if(do_intersect):
                    break
