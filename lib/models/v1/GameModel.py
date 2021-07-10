
from lib.models.v1.DeckModel import DeckModel
from pydantic import BaseModel

from typing import Optional

import string, random

class GameModel(BaseModel):
    game_id: Optional[str] = ''
    whose_turn_index: Optional[int] = -1
    current_color: Optional[str] = ''
    forward_direction: Optional[bool] = True
    deck_count: Optional[int] = -1
    game_ended: Optional[bool] = True
    participants_id_index_map: Optional[dict] = {}
    participants_index_id_map: Optional[dict] = {}
    participants_id_cards_map: Optional[dict] = {}
    game_room_name: Optional[str] = ''
    game_room_owner: Optional[str] = ''
    cards_used_map: Optional[dict] = {}
    cards_played_list: Optional[list] = []
    winner_id_list: Optional[list] = []
    last_card_people: Optional[dict] = {}

# TODO Validation req. Finish this implementation

    def initialize(self, game_room, deck_count):
        self.game_id = self.id_generator()
        self.game_room_name = game_room.name
        self.game_room_owner = game_room.created_by

        self.whose_turn_index = 0
        self.current_color = random.choice(['r', 'g', 'y', 'b'])
        self.forward_direction = True
        self.deck_count = deck_count
        self.game_ended = False
        
        self.populate_participants(game_room.participants)
        
        deck = DeckModel()
        deck.populate(deck_count)
        self.cards_used_map = {}
        for card in deck.cards:
            self.cards_used_map[card] = False
        
        self.assign_cards(game_room.participants, self.cards_used_map)

        
    # TODO Fix this
    def id_generator(size=15, chars=string.ascii_uppercase + string.digits):
        return '123456789012345'
        return ''.join(random.choice(chars) for _ in range(size))
    
    def populate_participants(self, participant_list):
        for idx, username in enumerate(participant_list):
            self.participants_id_index_map[username] = idx
            self.participants_index_id_map[idx] = username
    
    def assign_cards(self, participants_id_list, cards_used_map, card_count=7):
        card_list = [card for card in cards_used_map if cards_used_map[card] == False]
        total_card_count = len(card_list)
        cards_distributed_to_participants = []
        for id in participants_id_list:
            self.participants_id_cards_map[id] = []
            for i in range(card_count):
                if len(card_list) == 0: raise("Insufficient unused cards in deck, participant=" + str(id) + ", total_cards=" + str(total_card_count) + ", cards_distributed_to_participants=" + str(cards_distributed_to_participants))
                card = random.choice(card_list)
                self.participants_id_cards_map[id].append(card)
                cards_used_map[card] = True
                card_list.remove(card)
            cards_distributed_to_participants.append(id)
