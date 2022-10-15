import numpy as np

from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QMessageBox, QLineEdit


# функции для определения точек пересечения отрезков
def onSegment(p, q, r):
    if ((q.x() <= max(p.x(), r.x())) and (q.x() >= min(p.x(), r.x())) and
            (q.y() <= max(p.y(), r.y())) and (q.y() >= min(p.y(), r.y()))):
        return True
    return False


def orientation(p, q, r):
    val = (float(q.y() - p.y()) * (r.x() - q.x())) - \
        (float(q.x() - p.x()) * (r.y() - q.y()))
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


# функция для опредения координат точки пересечения
# и проверки на то, не является ли точка пересечения лишь вершиной графа
def find_point_and_check(p1, q1, p2, q2):
    if (q1.y() - p1.y() != 0):
        q = (q1.x() - p1.x()) / (p1.y() - q1.y())
        sn = (p2.x() - q2.x()) + (p2.y() - q2.y()) * q
        # if (not sn):
        #     return False
        fn = (p2.x() - p1.x()) + (p2.y() - p1.y()) * q
        if (sn == 0):
            n = 0
        else:
            n = fn / sn
    else:
        # if (not(p2.y() - q2.y())):
        #     return False
        n = (p2.y() - p1.y()) / (p2.y() - q2.y())
    dot = (p2.x() + (q2.x() - p2.x()) * n, p2.y() +
           (q2.y() - p2.y()) * n)  # точка пересечения
    if (dot[0] != p1.x() and dot[0] != q1.x() and dot[0] != p2.x() and dot[0] != q2.x() and
            dot[1] != p1.y() and dot[1] != q1.y() and dot[1] != p2.y() and dot[1] != q2.y()):
        return True


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
  

# проверка первого задания
def checkTask1(Graph, CorrectAdjacencyMatrix, ignore=False):
    CountOfNodes = 0
    CurrentCountOfConnections = 0
    CorrectCountOfConnections = 0
    mistakes = []  # список ошибок:
    #                   2 - неверное количество вершин
    #                   3 - неверное количество связей
    #                   4 - неверные связи
    #                   5 - связи пересекаются

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
        mistakes.append(2)

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
        mistakes.append(3)
        mistakes.append(4)
    elif (len(Graph.AdjacencyMatrix) >= len(CorrectAdjacencyMatrix[i])):
        wrong_connections = False
        for i in range(len(CorrectAdjacencyMatrix)):
            for j in range(len(CorrectAdjacencyMatrix)):
                if ((Graph.AdjacencyMatrix[i][j] >= 1 and CorrectAdjacencyMatrix[i][j] == 0) or 
                    (Graph.AdjacencyMatrix[i][j] == 0 and CorrectAdjacencyMatrix[i][j] == 1)):
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
            if col1 >= 1:
                for k, row2 in enumerate(Graph.AdjacencyMatrix):
                    for l, col2 in enumerate(row2):
                        if col2 >= 1:
                            p1 = QPointF(
                                Graph.Points[i][0], Graph.Points[i][1])
                            q1 = QPointF(
                                Graph.Points[j][0], Graph.Points[j][1])
                            p2 = QPointF(
                                Graph.Points[k][0], Graph.Points[k][1])
                            q2 = QPointF(
                                Graph.Points[l][0], Graph.Points[l][1])
                            if (((i, j) != (k, l)) and ((i, j) != (l, k)) and doIntersect(p1, q1, p2, q2) and find_point_and_check(p1, q1, p2, q2)):
                                mistakes.append(5)
                                return mistakes
    return mistakes


# проверка второго задания
def checkTask2(Graph):
    CorrectWeights = Graph.CorrectWeights
    CorrectAdjacencyMatrix = Graph.CorrectAdjacencyMatrix

    # CorrectWeights = np.array([[-1, 1, -1, -1],
    #                            [1, -1, 2, -1],
    #                            [-1, 2, -1, 3],
    #                            [-1, -1, 3, -1]])
    # CorrectAdjacencyMatrix = np.array([[0, 1, 0, 0],
    #                                    [0, 0, 1, 0],
    #                                    [0, 0, 0, 1],
    #                                    [0, 0, 0, 0]])

    n = len(CorrectWeights)

    mistakes = []  # список ошибок:
    #                   1 - верные ранние сроки событий
    #                   2 - верные поздние сроки событий
    #                   3 - верные продолжительности работ
    #                   4 - верно указан критический путь

    old_mistakes = []
    old_mistakes = checkTask1(Graph, CorrectAdjacencyMatrix, True)

    if (old_mistakes):
        warning = QMessageBox()
        warning.setWindowTitle("Предупреждение")
        warning.setText("Нарушено одно из условий проверки первого задания! Пожалуйста, проверьте каждое из условий:\n1. Верное количество вершин\n2. Верное количество связей\n3. Верные связи\n4. Связи не пересекаются")
        warning.setIcon(QMessageBox.Warning)
        warning.setStandardButtons(QMessageBox.Ok)
        return warning

    early = find_t_p(CorrectWeights, n)
    late = find_t_n(CorrectWeights, early, n)
    # reserve = find_R(CorrectWeights, early, late, n)

    for i in range(len(Graph.tp)):
        if (Graph.tp[i] != early[i]):
            mistakes.append(1)
            break

    for i in range(len(Graph.tn)):
        if (Graph.tn[i] != late[i]):
            mistakes.append(2)
            break

    for i in range(n):
        for j in range(n):
            if (type(Graph.label[i][j]) == QLineEdit):
                try:
                    if (int(Graph.label[i][j].text()) != CorrectWeights[i][j]):
                        mistakes.append(3)
                        mistakes.append(4)
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
        mistakes.append(4)
    # и найдены ли все такие пути
    elif paths != critical_paths:
        mistakes.append(4)

    return mistakes


