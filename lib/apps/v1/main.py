
from lib.models.v1.UserModel import UserModel
from lib.models.v1.StartGameRequestModel import StartGameRequestModel
from lib.models.v1.GameRoomModel import GameRoomModel
from lib.controllers.v1.RedisDataStore import RedisDataStore
from lib.controllers.v1.GameEngine import GameEngine

from lib.models.v1.UsernameModel import UsernameModel
from lib.models.v1.CreateGameRoomModel import CreateGameRoomModel
from lib.models.v1.GameModel import GameModel
from lib.models.v1.GameInputModel import GameInputModel
from lib.models.v1.DeckModel import DeckModel
from fastapi import FastAPI, Response, status
from fastapi.staticfiles import StaticFiles

from lib.models.v1.AllModel import AllModel

mainApp = FastAPI()

mainApp.mount("/static", StaticFiles(directory="static"), name="static")

def getDataStore():
    return RedisDataStore()

@mainApp.get("/")
def read_ui():
    return { "hello": "world" }

@mainApp.post("/api/login")
def post_login(payload: UserModel):
    success, error = payload.is_valid()
    if not success:
        return error
    data_store = getDataStore()
    if payload.username.endswith("@beta"):
        # Auto register
        data_store.set_user_model(payload)
    val = data_store.get_user_model(payload.username)
    if val is not None and "passcode" in val:
        del val["passcode"]
    return val


@mainApp.get("/api/v1/all")
def get_all():
    deck = DeckModel()
    deck.populate(1)
    resp = AllModel(version="1.0.0", deck_model=deck)
    return resp

@mainApp.get("/api/v1/gamerooms")
def get_game_rooms():
    data_store = getDataStore()
    return data_store.get_all_game_rooms()

@mainApp.get("/api/v1/{username}/gamerooms")
def get_game_rooms(username: str):
    data_store = getDataStore()
    return data_store.get_game_rooms_by_username(username)

@mainApp.get("/api/v1/{username}/gamerooms/{gameroom_name}")
def get_game_rooms(username: str, gameroom_name: str):
    data_store = getDataStore()
    return data_store.get_game_rooms_by_username_and_name(username, gameroom_name)

@mainApp.post("/api/v1/{username}/gamerooms")
def create_game_room(username: str, payload: CreateGameRoomModel):
    game_room = GameRoomModel(name=payload.gameroom_name, \
        created_by=username, password=payload.password, participants=[])
    data_store = getDataStore()
    usermodel = data_store.get_user_model(username)
    success = usermodel.passcode == payload.password
    success = success and data_store.set_game_room_model(game_room)
    if success:
        return data_store.get_game_room_model(username, payload.gameroom_name)
    return "FAIL"

@mainApp.post("/api/v1/{username}/gamerooms/{gameroom_name}/adduser")
def add_user_to_game_room(username: str, gameroom_name: str, payload: UsernameModel):
    data_store = getDataStore()
    success, error = data_store.add_user_to_game_room(username, gameroom_name, payload.username)
    if success:
        return "OK"
    return error

@mainApp.post("/api/v1/{username}/gamerooms/{gameroom_name}/removeuser")
def remove_user_from_game_room(username: str, gameroom_name: str, payload: UsernameModel):
    data_store = getDataStore()
    success, error = data_store.remove_user_from_game_room(username, gameroom_name, payload.username)
    if success:
        return "OK"
    return error

@mainApp.post("/api/v1/{username}/gamerooms/{gameroom_name}/start")
def start_game_room(username: str, gameroom_name: str, payload: StartGameRequestModel):
    data_store = getDataStore()
    gameModel = GameModel()
    gameRoom = data_store.get_game_room_model(username=username, name=gameroom_name)
    gameModel.initialize(gameRoom, payload.deck_count)
    data_store.set_game_model(gameModel)
    return data_store.get_game_model(gameModel.game_id)

@mainApp.get("/api/v1/games/{game_id}")
def get_game_model(game_id: str):
    data_store = getDataStore()
    return data_store.get_game_model(game_id)

@mainApp.post("/api/v1/games/{game_id}/updategameroom")
def update_game_with_updated_gameroom(game_id: str):
    # TODO Finish this implementation - Re-align the game by add and remove players
    return "NotImplemented"

@mainApp.post("/api/v1/games/{game_id}/stop")
def stop_game(game_id: str):
    # TODO Finish this implementation
    return "NotImplemented"

@mainApp.post("/api/v1/games/{game_id}/process")
def post_process(game_id: str, gameInput: GameInputModel, response: Response):
    engine = GameEngine()
    data_store = getDataStore()
    game_model = data_store.get_game_model(game_id)
    anychanges, game_model = engine.process(game_model, gameInput)

    if anychanges:
        data_store.set_game_model(game_model)
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
    
    return data_store.get_game_model(game_model.game_id)

@mainApp.get("/api/v1/games/byusername/{username}")
def get_games(username: str):
    # TODO Finish this implementation
    return "NotImplemented"

