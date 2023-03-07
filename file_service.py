import os, re

class FileService:
    def __init__(self):
        pass

    ####################____ФУНКЦИИ_ДЛЯ_ОЧИСТКИ_СОХРАНЕНИЯ_СТУДЕНТА____####################################################
    
    def clear_answer_universal(self, variant, pathToDir = 'answer_of_student/'):
        for i in range(1, 6):
            path = pathToDir + f'states_of_graphs_{i}/'
            pattern = f'state_{variant}'
            self.purge(path, pattern)
        
    def purge(self, dir, pattern):
        try:
            for f in os.listdir(dir):
                if re.search(pattern, f):
                    print(f'[INFO] DELETE FILE ----> {os.path.join(dir, f)}')
                    os.remove(os.path.join(dir, f))
        except:
            pass
####################################################################################################################### 