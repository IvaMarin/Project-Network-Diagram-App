# Model составляющая MVC (Граф)
# "несуществющие вершины" - вершины в середине списка индексов вершин, которые были удалены (далее без ковычек)

import numpy as np
import copy

# функция для вычисления граничной точки с учётом радиуса
def calculate_bound_point(start_point, end_point, radius):
    try:
        dx = start_point[0] - end_point[0]
        dy = start_point[1] - end_point[1]

        length = np.sqrt(dx ** 2 + dy ** 2)

        # нормализуем
        if (length == 0):
            norm_x, norm_y = 0, 0
        else:
            norm_x, norm_y = dx / length, dy / length

        middle_point_x = end_point[0] + radius * norm_x
        middle_point_y = end_point[1] + radius * norm_y
        middle_point = [middle_point_x, middle_point_y]

        return middle_point

    except (ZeroDivisionError, Exception):
        return None

# класс "граф"
class Graph:
	# конструктор графа; параметры: радиус вершины
	def __init__(self, RadiusPoint):
		# математические характеристики графа
		self.Points = np.empty((0, 2))  # массив координат центров вершин графа (если None, то вершина не существует)
		self.AdjacencyMatrix = np.zeros((0, 0))  # матрица смежности
		self.CorrectAdjacencyMatrix = None

		self.CorrectSquadsWork = None  # верное распределение отделений по работам
		self.SquadsPeopleToWork = None # верное число людей по работам
		self.SquadsPeopleNumber = None # верное число людей в отделении
		
		self.CorrectWeights = None
		self.PointsTimeEarly = None
		self.ArrowPointsTimeEarly = None
		self.PointsTimeLate = None
		self.ArrowPointsTimeLate = None
		
		self.tp = np.empty((0))  # ранний срок наступления события
		self.tn = np.empty((0))  # поздний срок наступления события
		self.R = np.empty((0))  # резерв времени
		self.CriticalPath = np.array([0])  # критический путь
		self.ArrowPoints = np.zeros((0, 0), dtype=object)  # массив координат стрелок

		# графические характеристики графа
		self.RadiusPoint = RadiusPoint  # радиус вершины

		self.PeopleWeights = None

	# добавить вершину; параметры: координата х, координата у
	def AddPoint(self, x, y):
		# для каждой вершины (вне зависимости от существования)
		for i in range(len(self.Points)):
			# если вершина не существует
			if np.isnan(self.Points[i][0]):
				self.Points[i][0], self.Points[i][1] = x, y # добавить координаты х, y центра вершины графа
				# добавить нулевые строки и столбцы
				self.AdjacencyMatrix = np.vstack([self.AdjacencyMatrix, np.zeros(len(self.AdjacencyMatrix))])	
				self.AdjacencyMatrix = np.c_[self.AdjacencyMatrix, np.zeros(len(self.AdjacencyMatrix[0]) + 1)]

				self.ArrowPoints = np.vstack([self.ArrowPoints, np.zeros(len(self.ArrowPoints))])	
				self.ArrowPoints = np.c_[self.ArrowPoints, np.zeros(len(self.ArrowPoints[0]) + 1)]
				return
		# если не было не существующей вершины
		self.Points = np.vstack([self.Points, [x, y]]) # добавить координаты х, y центра вершины графа
		# добавить нулевые строки и столбцы
		self.AdjacencyMatrix = np.vstack([self.AdjacencyMatrix, np.zeros(len(self.AdjacencyMatrix))])	
		self.AdjacencyMatrix = np.c_[self.AdjacencyMatrix, np.zeros(len(self.AdjacencyMatrix[0]) + 1)]

		self.ArrowPoints = np.vstack([self.ArrowPoints, np.zeros(len(self.ArrowPoints))])	
		self.ArrowPoints = np.c_[self.ArrowPoints, np.zeros(len(self.ArrowPoints[0]) + 1)]
	
	# находится ли курсор на вершине; параметры: координата курсора х, координата курсора у
	# вернуть -1, если курсор ни на одной вершине
	# вернуть номер вершины, на которой находится курсор
	def IsCursorOnPoint(self, x, y):
		# по каждой паре координат центра вершины
		for i in range(len(self.Points)-1, -1, -1):
			# если нашлась пара координат центра вершины, в окрестности радиуса вершины которой попал курсор
			if ((x >= self.Points[i][0] - self.RadiusPoint and x <= self.Points[i][0] + self.RadiusPoint) and 
				 (y >= self.Points[i][1] - self.RadiusPoint and y <= self.Points[i][1] + self.RadiusPoint)):
				return i # вернуть индекс вершины, в которую попал курсор
		return -1 # вернуть -1, если не нашлась такая пара координат

	def IsCursorOnArrowPoint(self, x, y):
		for i in range(len(self.ArrowPoints)-1, -1, -1):
			for j in range(len(self.ArrowPoints)-1, -1, -1):
				# если нашлась пара координат конца стрелки, в окрестность которой попал курсор
				if  (type(self.ArrowPoints[i][j]) != float) and ((x >= self.ArrowPoints[i][j][0] - self.RadiusPoint and x <= self.ArrowPoints[i][j][0] + self.RadiusPoint) and 
					(y >= self.ArrowPoints[i][j][1] - self.RadiusPoint and y <= self.ArrowPoints[i][j][1] + self.RadiusPoint)):
					return [i, j] # вернуть индексы вершин
		return [-1, -1] # если не нашлась такая пара координат
	
	# удалить вершину; параметры: индекс удаляемой вершины
	def DeletePoint(self, index):
		# если курсор не наведен на вершину
		if index == -1:
			return # ничего не делать
		self.Points[index][0], self.Points[index][1] = None, None
		# итерироваться по i-й строке/столбку матрицы смежности
		for i in range(len(self.AdjacencyMatrix)):
			# удалить связи
			self.AdjacencyMatrix[i][index] = 0
			self.AdjacencyMatrix[index][i] = 0

	# связать вершины; параметры: индекс вершины
	def AddConnection(self, firstIndex, secondIndex):
		# если курсор не наведен на вершину
		if firstIndex == -1 or secondIndex == -1:
			return # ничего не делать
		self.AdjacencyMatrix[firstIndex][secondIndex] = 1 # соединить вершины

		point = calculate_bound_point(self.Points[firstIndex], self.Points[secondIndex], self.RadiusPoint)
		self.ArrowPoints[firstIndex][secondIndex] = point
					
	# удалить связь между вершинами; параметры: индекс первой вершины, индекс второй вершины
	def DeleteConnection(self, firstIndex, secondIndex):
		# если курсор не наведен хотя бы на одну из вершин
		if firstIndex == -1 or secondIndex == -1:
			return # ничего не делать
		# итерироваться по парам связанных вершин
		self.AdjacencyMatrix[firstIndex][secondIndex] = 0 # удалить связь

	# переместить вершину; параметры: номер вершины, координата х, координата y
	def MovePoint(self, index, x, y):
		# если курсор не наведен на вершину
		if index == -1:
			return # ничего не делать
		# присвоить новые значения координат центра вершины
		self.Points[index][0], self.Points[index][1] = x, y # присовить новые значения координат центра вершины

		for i in range(len(self.ArrowPoints)-1, -1, -1):
			if (i == index):
				for j in range(len(self.ArrowPoints)-1, -1, -1):
					if type(self.ArrowPoints[i][j]) != float:
						self.MoveArrowPoint([i, j], self.ArrowPoints[i][j][0], self.ArrowPoints[i][j][1])
					if type(self.ArrowPoints[j][i]) != float:
						self.MoveArrowPoint([j, i], self.ArrowPoints[j][i][0], self.ArrowPoints[j][i][1])

	# переместить пунктирную стрелку; параметры: номера вершин, координата х, координата y
	def MoveArrowPoint(self, index, x, y):
		if index == [-1, -1]:
			return
		start_point = self.Points[index[0]]
		end_point = self.Points[index[1]]

		dx = start_point[0] - end_point[0]
		dy = start_point[1] - end_point[1]
		
		length = np.sqrt(dx ** 2 + dy ** 2)

		# нормализуем
		if (length == 0):
			norm_x, norm_y = 0, 0
		else:
			norm_x, norm_y = dx / length, dy / length
		
		arrow_height = 10
		p1_x = start_point[0] - (self.RadiusPoint + arrow_height) * norm_x
		p1_y = start_point[1] - (self.RadiusPoint + arrow_height) * norm_y
		p1 = np.array([p1_x, p1_y])

		p2_x = end_point[0] + self.RadiusPoint * norm_x
		p2_y = end_point[1] + self.RadiusPoint * norm_y
		p2 = np.array([p2_x, p2_y])
			
		p3 = np.array([x, y])
		
		distance = np.sum((p1 - p2)**2)

		# параметризация: p1 + t (p2 - p1)
		# проекция находится где t = [(p3-p1) . (p2-p1)] / |p2-p1|^2
		if (distance == 0):
			t = 0
		else:
			t = np.sum((p3 - p1) * (p2 - p1)) / distance
			
		if t > 1:
			projection = p2
		elif t <= 0:
			projection = p1
		else:
			projection = p1 + t * (p2 - p1)
	
		self.ArrowPoints[index[0], index[1]] = projection
	
	# выделить критический путь
	def SelectCriticalPath(self, firstIndex, secondIndex):
		# если курсор не наведен на вершину
		if firstIndex == -1 or secondIndex == -1:
			return # ничего не делать
		# если связь выделена как критическая
		if self.AdjacencyMatrix[firstIndex][secondIndex] == 2:
			self.AdjacencyMatrix[firstIndex][secondIndex] = 1 # убрать критическое выделение
			return
		# если связть существовала
		if self.AdjacencyMatrix[firstIndex][secondIndex] == 1:
			self.AdjacencyMatrix[firstIndex][secondIndex] = 2 # выделить критическую связь

	# функция копирования графа (в разработке)
	def copy_graph(self):
		new_graph = Graph(30)
		new_graph.Points =  copy.deepcopy(self.Points) 
		new_graph.AdjacencyMatrix = copy.deepcopy(self.AdjacencyMatrix)
		new_graph.CorrectAdjacencyMatrix = copy.deepcopy(self.CorrectAdjacencyMatrix)
		
		new_graph.CorrectWeights = copy.deepcopy(self.CorrectWeights)
		new_graph.PointsTimeEarly = copy.deepcopy(self.PointsTimeEarly)
		new_graph.ArrowPointsTimeEarly = copy.deepcopy(self.ArrowPointsTimeEarly)
		new_graph.PointsTimeLate = copy.deepcopy(self.PointsTimeLate)
		new_graph.ArrowPointsTimeLate = copy.deepcopy(self.ArrowPointsTimeLate)
		
		new_graph.tp = copy.deepcopy(self.tp)  # ранний срок наступления события
		new_graph.tn = copy.deepcopy(self.tn)  # поздний срок наступления события
		new_graph.R = copy.deepcopy(self.R) # резерв времени
		new_graph.CriticalPath = copy.deepcopy(self.CriticalPath)  # критический путь
		new_graph.ArrowPoints = copy.deepcopy(self.ArrowPoints) # массив координат стрелок

		new_graph.RadiusPoint = copy.deepcopy(self.RadiusPoint) # радиус вершины

		new_graph.PeopleWeights = copy.deepcopy(self.PeopleWeights)


