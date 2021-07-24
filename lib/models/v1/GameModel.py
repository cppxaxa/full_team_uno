
from lib.models.v1.GameRoomModel import GameRoomModel
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
    cards_sequence: Optional[list] = []
    cards_played_sequence: Optional[list] = []
    participants_played_sequence: Optional[list] = []
    cards_uid_index_map: Optional[dict] = {}
    cards_uid_used_map: Optional[dict] = {}
    cards_played_map: Optional[dict] = {}
    winner_id_list: Optional[list] = []
    last_card_people_map: Optional[dict] = {}

# TODO Validation req. Finish this implementation

    def initialize(self, game_room: GameRoomModel, deck_count):
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
        self.cards_sequence = []
        for idx, card in enumerate(deck.cards):
            self.cards_sequence.append(card)
            self.cards_uid_used_map[card.unique_id] = False
            self.cards_uid_index_map[card.unique_id] = idx
            self.cards_played_map[card.unique_id] = False
        
        self.assign_cards(game_room.participants, self.cards_uid_used_map)

        
    # TODO Fix this
    def id_generator(size=15, chars=string.ascii_uppercase + string.digits):
        return '123456789012345'
        return ''.join(random.choice(chars) for _ in range(size))
    
    def populate_participants(self, participant_list):
        for idx, username in enumerate(participant_list):
            self.participants_id_index_map[username] = idx
            self.participants_index_id_map[idx] = username
    
    def assign_cards(self, participants_id_list, cards_uid_used_map, card_count=7, reset_existing=True):
        card_uid_list = [uid for uid in cards_uid_used_map if cards_uid_used_map[uid] == False]
        total_card_count = len(card_uid_list)
        cards_distributed_to_participants = []
        for id in participants_id_list:
            if reset_existing:
                self.participants_id_cards_map[id] = []
            for _ in range(card_count):
                if len(card_uid_list) == 0: raise("Insufficient unused cards in deck, participant=" + str(id) + ", total_cards=" + str(total_card_count) + ", cards_distributed_to_participants=" + str(cards_distributed_to_participants))
                card_uid = random.choice(card_uid_list)
                self.participants_id_cards_map[id].append(card_uid)
                cards_uid_used_map[card_uid] = True
                card_uid_list.remove(card_uid)
            cards_distributed_to_participants.append(id)


    def assign_cards_to_username(self, username, card_count):
        if username not in self.participants_id_index_map:
            raise("Invalid username")
        
        for _ in range(2):
            card_uid_list = [uid for uid in self.cards_uid_used_map if self.cards_uid_used_map[uid] == False]
            total_unused_card_count = len(card_uid_list)
        
            if total_unused_card_count < card_count:
                count = self._free_up_unallocated_played_card()
                if count < card_count:
                    raise("Scanning unallocated cards gave less than " + card_count)
            else:
                self.assign_cards([username], self.cards_uid_used_map, card_count=card_count, reset_existing=False)
                return self # To avoid any retry
        return self


    # TODO Complete the function
    def _free_up_unallocated_played_card(self):
        count = 0

        return count

