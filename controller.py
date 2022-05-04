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
		# если расстояние от курсора до левой ближайшей границы сетки меньше или равно чем до правой
		if abs(event.pos().x() - GridBegin+(i-1)*GridStep) <= abs(event.pos().x() - GridBegin+i*GridStep):
			XonGrid = GridBegin+(i-1)*GridStep
		else:
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
def CMovePoint(graph, event):
	graph.MovePoint(graph.IsCursorOnPoint(event.pos().x(), event.pos().y()), event.pos().x(), event.pos().y()) # переместить вершину

# переместить вершину по нажатию в сетке; параметры: объект "граф", событие, кнопка, начало сетки по х, шаг сетки по х, фиксированная координата по y
# если FixedY == None, то не фикисировать по y
def CMovePointGrid(graph, event, GridBegin, GridStep, FixedY):
	wasFinded = False # найден промежуток, в который попадает курсор
	i = 0
	while(not wasFinded):
		i += 1 # инкрементировать номер
		if event.pos().x() <= GridBegin+i*GridStep:
			wasFinded = True # найден промежуток
	XonGrid = GridBegin
	# если расстояние от курсора до левой ближайшей границы сетки меньше или равно чем до правой
	if abs(event.pos().x() - GridBegin+(i-1)*GridStep) <= abs(event.pos().x() - GridBegin+i*GridStep):
		XonGrid = GridBegin+(i-1)*GridStep
	else:
		XonGrid = GridBegin+i*GridStep
	# если указана фиксированная координата по y
	if FixedY != None:
		graph.MovePoint(graph.IsCursorOnPoint(event.pos().x(), event.pos().y()), XonGrid, FixedY) # переместить вершину
		return
	graph.MovePoint(graph.IsCursorOnPoint(event.pos().x(), event.pos().y()), XonGrid, event.pos().y()) # переместить вершину
