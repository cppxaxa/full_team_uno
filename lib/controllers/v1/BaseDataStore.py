
from abc import ABC, abstractmethod

class BaseDataStore(ABC):

    @abstractmethod
    def get_game_model(self, game_id):
        pass
    
    @abstractmethod
    def get_game_room_model(self, username, name):
        pass

    @abstractmethod
    def get_user_model(self, username):
        pass

    @abstractmethod
    def set_game_model(self, game_model):
        pass
    
    @abstractmethod
    def set_game_room_model(self, game_room):
        pass

    @abstractmethod
    def set_user_model(self, usermodel):
        pass

    @abstractmethod
    def get_all_game_rooms(self):
        pass

    @abstractmethod
    def get_game_rooms_by_username(self, username):
        pass
    
    @abstractmethod
    def add_user_to_game_room(username, gameroom_name, param_username):
        pass

    @abstractmethod
    def remove_user_from_game_room(username, gameroom_name, param_username):
        pass

    