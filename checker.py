from enum import Enum
import numpy as np

from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QMessageBox, QLineEdit


class TaskOneMistakes(Enum):
    WRONG_VERTICES_AMOUNT = 2           # неверное количество вершин
    WRONG_CONNECTIONS_AMOUNT = 3        # неверное количество связей
    WRONG_CONNECTIONS = 4               # неверные связи
    INTERCETING_CONNECTIONS = 5         # связи пересекаются

class TaskTwoMistakes(Enum):
    WRONG_EARLY_DATES = 1               # неверные ранние сроки событий
    WRONG_LATE_DATES = 2                # неверные поздние сроки событий
    WRONG_DURATIONS = 3                 # неверные продолжительности работ
    WRONG_CRITICAL_PATHS = 4            # неверно указан критический путь

class TaskThreeAndFourMistakes(Enum):
    POINTS_ON_WRONG_TIME_POSITIONS = 1  # вершины не на нужных осях
    ARROWS_ON_WRONG_TIME_POSITIONS = 2  # стрелки не на нужных осях


# функции для определения пересечения отрезков
def onSegment(p, q, r):
    if ((q.x() <= max(p.x(), r.x())) and 
        (q.x() >= min(p.x(), r.x())) and
        (q.y() <= max(p.y(), r.y())) and 
        (q.y() >= min(p.y(), r.y()))):
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

def doIntersect(p1, q1, p2, q2):
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

# параметр EPS отвечает за чувствительность проверки
def IsPointOnSegment(a, p, b, EPS=0.1) -> bool:
    AB = np.sqrt((b.x() - a.x()) * (b.x() - a.x()) + (b.y()-a.y()) * (b.y() - a.y()))
    AP = np.sqrt((p.x() - a.x()) * (p.x() - a.x()) + (p.y()-a.y()) * (p.y() - a.y()))
    PB = np.sqrt((b.x() - p.x()) * (b.x() - p.x()) + (b.y()-p.y()) * (b.y() - p.y()))
    if np.abs(AB - (AP + PB)) < EPS:
        return True
    else:
        return False


def find_t_p(graph, n):
    early = np.zeros(n, int)
    early[0] = 0
    for i in range(1, n):
        max_t = 0
        for j in range(i):
            if (graph[i][j] != -1):
                cur_max_t = early[j] + graph[i][j]
                if (cur_max_t > max_t):
                    max_t = cur_max_t

        early[i] = max_t
    return early

def find_t_n(graph, early, n):
    late = np.zeros(n, float)
    late[n-1] = early[n-1]
    for i in range(n-2, -1, -1):
        min_t = np.inf

        for j in range(n-1, i, -1):
            if (graph[i][j] != -1):
                cur_min_t = late[j] - graph[i][j]
                if (cur_min_t < min_t):
                    min_t = cur_min_t
        if (min_t == np.inf):
            late[i] = early[i]
        else:
            late[i] = min_t
    return late

def find_R(reserve, early, late, n):
    reserve = np.zeros(n, int)
    for i in range(n):
        reserve[i] = late[i] - early[i]
    return reserve


def topological_sort(v):
    visited[v] = True

    for i in adj[v]:
        if (not visited[i[0]]):
            topological_sort(i[0])

    Stack.append(v)

def critical_path(s, n):
    dist = [-np.inf for _ in range(n)]

    for i in range(n):
        if (visited[i] == False):
            topological_sort(i)

    dist[s] = 0

    while (len(Stack) > 0):

        u = Stack[-1]
        del Stack[-1]

        if (dist[u] != np.inf):
            for i in adj[u]:
                if (dist[i[0]] < dist[u] + i[1]):
                    dist[i[0]] = dist[u] + i[1]
    return dist[n-1]


def find_all_paths(u, d, path):
    visited[u]= True
    path.append(u)

    if u == d:
        cp_path = path.copy()
        paths.append(cp_path)
    else:
        for i in adj[u]:
            if visited[i[0]] == False:
                find_all_paths(i[0], d, path)
    
    path.pop()
    visited[u]= False


