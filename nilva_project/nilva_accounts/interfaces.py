from abc import ABC,abstractmethod

class UserInterface(ABC):
    
    @abstractmethod
    def hash_password(self,user,password):
        pass