# проверка третьего задания
def checkTask3(Graph, CorrectWeights, GridBegin, GridStep):
    CorrectAdjacencyMatrix = Graph.CorrectAdjacencyMatrix

    # CorrectWeights = np.array([[-1, 1, -1, -1],
    #                            [1, -1, 2, -1],
    #                            [-1, 2, -1, 3],
    #                            [-1, -1, 3, -1]])
    # CorrectAdjacencyMatrix = np.array([[0, 1, 0, 0],
    #                                    [0, 0, 1, 0],
    #                                    [0, 0, 0, 1],
    #                                    [0, 0, 0, 0]])

    n = len(CorrectWeights)

    mistakes = []  # список ошибок:
    #                   1 - вершины не на нужных осях
    #                   2 - стрелки не на нужных осях

    old_mistakes = []
    old_mistakes = checkTask1(Graph, CorrectAdjacencyMatrix, True)

    if (old_mistakes):
        warning = QMessageBox()
        warning.setWindowTitle("Предупреждение")
        warning.setText("Нарушено одно из условий проверки первого задания! Пожалуйста, проверьте каждое из условий:\n1. Верное количество вершин\n2. Верное количество связей\n3. Верные связи\n4. Связи не пересекаются")
        warning.setIcon(QMessageBox.Warning)
        warning.setStandardButtons(QMessageBox.Ok)
        return warning

    early = find_t_p(CorrectWeights, n)

    Graph.PointsTimeEarly = np.zeros(n, int)
    for i in range(n):
        Graph.PointsTimeEarly[i] = round((Graph.Points[i][0] - GridBegin) / GridStep)

    points_on_correct_axes = True
    for i in range(n):
        if (Graph.PointsTimeEarly[i] != early[i]):
            mistakes.append(1)
            mistakes.append(2)
            points_on_correct_axes = False
            break

    Graph.ArrowPointsTimeEarly = np.zeros((n, n), int)
    for i in range(len(CorrectAdjacencyMatrix)):
        for j in range(len(CorrectAdjacencyMatrix)):
            if (CorrectAdjacencyMatrix[i][j] == 1):
                Graph.ArrowPointsTimeEarly[i][j] = round((Graph.ArrowPoints[i][j][0] - GridBegin) / GridStep)
            else:
                Graph.ArrowPointsTimeEarly[i][j] = -1

    if (points_on_correct_axes):
        for i in range(len(CorrectAdjacencyMatrix)):
            for j in range(len(CorrectAdjacencyMatrix)):
                if ((CorrectAdjacencyMatrix[i][j] == 1) and (Graph.ArrowPointsTimeEarly[i][j] != Graph.PointsTimeEarly[i] + CorrectWeights[i][j])):
                    mistakes.append(2)
                    return mistakes
    return mistakes


# проверка четвертого задания
def checkTask4(Graph, CorrectWeights, GridBegin, GridStep):
    CorrectAdjacencyMatrix = Graph.CorrectAdjacencyMatrix

    # CorrectWeights = np.array([[-1, 1, -1, -1],
    #                            [1, -1, 2, -1],
    #                            [-1, 2, -1, 3],
    #                            [-1, -1, 3, -1]])
    # CorrectAdjacencyMatrix = np.array([[0, 1, 0, 0],
    #                                    [0, 0, 1, 0],
    #                                    [0, 0, 0, 1],
    #                                    [0, 0, 0, 0]])

    n = len(CorrectWeights)

    mistakes = []  # список ошибок:
    #                   1 - вершины не на нужных осях
    #                   2 - стрелки не на нужных осях

    old_mistakes = []
    old_mistakes = checkTask1(Graph, CorrectAdjacencyMatrix, True)

    if (old_mistakes):
        warning = QMessageBox()
        warning.setWindowTitle("Предупреждение")
        warning.setText("Нарушено одно из условий проверки первого задания! Пожалуйста, проверьте каждое из условий:\n1. Верное количество вершин\n2. Верное количество связей\n3. Верные связи\n4. Связи не пересекаются")
        warning.setIcon(QMessageBox.Warning)
        warning.setStandardButtons(QMessageBox.Ok)
        return warning

    early = find_t_p(CorrectWeights, n)
    late = find_t_n(CorrectWeights, early, n)

    Graph.PointsTimeLate = np.zeros(n, int)
    for i in range(n):
        Graph.PointsTimeLate[i] = round((Graph.Points[i][0] - GridBegin) / GridStep)

    points_on_correct_axes = True
    for i in range(n):
        if (Graph.PointsTimeLate[i] != late[i]):
            mistakes.append(1)
            mistakes.append(2)
            points_on_correct_axes = False
            break

    Graph.ArrowPointsTimeLate = np.zeros((n, n), int)
    for i in range(len(CorrectAdjacencyMatrix)):
        for j in range(len(CorrectAdjacencyMatrix)):
            if (CorrectAdjacencyMatrix[i][j] == 1):
                Graph.ArrowPointsTimeLate[i][j] = round((Graph.ArrowPoints[i][j][0] - GridBegin) / GridStep)

    if (points_on_correct_axes):
        for i in range(len(CorrectAdjacencyMatrix)):
            for j in range(len(CorrectAdjacencyMatrix)):
                if ((CorrectAdjacencyMatrix[i][j] == 1) and (Graph.ArrowPointsTimeLate[i][j] != Graph.PointsTimeLate[j] - CorrectWeights[i][j])):
                    mistakes.append(2)
                    return mistakes
    return mistakes