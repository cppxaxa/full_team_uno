
from lib.models.v1.GameRoomModel import GameRoomModel
from pydantic import BaseModel

from typing import Optional

class GameModel(BaseModel):
    game_id: Optional[str] = ""
    whose_turn_index: Optional[int] = -1
    forward_direction: Optional[bool] = True
    deck_count: Optional[int] = -1
    game_ended: Optional[bool] = True
    participants_id_index_map: Optional[dict] = None
    participants_index_id_map: Optional[dict] = None
    participants_id_cards_map: Optional[dict] = None
    game_room: Optional[GameRoomModel] = None
    cards_used_map: Optional[dict] = None
    winner_id_list: Optional[list] = list()
    last_card_people: Optional[dict] = dict()

# TODO Finish this implementation

    def initialize(self, game_room, deck_count):
        pass