class GraphOrthogonal:
	def __init__(self, Radius) -> None:
		self.Radius = Radius
		self.Points = dict() 		# key: (digit, id) 						value: (x, y)
		self.AdjacencyList = dict() # key: (digit1, id1) 					value: (digit2, id2)
		self.Arrows = dict()		# key: ((digit1, id1), (digit2, id2)) 	value: (x, y)
		self.PeopleWeights = None	# key: ((digit1, id1), (digit2, id2)) 	value: weight
		self.Sequences = list()
	
	def _FindMaxId(self, digit):
		id = 0
		for (p_digit, p_id) in self.Points.keys():
			if p_digit == digit:
				id = max(p_id + 1, id)
		return id

	def AddPoint(self, digit, x, y):
		id = self._FindMaxId(digit)
		self.Points[(digit, id)] = (x, y)

	def AddPointsSequence(self, sequence: list, gridStart, gridStep, gridY):
		self.Sequences.append(sequence)
		for i, digit in enumerate(sequence):
			cur_digit = sequence[i] 
			cur_id = self._FindMaxId(digit)

			gridX = gridStart + i * gridStep
			self.AddPoint(digit, gridX, gridY)

			if (i > 0):
				self.AddConnection((prev_digit, prev_id), (cur_digit, cur_id))
			
			prev_digit = cur_digit
			prev_id = cur_id
	
	def DeletePoint(self, Point: tuple):
		self.Points.pop(Point)
		AdjacencyListCopy = self.AdjacencyList.copy()
		for p1, p2 in AdjacencyListCopy.items():
			if p1 == Point:
				self.DeleteConnection(p1, p2)
			elif p2 == Point:
				self.DeleteConnection(p1, p2)
	
	def DeletePointsSequence(self, gridY):
		PointsCopy = self.Points.copy()
		deletedSequence = []
		for (p_digit, p_id), (p_x, p_y) in PointsCopy.items():
			if p_y == gridY:
				deletedSequence.append(p_digit)
				self.DeletePoint((p_digit, p_id))
		self.Sequences.remove(deletedSequence)

	def AddConnection(self, firstPoint: tuple, secondPoint: tuple):
		if (firstPoint in self.Points.keys()) and (secondPoint in self.Points.keys()):
			self.AdjacencyList[firstPoint] = secondPoint
			self.InitializeArrow(firstPoint, secondPoint)
	
	def DeleteConnection(self, firstPoint: tuple, secondPoint: tuple):
		try:
			self.AdjacencyList.pop(firstPoint)
			self.Arrows.pop((firstPoint, secondPoint))
		except:
			pass

	def InitializeArrow(self, firstPoint: tuple, secondPoint: tuple):
		(firstPoint_x, firstPoint_y) = self.Points[firstPoint]
		(secondPoint_x, secondPoint_y) = self.Points[secondPoint]
		[x, y] = calculate_bound_point([firstPoint_x, firstPoint_y], [secondPoint_x, secondPoint_y], self.Radius)
		self.Arrows[(firstPoint, secondPoint)] = (x, y)

	def IsCursorOnPoint(self, x, y):
		for (p_digit, p_id), (p_x, p_y) in self.Points.items():
			if ((x >= p_x - self.Radius and x <= p_x + self.Radius) and 
				(y >= p_y - self.Radius and y <= p_y + self.Radius)):
				return (p_digit, p_id)
		return None 

	def IsCursorOnArrowPoint(self, x, y):
		for key, (a_x, a_y) in self.Arrows.items():
			if  ((x >= a_x - self.Radius and x <= a_x + self.Radius) and 
				 (y >= a_y - self.Radius and y <= a_y + self.Radius)):
					return key
		return None

	def UpdateArrows(self, Point: tuple):
		for (p_digit, p_id) in self.Points.keys():
			if self.Arrows.get((Point, (p_digit, p_id))) != None:
				(x, y) = self.Arrows[(Point, (p_digit, p_id))]
				self.MoveArrowPoint(Point, (p_digit, p_id), x, y)
			
			if self.Arrows.get(((p_digit, p_id), Point)) != None:
				(x, y) = self.Arrows[((p_digit, p_id), Point)]
				self.MoveArrowPoint((p_digit, p_id), Point, x, y)

	def MovePoint(self, Point: tuple, x, y):
		self.Points[Point] = (x, y)
		self.UpdateArrows(Point)

	def MovePointFixedY(self, Point: tuple, x):
		(cur_x, cur_y) = self.Points[Point]
		self.Points[Point] = (x, cur_y)
		self.UpdateArrows(Point)

	def MoveAllPointsFixedY(self, Point: tuple, x):
		MovedPoints = list()
		for p in self.Points.keys():
			if (p[0] == Point[0]):
				(cur_x, cur_y) = self.Points[p]
				self.Points[p] = (x, cur_y)
				MovedPoints.append(p)
		for p in MovedPoints:
			self.UpdateArrows(p)

	def MoveArrowPoint(self, firstPoint: tuple, secondPoint: tuple, x, y):
		(firstPoint_x, firstPoint_y) = self.Points[firstPoint]
		(secondPoint_x, secondPoint_y) = self.Points[secondPoint]
		dx = firstPoint_x - secondPoint_x
		dy = firstPoint_y - secondPoint_y
		length = np.sqrt(dx ** 2 + dy ** 2)

		if (length == 0):
			norm_x, norm_y = 0, 0
		else:
			norm_x, norm_y = dx / length, dy / length
		
		arrow_height = 10
		p1_x = firstPoint_x - (self.Radius + arrow_height) * norm_x
		p1_y = firstPoint_y - (self.Radius + arrow_height) * norm_y
		p1 = np.array([p1_x, p1_y])

		p2_x = secondPoint_x + self.Radius * norm_x
		p2_y = secondPoint_y + self.Radius * norm_y
		p2 = np.array([p2_x, p2_y])
			
		p3 = np.array([x, y])
		
		distance = np.sum((p1 - p2)**2)
		if (distance == 0):
			t = 0
		else:
			t = np.sum((p3 - p1) * (p2 - p1)) / distance
			
		if t > 1:
			projection = p2
		elif t <= 0:
			projection = p1
		else:
			projection = p1 + t * (p2 - p1)

		(x, y) = projection
	
		self.Arrows[(firstPoint, secondPoint)] = (x, y)

	def MoveArrowPointFixedY(self, firstPoint: tuple, secondPoint: tuple, x):
		(cur_x, cur_y) = self.Arrows[(firstPoint, secondPoint)]

		(firstPoint_x, firstPoint_y) = self.Points[firstPoint]
		(secondPoint_x, secondPoint_y) = self.Points[secondPoint]
		dx = firstPoint_x - secondPoint_x
		dy = firstPoint_y - secondPoint_y
		length = np.sqrt(dx ** 2 + dy ** 2)

		if (length == 0):
			norm_x, norm_y = 0, 0
		else:
			norm_x, norm_y = dx / length, dy / length
		
		arrow_height = 10
		p1_x = firstPoint_x - (self.Radius + arrow_height) * norm_x
		p1_y = firstPoint_y - (self.Radius + arrow_height) * norm_y
		p1 = np.array([p1_x, p1_y])

		p2_x = secondPoint_x + self.Radius * norm_x
		p2_y = secondPoint_y + self.Radius * norm_y
		p2 = np.array([p2_x, p2_y])
			
		p3 = np.array([x, cur_y])
		
		distance = np.sum((p1 - p2)**2)
		if (distance == 0):
			t = 0
		else:
			t = np.sum((p3 - p1) * (p2 - p1)) / distance
			
		if t > 1:
			projection = p2
		elif t <= 0:
			projection = p1
		else:
			projection = p1 + t * (p2 - p1)

		(x, cur_y) = projection
	
		self.Arrows[(firstPoint, secondPoint)] = (x, cur_y)

	def _Print(self):
		print("GraphOrthogonal:")

		print("Points:")
		for (p_digit, p_id), (p_x, p_y) in self.Points.items():
			print(p_digit, p_id, p_x, p_y)

		print("AdjacencyList:")
		for (v1_digit, v1_id), (v2_digit, v2_id) in self.AdjacencyList.items():
			print('(',v1_digit, v1_id,')', "->", '(',v2_digit, v2_id,')')
		
		print("Arrows:")
		for ((v1_digit, v1_id), (v2_digit, v2_id)), (a_x, a_y) in self.Arrows.items():
			print('(',v1_digit, v1_id,')', '(',v2_digit, v2_id,')', ": " , '(',a_x, a_y,')')