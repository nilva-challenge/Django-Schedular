from abc import ABC,abstractmethod

class TodoInterface:
    
    @abstractmethod
    def get_all_todos(self):
        pass

    @abstractmethod
    def get_user_todos(self,user):
        pass
