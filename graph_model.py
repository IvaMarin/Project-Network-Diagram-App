# Model составляющая MVC (Граф)
# "несуществющие вершины" - вершины в середине списка индексов вершин, которые были удалены (далее без ковычек)
import numpy as np

# класс "граф"
class Graph:
	# конструктор графа; параметры: радиус вершины
	def __init__(self, RadiusPoint):
		# математические характеристики графа
		self.Points = np.empty((0,2)) # массив координат центров вершин графа (если None, то вершина не существует)
		self.AdjacencyMatrix = np.zeros((0,0)) # матрица смежности

		# графические характеристики графа
		self.RadiusPoint = RadiusPoint # радиус вершины

	# добавить вершину; параметры: координата х, координата у
	def AddPoint(self, x, y):
		# для каждой вершины (вне зависимости от существования)
		for i in range(len(self.Points)):
			# если вершина не существует
			if np.isnan(self.Points[i][0]):
				self.Points[i][0], self.Points[i][1] = x, y # добавить координаты х, y центра вершины графа
				# добавить нулевые строки и столбцы
				self.AdjacencyMatrix = np.vstack([self.AdjacencyMatrix, np.zeros(len(self.AdjacencyMatrix))])	
				self.AdjacencyMatrix = np.c_[self.AdjacencyMatrix, np.zeros(len(self.AdjacencyMatrix[0])+1)]
				return
		# если не было не существующей вершины
		self.Points = np.vstack([self.Points, [x, y]]) # добавить координаты х, y центра вершины графа
		# добавить нулевые строки и столбцы
		self.AdjacencyMatrix = np.vstack([self.AdjacencyMatrix, np.zeros(len(self.AdjacencyMatrix))])	
		self.AdjacencyMatrix = np.c_[self.AdjacencyMatrix, np.zeros(len(self.AdjacencyMatrix[0])+1)]
	
	# находится ли курсор на вершине; параметры: координата курсора х, координата курсора у
	# вернуть -1, если курсор ни на одной вершине
	# вернуть номер вершины, на которой находится курсор
	def IsCursorOnPoint(self, x, y):
		# по каждой паре координат центра вершины
		for i in range(len(self.Points)):
			# если нашлась пара координат центра вершины, в окрестности радиуса вершины которой попал курсор
			if ((x >= self.Points[i][0] - self.RadiusPoint and x <= self.Points[i][0] + self.RadiusPoint) and 
				 (y >= self.Points[i][1] - self.RadiusPoint and y <= self.Points[i][1] + self.RadiusPoint)):
				return i # вернуть индекс вершины, в которую попал курсор
		return -1 # вернуть -1, если не нашлась такая пара координат
	
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
	def ConnectPoints(self, firstIndex, secondIndex):
		# если курсор не наведен на вершину
		if firstIndex == -1 or secondIndex == -1:
			return # ничего не делать
		self.AdjacencyMatrix[firstIndex][secondIndex] = 1 # соединить вершины
					
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
		# присовить новые значения координат центра вершины
		self.Points[index][0], self.Points[index][1] = x, y # присовить новые значения координат центра вершины
