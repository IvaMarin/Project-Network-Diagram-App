# Controller составляющая MVC (Граф)
from BNG.src.python.graph import GraphModel as graph

# добавить вершину по нажатию; параметры: объект "граф", событие, кнопка
def CAddPoint(graph, event, but):
	# если нажата кнопка <- добавить проверку на нахождение в поле
	if event.button() == but:
		graph.AddPoint(event.pos().x(), event.pos().y(), event) # добавить вершину

# удалить вершину по нажатию; параметры: объект "граф", событие, кнопка
def CDeletePoint(graph, event, but):
	# если нажата кнопка
	if event.button() == but:
		graph.DeletePoint(graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # удалить вершину

# связать вершины по нажатию; параметры: объект "граф", событие, кнопка
def CConnectPoints(graph, event, but):
	# если нажата кнопка
	if event.button() == but:
		graph.ConnectPoints(graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # связать вершины

# удалить связь между вершинами по нажатию; параметры: объект "граф", событие, кнопка
def CDeleteConnection(graph, event, but):
	# если нажата кнопка
	if event.button() == but:
		graph.DeleteConnection(graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # удалить связь между вершинами

# переместить вершину по нажатию; параметры: объект "граф", событие, кнопка
def CMovePoint(graph, event):
	# если нажата кнопка
	#if event.button() == but:
		graph.MovePoint(graph.IsCursorOnPoint(event.pos().x(), event.pos().y()), event.pos().x(), event.pos().y()) # переместить вершину
