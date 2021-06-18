
from lib.controllers.v1.RedisDataStore import RedisDataStore
from lib.controllers.v1.GameEngine import GameEngine

from lib.models.v1.UsernameModel import UsernameModel
from lib.models.v1.CreateGameRoomModel import CreateGameRoomModel
from lib.models.v1.GameModel import GameModel
from lib.models.v1.GameInputModel import GameInputModel
from lib.models.v1.DeckModel import DeckModel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from lib.models.v1.AllModel import AllModel

mainApp = FastAPI()

mainApp.mount("/static", StaticFiles(directory="static"), name="static")

def getDataStore():
    return RedisDataStore()

@mainApp.get("/")
def read_ui():
    return { "hello": "world" }

@mainApp.get("/api/v1/all")
def get_all():
    deck = DeckModel()
    deck.populate(1)
    resp = AllModel(version="1.0.0", deck_model=deck)
    return resp

@mainApp.post("/api/v1/process")
def post_process(gameInput: GameInputModel):
    engine = GameEngine()
    data_store = getDataStore()
    game_model = data_store.get_game_model(gameInput.game_id)
    anychanges, game_model = engine.process(game_model, gameInput)

    if anychanges:
        data_store.save_game_model(game_model.game_id, game_model)
    
    return data_store.get_game_model(gameInput.game_id)

@mainApp.get("/api/v1/gamemodel/{game_id}")
def get_game_model(game_id: str):
    data_store = getDataStore()
    return data_store.get_game_model(game_id)

@mainApp.get("/api/v1/gamerooms")
def get_game_rooms():
    # TODO Finish this implementation
    return []

@mainApp.get("/api/v1/gamerooms/byusername/{username}")
def get_game_rooms(username: str):
    # TODO Finish this implementation
    return []

@mainApp.post("/api/v1/gamerooms")
def create_game_room(payload: CreateGameRoomModel):
    # TODO Finish this implementation
    return "OK"

@mainApp.post("/api/v1/gamerooms/{gameroom_name}/adduser")
def create_game_room(payload: UsernameModel):
    # TODO Finish this implementation
    return "OK"

@mainApp.post("/api/v1/gamerooms/{gameroom_name}/removeuser")
def create_game_room(payload: UsernameModel):
    # TODO Finish this implementation
    return "OK"