def check_intersections(mistakes, mistake_id, Points, AdjacencyMatrix):
    # (i, j) - first edge
    for i, row1 in enumerate(AdjacencyMatrix):
        for j, col1 in enumerate(row1):
            # checks if connection exists
            if col1 >= 1: 
                # (k, l) - second edge
                for k, row2 in enumerate(AdjacencyMatrix):
                    for l, col2 in enumerate(row2):
                        # checks if connection exists
                        if col2 >= 1: 
                            if ((i, j) == (k, l)) or ((i, j) == (l, k)):
                                continue

                            # p1 -> q1
                            p1 = QPointF(Points[i][0], Points[i][1])
                            q1 = QPointF(Points[j][0], Points[j][1])
                            # p2 -> q2
                            p2 = QPointF(Points[k][0], Points[k][1])
                            q2 = QPointF(Points[l][0], Points[l][1])
                            
                            # q1 == q2
                            if (j == l):
                                if (IsPointOnSegment(p1, p2, q1) or IsPointOnSegment(p2, p1, q1)):
                                    mistakes.append(mistake_id)
                                    return mistakes
                            # p1 == p2
                            elif (i == k):
                                if (IsPointOnSegment(p1, q1, q2) or IsPointOnSegment(p1, q2, q1)):
                                    mistakes.append(mistake_id)
                                    return mistakes
                            # q1 == p2
                            elif (j == k):
                                if (IsPointOnSegment(p1, q2, q1) or IsPointOnSegment(q2, p1, q1)):
                                    mistakes.append(mistake_id)
                                    return mistakes
                            # q2 == p1
                            elif (i == l):
                                if (IsPointOnSegment(p2, q1, p1) or IsPointOnSegment(q1, p2, p1)):
                                    mistakes.append(mistake_id)
                                    return mistakes
                            
                            elif (doIntersect(p1, q1, p2, q2)):
                                mistakes.append(mistake_id)
                                return mistakes
    return mistakes

def check_connections(mistakes, mistake_id, AdjacencyMatrix, CorrectAdjacencyMatrix):
    if (len(AdjacencyMatrix) >= len(CorrectAdjacencyMatrix)):
        for i in range(len(CorrectAdjacencyMatrix)):
            for j in range(len(CorrectAdjacencyMatrix)):
                if ((AdjacencyMatrix[i][j] >= 1 and CorrectAdjacencyMatrix[i][j] == 0) or 
                    (AdjacencyMatrix[i][j] == 0 and CorrectAdjacencyMatrix[i][j] == 1)):
                    mistakes.append(mistake_id)
                    return mistakes
    else:
        mistakes.append(mistake_id)
        return mistakes

