
from lib.models.v1.DeckModel import DeckModel
from pydantic import BaseModel

from typing import Optional

from lib.models.v1.GameModel import GameModel
from lib.models.v1.UserModel import UserModel

class AllModel(BaseModel):
    version: Optional[str] = ""
    game_model: Optional[GameModel] = None
    current_user: Optional[UserModel] = None
    deck_model: Optional[DeckModel] = None
