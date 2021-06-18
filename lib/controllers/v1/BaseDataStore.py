
from abc import ABC, abstractmethod

class BaseDataStore(ABC):

    @abstractmethod
    def get_game_model(self, game_id):
        pass
    
    @abstractmethod
    def get_game_room_model(self, name):
        pass

    @abstractmethod
    def get_user_model(self, username):
        pass

    @abstractmethod
    def set_game_model(self, game_id, game_model):
        pass
    
    @abstractmethod
    def set_game_room_model(self, name, game_room):
        pass

    @abstractmethod
    def set_user_model(self, username, usermodel):
        pass

    