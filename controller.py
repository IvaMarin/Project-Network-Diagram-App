# Controller составляющая MVC (Граф)

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
		graph.DeletePoint(graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # удалить вершину

# связать вершины по нажатию; параметры: объект "граф", событие, кнопка, выделенные точки
def CConnectPoints(graph, event, but, points):
	# если нажата кнопка
	if event.button() == but:
		graph.ConnectPoints(int(points[0]), int(points[1])) # связать вершины

# удалить связь между вершинами по нажатию; параметры: объект "граф", событие, кнопка
def CDeleteConnection(graph, event, but, points):
	# если нажата кнопка
	if event.button() == but:
		graph.DeleteConnection(int(points[0]), int(points[1])) # удалить связь между вершинами

# переместить вершину по нажатию; параметры: объект "граф", событие, кнопка
def CMovePoint(graph, event, but, FixedPoint):
	# если нажата кнопка
	if event.buttons() == but:
		graph.MovePoint(FixedPoint, event.pos().x(), event.pos().y()) # переместить вершину

# переместить вершину по нажатию в сетке; параметры: объект "граф", событие, кнопка, начало сетки по х, шаг сетки по х, фиксированная координата по y
# если FixedY == None, то не фикисировать по y
def CMovePointGrid(graph, event, but, FixedPoint, GridBegin, GridStep, FixedY):
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
			graph.MovePoint(FixedPoint, XonGrid, FixedY) # переместить вершину
		return
	if event.buttons() == but:
		graph.MovePoint(FixedPoint, XonGrid, event.pos().y()) # переместить вершину

# находится ли курсор на вершине;
def CIsCursorOnPoint(graph, event, but):
	# если нажата кнопка
	if event.button() == but:
		return graph.IsCursorOnPoint(event.pos().x(), event.pos().y())