# проверка первого задания
def checkTask1(Graph, CorrectAdjacencyMatrix, ignore=False):
    CountOfNodes = 0
    CurrentCountOfConnections = 0
    CorrectCountOfConnections = 0
    mistakes = []  # список ошибок:

    if (not ignore):
        # проверяем не находятся ли точки слишком близко
        distancing_radius = Graph.RadiusPoint * 3
        for i in range(len(Graph.Points)):
            for j in range(len(Graph.Points)):
                if (j != i and (Graph.Points[j][0] + distancing_radius >= Graph.Points[i][0] - distancing_radius and
                                Graph.Points[j][0] - distancing_radius <= Graph.Points[i][0] + distancing_radius and
                                Graph.Points[j][1] + distancing_radius >= Graph.Points[i][1] - distancing_radius and
                                Graph.Points[j][1] - distancing_radius <= Graph.Points[i][1] + distancing_radius)):
                    warning = QMessageBox()
                    warning.setWindowTitle("Предупреждение")
                    warning.setText("Некоторые вершины находятся слишком близко друг к другу!")
                    warning.setIcon(QMessageBox.Warning)
                    warning.setStandardButtons(QMessageBox.Ok)
                    return warning

    # считаем число точек
    for i in range(len(Graph.Points)):
        if (not np.isnan(Graph.Points[i][0])):
            CountOfNodes += 1

    if (CountOfNodes != len(CorrectAdjacencyMatrix)):
        mistakes.append(TaskOneMistakes.WRONG_VERTICES_AMOUNT.value)

    # считаем число связей в графе студента
    for i in range(len(Graph.AdjacencyMatrix)):
        for j in range(len(Graph.AdjacencyMatrix[i])):
            if Graph.AdjacencyMatrix[i][j] >= 1:
                CurrentCountOfConnections += 1

    # считаем число связей в правильном графе
    for i in range(len(CorrectAdjacencyMatrix)):
        for j in range(len(CorrectAdjacencyMatrix[i])):
            if CorrectAdjacencyMatrix[i][j] == 1:
                CorrectCountOfConnections += 1

    if CorrectCountOfConnections != CurrentCountOfConnections:
        mistakes.append(TaskOneMistakes.WRONG_CONNECTIONS_AMOUNT.value)
        mistakes.append(TaskOneMistakes.WRONG_CONNECTIONS.value)
    else:
        check_connections(mistakes, TaskOneMistakes.WRONG_CONNECTIONS.value, Graph.AdjacencyMatrix, CorrectAdjacencyMatrix)

    # проверим на пересечение рёбер
    check_intersections(mistakes, TaskOneMistakes.INTERCETING_CONNECTIONS.value, Graph.Points, Graph.AdjacencyMatrix)
    
    return mistakes


# проверка второго задания
def checkTask2(Graph, Display):
    CorrectWeights = Graph.CorrectWeights
    CorrectAdjacencyMatrix = Graph.CorrectAdjacencyMatrix

    n = len(CorrectWeights)

    mistakes = []  # список ошибок:

    old_mistakes = []
    old_mistakes = checkTask1(Graph, CorrectAdjacencyMatrix, True)

    if (old_mistakes):
        warning = QMessageBox()
        warning.setWindowTitle("Предупреждение")
        warning.setText("Связи пересекаются!")
        warning.setIcon(QMessageBox.Warning)
        warning.setStandardButtons(QMessageBox.Ok)
        return warning

    early = find_t_p(CorrectWeights, n)
    late = find_t_n(CorrectWeights, early, n)
    # reserve = find_R(CorrectWeights, early, late, n)

    if (len(Graph.tp) == 0):
        mistakes.append(TaskTwoMistakes.WRONG_EARLY_DATES.value)
    else:
        for i in range(len(Graph.tp)):
            if (Graph.tp[i] != early[i]):
                mistakes.append(TaskTwoMistakes.WRONG_EARLY_DATES.value)
                break

    if (len(Graph.tn) == 0):
        mistakes.append(TaskTwoMistakes.WRONG_LATE_DATES.value)
    else:
        for i in range(len(Graph.tn)):
            if (Graph.tn[i] != late[i]):
                mistakes.append(TaskTwoMistakes.WRONG_LATE_DATES.value)
                break

    for i in range(n):
        for j in range(n):
            if (type(Display.QLineEdits[i][j]) == QLineEdit):
                try:
                    if (int(Display.QLineEdits[i][j].text()) != CorrectWeights[i][j]):
                        mistakes.append(TaskTwoMistakes.WRONG_DURATIONS.value)
                        mistakes.append(TaskTwoMistakes.WRONG_CRITICAL_PATHS.value)
                        return mistakes
                except ValueError:
                    warning = QMessageBox()
                    warning.setWindowTitle("Предупреждение")
                    warning.setText("Не введено значение продолжительности работы для одного или нескольких рёбер!")
                    warning.setIcon(QMessageBox.Warning)
                    warning.setStandardButtons(QMessageBox.Ok)
                    return warning
                
    
    # Критические Пути:
    # на первом шаге найдем правильное значение максимального пути в графе
    global Stack, visited, adj, paths

    Stack = []
    visited = [False]*(n)
    adj = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i, n):
            if (CorrectWeights[i][j] != -1):
                adj[i].append([j, CorrectWeights[i][j]])

    correct_max_distance = critical_path(0, n)
    
    # теперь найдем все пути в графе
    visited = [False]*(n)
    path = []
    paths = []
    
    find_all_paths(0, n-1, path)
    # и среди них выберем те, у которых длина равна максимальной
    critical_paths = []
    for p in paths:
        distance = 0
        i = 0
        while (p[i] != n-1):
            distance += CorrectWeights[p[i]][p[i+1]]
            i+=1
        if (distance == correct_max_distance):
            critical_paths.append(p)

    # на втором шаге найдем значение максимального пути пользователя
    Stack = []
    visited = [False]*(n)
    adj = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i, n):
            if (Graph.AdjacencyMatrix[i][j] == 2):
                adj[i].append([j, CorrectWeights[i][j]]) 

    max_distance = critical_path(0, n)

    # и найдем все пути от начала и до конца выбранные пользователем
    visited = [False]*(n)
    path = []
    paths = []
    
    find_all_paths(0, n-1, path)

    # на третьем шаге проверим совпадает ли значение максимального пути с верным
    if correct_max_distance != max_distance:
        mistakes.append(TaskTwoMistakes.WRONG_CRITICAL_PATHS.value)
    # и найдены ли все такие пути
    elif paths != critical_paths:
        mistakes.append(TaskTwoMistakes.WRONG_CRITICAL_PATHS.value)

    return mistakes


