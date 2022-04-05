# Controller ������������ MVC (����)
import graph_model as gm

# �������� ������� �� �������; ���������: ������ "����", �������, ������
def CAddPoint(graph, event, but):
	# ���� ������ ������
	if event.button() == but:
		graph.AddPoint(event.pos().x(), event.pos().y()) # �������� �������

# ������� ������� �� �������; ���������: ������ "����", �������, ������
def CDeletePoint(graph, event, but):
	# ���� ������ ������
	if event.button() == but:
		graph.DeletePoint(graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # ������� �������

# ������� ������� �� �������; ���������: ������ "����", �������, ������
def CConnectPoints(graph, event, but):
	# ���� ������ ������
	if event.button() == but:
		graph.ConnectPoints(graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # ������� �������

# ������� ����� ����� ��������� �� �������; ���������: ������ "����", �������, ������
def CDeleteConnection(graph, event, but):
	# ���� ������ ������
	if event.button() == but:
		graph.DeleteConnection(graph.IsCursorOnPoint(event.pos().x(), event.pos().y()),
									  graph.IsCursorOnPoint(event.pos().x(), event.pos().y())) # ������� ����� ����� ���������

# ����������� ������� �� �������; ���������: ������ "����", �������, ������
def CDeleteConnection(graph, event, but):
	# ���� ������ ������
	if event.button() == but:
		graph.MovePoint(graph.IsCursorOnPoint(event.pos().x(), event.pos().y(), event.pos().x(), event.pos().y())) # ����������� �������
