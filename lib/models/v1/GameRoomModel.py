
from pydantic import BaseModel

class GameRoomModel(BaseModel):
    name: str
    created_by: str
    password: str
    participants: list
