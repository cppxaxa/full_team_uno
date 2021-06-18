
from lib.controllers.v1.BaseDataStore import BaseDataStore

import json
import redis

# TODO Finish this implementation

class RedisDataStore(BaseDataStore):

    def __init__(self):
        # Read some config and connect
        pass

    def get_game_model(self, game_id):
        pass
    
    def get_game_room_model(self, name):
        pass

    def get_user_model(self, username):
        pass

    def set_game_model(self, game_id, game_model):
        pass
    
    def set_game_room_model(self, name, game_room):
        pass

    def set_user_model(self, username, usermodel):
        pass
