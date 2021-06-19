
from pydantic import BaseModel

class StartGameRequestModel(BaseModel):
    deck_count: int
