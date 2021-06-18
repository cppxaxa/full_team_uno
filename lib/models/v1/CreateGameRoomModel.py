
from pydantic import BaseModel

class CreateGameRoomModel(BaseModel):
    username: str
    gameroom_name: str
