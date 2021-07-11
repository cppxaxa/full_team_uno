
from typing import Optional
from pydantic import BaseModel

from lib.models.v1.CardModel import CardModel

class GameInputModel(BaseModel):
    username: Optional[str] = ""
    plays_card_uid: Optional[str] = ""
    declares_last_card: Optional[bool] = False
    change_color_to: Optional[str] = ''
