# Controller составляющая MVC (Граф)

from checker import Checker

# добавить вершину по нажатию; параметры: объект "граф", событие, кнопка
def CAddPoint(graph, event, but):
	# если нажата кнопка
	if event.button() == but:
		graph.AddPoint(event.pos().x(), event.pos().y()) # добавить вершину

# добавить вершину по нажатию в сетку; параметры: объект "граф", событие, кнопка, начало сетки по х, шаг сетки по х, фиксированная координата по y
# если FixedY == None, то не фикисировать по y
def CAddPointGrid(graph, event, but, GridBegin, GridStep, FixedY):
	# если нажата кнопка
	if event.button() == but:
		wasFinded = False # найден промежуток, в который попадает курсор
		i = 0
		while(not wasFinded):
			i += 1 # инкрементировать номер
			if event.pos().x() <= GridBegin+i*GridStep:
				wasFinded = True # найден промежуток
		XonGrid = GridBegin
		# если курсор в диапозоне одной лини
		if abs(event.pos().x() >= GridBegin+(i-3/2)*GridStep) and abs(event.pos().x() < GridBegin+(i-1/2)*GridStep):
			XonGrid = GridBegin+(i-1)*GridStep
		elif abs(event.pos().x() >= GridBegin+(i-1/2)*GridStep) and abs(event.pos().x() < GridBegin+(i+3/2)*GridStep):
			XonGrid = GridBegin+i*GridStep
		# если указана фиксированная координата по y
		if FixedY != None:
			graph.AddPoint(XonGrid, FixedY) # добавить вершину
			return
		graph.AddPoint(XonGrid, event.pos().y()) # добавить вершину

# удалить вершину по нажатию; параметры: объект "граф", событие, кнопка
def CDeletePoint(graph, event, but):
	# если нажата кнопка
	if event.button() == but:
		index = graph.IsCursorOnPoint(event.pos().x(), event.pos().y())
		graph.DeletePoint(index) # удалить вершину

	return index

# связать вершины по нажатию; параметры: объект "граф", событие, кнопка, выделенные точки
def CAddConnection(graph, event, but, points):
	# если нажата кнопка
	if event.button() == but:
		graph.AddConnection(int(points[0]), int(points[1])) # связать вершины

# удалить связь между вершинами по нажатию; параметры: объект "граф", событие, кнопка
def CDeleteConnection(graph, event, but, points):
	# если нажата кнопка
	if event.button() == but:
		graph.DeleteConnection(int(points[0]), int(points[1])) # удалить связь между вершинами

# переместить вершину по нажатию; параметры: объект "граф", событие, кнопка
def CMovePoint(graph, event, but, FixedPoint, width, height):
	# если нажата кнопка
	if event.buttons() == but:
		# переместить вершину
		graph.MovePoint(FixedPoint, Checker.checkBounds(event.pos().x(), width, graph.RadiusPoint), 
		  							Checker.checkBounds(event.pos().y(), height, graph.RadiusPoint)) 

# переместить пунктирную стрелку по нажатию; параметры: объект "граф", событие, кнопка
def CMoveArrowPoint(graph, event, but, FixedArrowPoint):
	# если нажата кнопка
	if event.buttons() == but:
		graph.MoveArrowPoint(FixedArrowPoint, event.pos().x(),
		                     event.pos().y())  # переместить пунктирную стрелку

# переместить пунктирную стрелку по нажатию в сетке; параметры: объект "граф", событие, кнопка, начало сетки по х, шаг сетки по х
def CMoveArrowPointGrid(graph, event, but, FixedArrowPoint, GridBegin, GridStep):
	wasFinded = False  # найден промежуток, в который попадает курсор
	i = 0
	while(not wasFinded):
		i += 1  # инкрементировать номер
		if event.pos().x() <= GridBegin+i*GridStep:
			wasFinded = True  # найден промежуток
	XonGrid = GridBegin
	# если курсор в диапазоне одной лини
	if abs(event.pos().x() >= GridBegin+(i-3/2)*GridStep) and abs(event.pos().x() < GridBegin+(i-1/2)*GridStep):
		XonGrid = GridBegin+(i-1)*GridStep
	elif abs(event.pos().x() >= GridBegin+(i-1/2)*GridStep) and abs(event.pos().x() < GridBegin+(i+3/2)*GridStep):
		XonGrid = GridBegin+i*GridStep

	# если нажата кнопка
	if event.buttons() == but:
		graph.MoveArrowPoint(FixedArrowPoint, XonGrid,
		                     event.pos().y())  # переместить переместить пунктирную стрелку

# переместить вершину по нажатию в сетке; параметры: объект "граф", событие, кнопка, начало сетки по х, шаг сетки по х, фиксированная координата по y
# если FixedY == None, то не фикисировать по y
def CMovePointGrid(graph, event, but, FixedPoint, GridBegin, GridStep, FixedY, width, height):
	wasFinded = False # найден промежуток, в который попадает курсор
	i = 0
	while(not wasFinded):
		i += 1 # инкрементировать номер
		if event.pos().x() <= GridBegin+i*GridStep:
			wasFinded = True # найден промежуток
	XonGrid = GridBegin
	# если курсор в диапозоне одной лини
	if abs(event.pos().x() >= GridBegin+(i-3/2)*GridStep) and abs(event.pos().x() < GridBegin+(i-1/2)*GridStep):
			XonGrid = GridBegin+(i-1)*GridStep
	elif abs(event.pos().x() >= GridBegin+(i-1/2)*GridStep) and abs(event.pos().x() < GridBegin+(i+3/2)*GridStep):
		XonGrid = GridBegin+i*GridStep
	if FixedY != None:
		if event.buttons() == but:
			# переместить вершину
			graph.MovePoint(FixedPoint, 
		   					Checker.checkBounds(XonGrid, width, graph.RadiusPoint), 
		   					Checker.checkBounds(FixedY, height, graph.RadiusPoint)) 
		return
	if event.buttons() == but:
		# переместить вершину
		graph.MovePoint(FixedPoint, 
		  				Checker.checkBounds(XonGrid, width, graph.RadiusPoint), 
		  				Checker.checkBounds(event.pos().y(), height, graph.RadiusPoint)) 

# находится ли курсор на вершине;
def CIsCursorOnPoint(graph, event, but):
	# если нажата кнопка
	if event.button() == but:
		return graph.IsCursorOnPoint(event.pos().x(), event.pos().y())

# находится ли курсор на пунктирной стрелке;
def CIsCursorOnArrowPoint(graph, event, but):
	# если нажата кнопка
	if event.button() == but:
		return graph.IsCursorOnArrowPoint(event.pos().x(), event.pos().y())

# выделить критический путь по нажатию; параметры: объект "граф", событие, кнопка, выделенные точки
def CSelectCriticalPath(graph, event, but, points):
	# если нажата кнопка
	if event.button() == but:
		graph.SelectCriticalPath(int(points[0]), int(points[1])) # добавить вершину в критический путь