# проверка третьего задания
def checkTask3(Graph, CorrectWeights, GridBegin, GridStep):
    CorrectAdjacencyMatrix = Graph.CorrectAdjacencyMatrix
    Indent = 1

    n = len(CorrectWeights)

    mistakes = []  # список ошибок:

    old_mistakes = []
    old_mistakes = checkTask1(Graph, CorrectAdjacencyMatrix, True)

    if (old_mistakes):
        warning = QMessageBox()
        warning.setWindowTitle("Предупреждение")
        warning.setText("Связи пересекаются!")
        warning.setIcon(QMessageBox.Warning)
        warning.setStandardButtons(QMessageBox.Ok)
        return warning

    early = find_t_p(CorrectWeights, n)

    Graph.PointsTimeEarly = np.zeros(n, int)
    for i in range(n):
        Graph.PointsTimeEarly[i] = round((Graph.Points[i][0] - GridBegin) / GridStep) - Indent

    points_on_correct_axes = True
    for i in range(n):
        if (Graph.PointsTimeEarly[i] != early[i]):
            mistakes.append(TaskThreeAndFourMistakes.POINTS_ON_WRONG_TIME_POSITIONS.value)
            mistakes.append(TaskThreeAndFourMistakes.ARROWS_ON_WRONG_TIME_POSITIONS.value)
            points_on_correct_axes = False
            break

    Graph.ArrowPointsTimeEarly = np.zeros((n, n), int)
    for i in range(len(CorrectAdjacencyMatrix)):
        for j in range(len(CorrectAdjacencyMatrix)):
            if (CorrectAdjacencyMatrix[i][j] == 1):
                Graph.ArrowPointsTimeEarly[i][j] = round((Graph.ArrowPoints[i][j][0] - GridBegin) / GridStep) - Indent
            else:
                Graph.ArrowPointsTimeEarly[i][j] = -1

    if (points_on_correct_axes):
        for i in range(len(CorrectAdjacencyMatrix)):
            for j in range(len(CorrectAdjacencyMatrix)):
                if ((CorrectAdjacencyMatrix[i][j] == 1) and (Graph.ArrowPointsTimeEarly[i][j] != Graph.PointsTimeEarly[i] + CorrectWeights[i][j])):
                    mistakes.append(TaskThreeAndFourMistakes.ARROWS_ON_WRONG_TIME_POSITIONS.value)
                    return mistakes
    return mistakes


