from .interfaces import UserInterface

class UserService(UserInterface):
    def hash_password(self,user,password):
        user.set_password(password)
        user.save()