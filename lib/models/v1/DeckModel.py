
from lib.models.v1.CardModel import CardModel
from typing import Optional
from pydantic import BaseModel

class DeckModel(BaseModel):
    cards: Optional[list] = []

    def populate(self, deck_count):
        self.cards = []

        for j in range(deck_count):
            self.cards.append(CardModel(number=0, color='r'))
            self.cards.append(CardModel(number=0, color='g'))
            self.cards.append(CardModel(number=0, color='b'))
            self.cards.append(CardModel(number=0, color='y'))

            for j in range(2):
                for i in range(1, 9 + 1):
                    for color in ['r', 'g', 'b', 'y']:
                        self.cards.append(CardModel(number=i, color=color))
                        
            for i in range(2):
                for color in ['r', 'g', 'b', 'y']:
                    CardModel(is_normal=False, is_draw_2=True, color=color)
                    CardModel(is_normal=False, is_reverse=True, color=color)
                    CardModel(is_normal=False, is_skip=True, color=color)
            
            for i in range(4):
                self.cards.append(CardModel(is_normal=False, is_wild=True, color='w'))
                self.cards.append(CardModel(is_normal=False, is_draw_4=True, is_wild=True, color='w'))

        pass