# проверка четвертого задания
def checkTask4(Graph, CorrectWeights, GridBegin, GridStep):
    CorrectAdjacencyMatrix = Graph.CorrectAdjacencyMatrix
    Indent = 1

    n = len(CorrectWeights)

    mistakes = []  # список ошибок:

    old_mistakes = []
    old_mistakes = checkTask1(Graph, CorrectAdjacencyMatrix, True)

    if (old_mistakes):
        warning = QMessageBox()
        warning.setWindowTitle("Предупреждение")
        warning.setText("Связи пересекаются!")
        warning.setIcon(QMessageBox.Warning)
        warning.setStandardButtons(QMessageBox.Ok)
        return warning

    early = find_t_p(CorrectWeights, n)
    late = find_t_n(CorrectWeights, early, n)

    Graph.PointsTimeLate = np.zeros(n, int)
    for i in range(n):
        Graph.PointsTimeLate[i] = round((Graph.Points[i][0] - GridBegin) / GridStep) - Indent

    points_on_correct_axes = True
    for i in range(n):
        if (Graph.PointsTimeLate[i] != late[i]):
            mistakes.append(TaskThreeAndFourMistakes.POINTS_ON_WRONG_TIME_POSITIONS.value)
            mistakes.append(TaskThreeAndFourMistakes.ARROWS_ON_WRONG_TIME_POSITIONS.value)
            points_on_correct_axes = False
            break

    Graph.ArrowPointsTimeLate = np.zeros((n, n), int)
    for i in range(len(CorrectAdjacencyMatrix)):
        for j in range(len(CorrectAdjacencyMatrix)):
            if (CorrectAdjacencyMatrix[i][j] == 1):
                Graph.ArrowPointsTimeLate[i][j] = round((Graph.ArrowPoints[i][j][0] - GridBegin) / GridStep) - Indent

    if (points_on_correct_axes):
        for i in range(len(CorrectAdjacencyMatrix)):
            for j in range(len(CorrectAdjacencyMatrix)):
                if ((CorrectAdjacencyMatrix[i][j] == 1) and (Graph.ArrowPointsTimeLate[i][j] != Graph.PointsTimeLate[j] - CorrectWeights[i][j])):
                    mistakes.append(TaskThreeAndFourMistakes.ARROWS_ON_WRONG_TIME_POSITIONS.value)
                    return mistakes
    return mistakes


def IsSubstring(word_list, text_list):
    word = "".join(str(i) for i in word_list)
    text = "".join(str(i) for i in text_list)
    return word in text

# проверка пятого задания
def checkTask5Part1(Graph, BaseGraph, Id) -> bool:
    is_correct = True
    
    CorrectPoints = set()
    CorrectAdjacencyMatrix = BaseGraph.CorrectSquadsWork.copy()
    for i in range(len(BaseGraph.CorrectSquadsWork)):
        for j in range(len(BaseGraph.CorrectSquadsWork)):
            if (BaseGraph.CorrectSquadsWork[i][j] == Id+1):
                CorrectAdjacencyMatrix[i][j] = 1
                CorrectPoints.add(i)
                CorrectPoints.add(j)
            else:
                CorrectAdjacencyMatrix[i][j] = 0
    CorrectPoints = list(CorrectPoints)

    Points = set()
    for (digit, id) in Graph.Points.keys():
        Points.add(digit)
    Points = list(Points)

    # события в отделении
    if (len(CorrectPoints) != len(Points)):
        is_correct = False
        return is_correct
    else:
        for i, digit in enumerate(Points):
            if (digit != CorrectPoints[i]):
                is_correct = False
                return is_correct

    AdjacencyMatrix = [([0] * len(CorrectAdjacencyMatrix)) for _ in range(len(CorrectAdjacencyMatrix))]
    for (digit1, id1), (digit2, id2) in Graph.AdjacencyList.items():
        AdjacencyMatrix[digit1][digit2] = 1 
    
    # работы в отделении
    mistakes = []
    mistake_id = 0
    check_connections(mistakes, mistake_id, AdjacencyMatrix, CorrectAdjacencyMatrix)

    if len(mistakes) > 0:
        is_correct = False
        return is_correct

    for i, s1 in enumerate(Graph.Sequences):
        for j, s2 in enumerate(Graph.Sequences):
            if (i != j) and IsSubstring(s1, s2):
                is_correct = False
                return is_correct

    return is_correct

