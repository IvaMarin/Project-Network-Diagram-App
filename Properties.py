import graph_model as gm
import main as windows

class Properties():

    def __init__(self):
        #свойства первого окна
        self.verification_passed_task_1 = False # проверка 1 задания пойдена

        #свойства второго окна
        self.verification_passed_task_2 = False # проверка 2 задания пойдена
        self.scaler = 3 # параметр увеличения радиуса для второго задания
        self.radius_points_task_2 = self.radius_points * self.scaler # радиус во втором задании

        #свойства третьего окна
        self.verification_passed_task_3 = False # проверка 3 задания пойдена

        #свойства четвертого окна
        self.verification_passed_task_4 = False # проверка 4 задания пойдена

        #свойства пятого окна
        self.verification_passed_task_5 = False # проверка 5 задания пойдена

        #свойства, использующиеся в разных заданиях
            #свойства из таблицы
        self.number_of_squads = self.get_number_of_squads() #количество отделений
        self.total_time #общее время работы (добавить + 3)
        
        self.graph_for_task_1 = self.get_graph() # граф для первого задания
        self.graphs_for_task_5 = self.get_graphs_for_task_5() # графы для 5 задания

        self.radius_points = 30 # радиус вершин по всем заданиям (кроме второго)

        self.step_grid = 100 # шаг сетки

    # функция подсчета количесва отделений
    def get_number_of_squads():
        MainWindow = windows.WindowMenu()
        number_of_squads = 1
        for row in range(MainWindow.ui.tableVar.rowCount()-1):
            if MainWindow.ui.tableVar.item(row, 1).text() >= '1' and MainWindow.ui.tableVar.item(row, 1).text() <= '9' :
                i = int(MainWindow.ui.tableVar.item(row, 1).text())
            if number_of_squads < i:
                number_of_squads = i
        return number_of_squads

    # функция получения общего графа
    def get_graph(self):
        return gm.Graph(self.radius_points)

    # функция получения списка графов для 5 задания
    def get_graphs_for_task_5(self):
        graphs = []
        for i in range(self.number_of_squads):
            graphs.append(self.get_graph)
        return graphs





