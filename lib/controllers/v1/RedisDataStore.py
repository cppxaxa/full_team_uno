
from lib.models.v1.GameModel import GameModel
from lib.models.v1.GameRoomModel import GameRoomModel
from lib.models.v1.UserModel import UserModel
from lib.controllers.v1.BaseDataStore import BaseDataStore

import json
import redis

# TODO Finish this implementation

class RedisDataStore(BaseDataStore):

    def __init__(self):
        with open("app.settings.json") as f:
            self.config = json.load(f)
        self.r = redis.Redis(host=self.config["redis_host"], port=self.config["redis_port"],
                                password=self.config["redis_password"])

    def get_game_model(self, game_id):
        key = self.get_key('uno', 'global', 'game', game_id)
        val = self.r.get(key)
        if val is not None:
            return GameModel.parse_obj(json.loads(val.decode('UTF-8')))
        return val
    
    def get_game_room_model(self, username, name):
        key = self.get_key('uno', username, 'gameroom', name)
        val = self.r.get(key)
        if val is not None:
            return GameRoomModel.parse_obj(json.loads(val.decode('UTF-8')))
        return val

    def get_user_model(self, username):
        key = self.get_key('uno', 'admin', 'user', username)
        val = self.r.get(key)
        if val is not None:
            return UserModel.parse_obj(json.loads(val.decode('UTF-8')))
        return val

    def set_game_model(self, game_model):
        key = self.get_key('uno', 'global', 'game', game_model.game_id)
        value = game_model.json()
        return self.r.set(key, value)
    
    def set_game_room_model(self, game_room: GameRoomModel):
        key = self.get_key('uno', game_room.created_by, 'gameroom', game_room.name)
        value = game_room.json()
        return self.r.set(key, value)

    def set_user_model(self, usermodel: UserModel):
        key = self.get_key('uno', 'admin', 'user', usermodel.username)
        value = usermodel.json()
        return self.r.set(key, value)

    def get_all_game_rooms(self):
        query = self.get_key('uno', '*', 'gameroom', '*')
        keys = self.r.keys(query)
        resp = [json.loads(self.r.get(key).decode('UTF-8')) for key in keys]
        response = {}
        for key, obj in zip(keys, resp):
            response[key.decode('UTF-8').split('/')[-1]] = obj
        return response

    def get_game_rooms_by_username(self, username):
        query = self.get_key('uno', username, 'gameroom', '*')
        keys = self.r.keys(query)
        resp = [json.loads(self.r.get(key).decode('UTF-8')) for key in keys]
        response = {}
        for key, obj in zip(keys, resp):
            response[key.decode('UTF-8').split('/')[-1]] = obj
        return response
    
    def get_game_rooms_by_username_and_name(self, username, gameroom_name):
        key = self.get_key('uno', username, 'gameroom', gameroom_name)
        val = self.r.get(key)
        if val is not None:
            return GameRoomModel.parse_obj(json.loads(val.decode('UTF-8')))
        return val
    
    def add_user_to_game_room(self, username, gameroom_name, param_username):
        param_usermodel = self.get_user_model(param_username)
        if param_usermodel is None:
            return False, "Invalid username to add"
        key = self.get_key('uno', username, 'gameroom', gameroom_name)
        gameroom = self.r.get(key)
        if gameroom is None:
            return False, "Incorrect gameroom owner or invalid gameroom"
        gameroom = json.loads(gameroom.decode('UTF-8'))
        participants = set(gameroom["participants"])
        participants.add(param_username)
        gameroom["participants"] = list(participants)
        self.set_game_room_model(GameRoomModel.parse_obj(gameroom))
        return True, ""

    def remove_user_from_game_room(self, username, gameroom_name, param_username):
        param_usermodel = self.get_user_model(param_username)
        if param_usermodel is None:
            return False, "Invalid username to remove"
        key = self.get_key('uno', username, 'gameroom', gameroom_name)
        gameroom = self.r.get(key)
        if gameroom is None:
            return False, "Incorrect gameroom owner or invalid gameroom"
        gameroom = json.loads(gameroom.decode('UTF-8'))
        gameroom["participants"] = [el for el in gameroom["participants"] if el.lower() != param_username.lower()]
        self.set_game_room_model(GameRoomModel.parse_obj(gameroom))
        return True, ""

    def get_key(self, domain, owner, app, key):
        return '/'.join([domain, owner, app, key])
