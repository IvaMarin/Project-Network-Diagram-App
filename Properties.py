import graph_model as gm
import main as windows

class Properties():

    def __init__(self):

        # массив пройденных заданий
        self.verification_passed_tasks = {1: False, 2: False, 3: False, 4: False, 5: False}
        #свойства первого окна

        #свойства второго окна
        self.scaler = 3 # параметр увеличения радиуса для второго задания
        self.radius_points_task_2 = self.radius_points * self.scaler # радиус во втором задании

        #свойства третьего окна

        #свойства четвертого окна

        #свойства пятого окна

        #свойства, использующиеся в разных заданиях
            #свойства из таблицы
        self.number_of_squads = self.get_number_of_squads() #количество отделений
        self.total_time #общее время работы (добавить + 3)
        
        self.graph_for_task_1 = self.get_graph() # граф для первого задания
        self.graph_for_task_3_4 = self.get_graph() # граф для 3-4 задания
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
    def get_graph_from_radius(self):
        return gm.Graph(self.radius_points)

    # функция получения общего графа
    def get_graph_from_graph(self, graph):
        # new_object_graph = graph.__class__
        # new_graph = new_object_graph()
        new_graph = graph.copy()
        return new_graph

    # функция получения списка графов для 5 задания
    def get_graphs_for_task_5(self):
        graphs = []
        for i in range(self.number_of_squads):
            graphs.append(self.get_graph)
        return graphs

    def get_verification_passed_pretasks(self, current):
        return self.verification_passed_tasks[current]    

    # функция получения подтверждения пройденых заданий
    def get_verification_passed_pretasks(self, current):
        # for i in range(current):
        #     if (self.verification_passed_tasks[i] == False):
        #         return False
        # return True
        if (self.verification_passed_tasks[current - 1] == False):
            return False
        else:
            return True

    
    # функция присваивания  подтверждения заданию
    def set__verification_passed_task(self, number):
        self.verification_passed_tasks[number] = True

    def set__verification_passed_task_all(self, arg):
        if (arg):
            self.verification_passed_tasks = {1: True, 2: True, 3: True, 4: True, 5: True}
        else:
            self.verification_passed_tasks = {1: False, 2: False, 3: False, 4: False, 5: False}
        
    