def checkTask5Part2(Graph, BaseGraph, CorrectWeights, GridBegin, GridStep, Id) -> bool:
    is_correct = True

    Indent = 1
    n = len(CorrectWeights)
    early = find_t_p(CorrectWeights, n)

    CorrectPoints = set()
    CorrectAdjacencyMatrix = BaseGraph.CorrectSquadsWork.copy()
    for i in range(len(BaseGraph.CorrectSquadsWork)):
        for j in range(len(BaseGraph.CorrectSquadsWork)):
            if (BaseGraph.CorrectSquadsWork[i][j] == Id+1):
                CorrectAdjacencyMatrix[i][j] = 1
                CorrectPoints.add(i)
                CorrectPoints.add(j)
            else:
                CorrectAdjacencyMatrix[i][j] = 0
    CorrectPoints = list(CorrectPoints)

    Points = set()
    for (digit, id) in Graph.Points.keys():
        Points.add(digit)
    Points = list(Points)

    Graph.PointsTimeEarly = np.zeros(n, int)
    for digit in Points:
        for p in Graph.Points.keys():
            if p[0] == digit:
                (x, y) = Graph.Points[p]
                Graph.PointsTimeEarly[digit] = round((x - GridBegin) / GridStep) - Indent
                break
        
    # Расположение событий на временной оси
    for i in range(n):
        if (i in CorrectPoints) and (Graph.PointsTimeEarly[i] != early[i]):
            is_correct = False
            return is_correct

    Graph.ArrowPointsTime = np.zeros((n, n), int)
    for (digit1, id1), (digit2, id2) in Graph.AdjacencyList.items():
            (x, y) = Graph.Arrows[((digit1, id1), (digit2, id2))]
            if (CorrectAdjacencyMatrix[digit1][digit2] == 1):
                Graph.ArrowPointsTime[digit1][digit2] = round((x - GridBegin) / GridStep) - Indent
            else:
                Graph.ArrowPointsTime[i][j] = -1

    # Промежутки времени у работ
    for i in range(len(CorrectAdjacencyMatrix)):
        for j in range(len(CorrectAdjacencyMatrix)):
            if (CorrectAdjacencyMatrix[i][j] == 1):
                if (len(BaseGraph.R) > i) and (BaseGraph.R[i] > 0): # ранние сроки
                    if Graph.ArrowPointsTime[i][j] != (Graph.PointsTimeEarly[i] + CorrectWeights[i][j]):
                        is_correct = False
                        return is_correct
                else: # поздние сроки
                    if Graph.ArrowPointsTime[i][j] != (Graph.PointsTimeEarly[j] - CorrectWeights[i][j]):
                        is_correct = False
                        return is_correct
            
    return is_correct

def checkTask5Part3(BaseGraph, CorrectWeights, Display, Id) -> bool:
    is_correct = True

    CorrectAdjacencyMatrix = BaseGraph.CorrectSquadsWork.copy()
    for i in range(len(BaseGraph.CorrectSquadsWork)):
        for j in range(len(BaseGraph.CorrectSquadsWork)):
            if (BaseGraph.CorrectSquadsWork[i][j] == Id+1):
                CorrectAdjacencyMatrix[i][j] = 1
            else:
                CorrectAdjacencyMatrix[i][j] = 0
    
    # Численность в отделении
    for k, v in Display.QLineEdits.items():
        i = k[0][0]
        j = k[1][0]
        if (CorrectAdjacencyMatrix[i][j] == 1):
            try:
                if (int(v.text()) != CorrectWeights[i][j]):
                    is_correct = False
                    return is_correct
            except ValueError:
                warning = QMessageBox()
                warning.setWindowTitle("Предупреждение")
                warning.setText("Не введено значение числа людей, выполняющих работу, для одного или нескольких рёбер!")
                warning.setIcon(QMessageBox.Warning)
                warning.setStandardButtons(QMessageBox.Ok)
                return warning
    
    return is_correct