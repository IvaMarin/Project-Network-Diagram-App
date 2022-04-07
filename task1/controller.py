# Controller ñîñòàâëÿþùàÿ MVC (Ãðàô)
import graph_model as gm

# äîáàâèòü âåðøèíó ïî íàæàòèþ ïàðàìåòðû: îáúåêò "ãðàô", ñîáûòèå, êíîïêà
def CAddPoint(graph, event, but):
	# åñëè íàæàòà êíîïêà
	if event.button() == but:
		graph.AddPoint(event.pos().x(), event.pos().y()) # äîáàâèòü âåðøèíó

# óäàëèòü âåðøèíó ïî íàæàòèþ; ïàðàìåòðû: îáúåêò "ãðàô", ñîáûòèå, êíîïêà
def CDeletePoint(graph, event, but):
	# åñëè íàæàòà êíîïêà
	if event.button() == but:
		graph.DeletePoint(graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # óäàëèòü âåðøèíó

# ñâÿçàòü âåðøèíû ïî íàæàòèþ; ïàðàìåòðû: îáúåêò "ãðàô", ñîáûòèå, êíîïêà
def CConnectPoints(graph, event, but):
	# åñëè íàæàòà êíîïêà
	if event.button() == but:
		graph.ConnectPoints(graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # ñâÿçàòü âåðøèíû

# óäàëèòü ñâÿçü ìåæäó âåðøèíàìè ïî íàæàòèþ; ïàðàìåòðû: îáúåêò "ãðàô", ñîáûòèå, êíîïêà
def CDeleteConnection(graph, event, but):
	# åñëè íàæàòà êíîïêà
	if event.button() == but:
		graph.DeleteConnection(graph.IsCursorOnPoint(event.pos().x(), event.pos().y()),
									  graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # óäàëèòü ñâÿçü ìåæäó âåðøèíàìè

# ïåðåìåñòèòü âåðøèíó ïî íàæàòèþ; ïàðàìåòðû: îáúåêò "ãðàô", ñîáûòèå, êíîïêà
def CDeleteConnection(graph, event, but):
	# åñëè íàæàòà êíîïêà
	if event.button() == but:
		graph.MovePoint(graph.IsCursorOnPoint(event.pos().x(), event.pos().y(), event.pos().x(), event.pos().y())) # ïåðåìåñòèòü âåðøèíó
