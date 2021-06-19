
from pydantic import BaseModel

class CreateGameRoomModel(BaseModel):
    gameroom_name: str
    password: str
