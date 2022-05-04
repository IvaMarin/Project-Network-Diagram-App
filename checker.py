from enum import Enum
import numpy as np

from PyQt5.QtWidgets import QMessageBox
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

class Mistake(Enum):
    SO_CLOSE = 1
    WRONG_COUNT_OF_NODES = 2
    WRONG_COUNT_OF_CONNECTIONS = 3

# checker
def check(Graph, CorrectAdjacencyMatrix):
    msg = QMessageBox()
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

    if len(Graph.AdjacencyMatrix) >= len(CorrectAdjacencyMatrix):
        for i in range(len(Graph.AdjacencyMatrix)):
            for j in range(len(Graph.AdjacencyMatrix[i])):
                if Graph.AdjacencyMatrix[i][j] == 1:
                    CorrectCountOfConnections += 1

    if (cnt != 0):
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Ошибка!")
        error_string += "Неверные связи.\n"
        correct = False
        msg.setInformativeText(error_string)
        msg.setWindowTitle("Результат")
        msg.exec_()

    # в случае если все проверки были пройдены, проверим на пересечение рёбер
    if (correct and no_warnings):
        do_intersect = False
        for i in correct_connections:
            for j in correct_connections:
                p1 = QPointF(self.points[i[0]][0].x(), self.points[i[0]][0].y())
                q1 = QPointF(self.points[i[1]][0].x(), self.points[i[1]][0].y())
                p2 = QPointF(self.points[j[0]][0].x(), self.points[j[0]][0].y())
                q2 = QPointF(self.points[j[1]][0].x(), self.points[j[1]][0].y())  
                if ((not do_intersect) and (j != i) and doIntersect(p1, q1, p2, q2) and find_point_and_check(p1, q1, p2, q2)):
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Внимание!")
                    msg.setInformativeText("Граф построен верно, но рёбра не должны пересекаться.")
                    msg.setWindowTitle("Результат")
                    msg.exec_()
                    do_intersect = True
                    correct = False
                    no_warnings = False
                    break
            if(do_intersect):
                break

    if (correct and no_warnings):
        msg.setIcon(QMessageBox.Information)
        msg.setText("Отлично!")
        msg.setInformativeText("Всё верно.")
        msg.setWindowTitle("Результат")
        msg.exec_()
