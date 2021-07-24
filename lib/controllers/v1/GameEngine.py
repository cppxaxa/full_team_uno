
import random
from lib.models.v1.GameInputModel import GameInputModel
from lib.models.v1.GameModel import GameModel
from lib.models.v1.CardModel import CardModel

class GameEngine:

    def process(self, gameModel: GameModel, input: GameInputModel):
        if not self._is_rightful_player(gameModel, input):
            return False, gameModel

        user_cards_count = len(self._extract_cards_of_person(gameModel, input))
        if input.declares_last_card and user_cards_count == 2:
            return self._process_last_card_declaration(gameModel, input)

        if self._is_card_valid(gameModel, input.plays_card_uid):
            card:CardModel = self._extract_card(gameModel, input)

            if card.is_wild:
                success, gameModel = self._set_current_color(gameModel, input)
                if not success: False, gameModel
                return self._process_card(gameModel, input)

            if card.color != gameModel.current_color:
                if not self._is_card_with_same_color_or_wild_available(gameModel, input):
                    return self._process_card(gameModel, input)
                elif self._is_card_number_equals_last_card_if_available(gameModel, card):
                    return self._process_card(gameModel, input)
                return False, gameModel # Wait for the same color or wild card
            else:
                return self._process_card(gameModel, input)

        return False, gameModel # Invalid card to play with


    def _is_card_valid(self, gameModel: GameModel, card_uid):
        if card_uid == '': return False
        return card_uid in gameModel.cards_uid_used_map and (not gameModel.cards_played_map[card_uid])


    def _is_rightful_player(self, gameModel: GameModel, input: GameInputModel):
        expected_player = gameModel.participants_index_id_map[str(gameModel.whose_turn_index)]
        return expected_player == input.username


    def _process_last_card_declaration(self, gameModel: GameModel, input: GameInputModel):
        gameModel.last_card_people_map[input.username] = True
        return True, gameModel


    def _set_current_color(self, gameModel: GameModel, input: GameInputModel):
        if input.change_color_to in ['r', 'g', 'b', 'y']:
            gameModel.current_color = input.change_color_to
            return True, gameModel
        return False, gameModel


    def _is_card_with_same_color_or_wild_available(self, gameModel: GameModel, input: GameInputModel):
        card_uid_list = gameModel.participants_id_cards_map[input.username]
        cards_list = [gameModel.cards_sequence[gameModel.cards_uid_index_map[uid]] for uid in card_uid_list]
        return 0 < len([True for card in cards_list if card['color'] == "w" or card['color'] == gameModel.current_color])


    def _is_card_number_equals_last_card_if_available(self, gameModel: GameModel, card: CardModel):
        last_card_available = 0 < len(gameModel.cards_played_sequence)
        if last_card_available:
            lastCard:CardModel = CardModel.parse_obj(gameModel.cards_played_sequence[-1])
            return lastCard.number == card.number
        return False # If no last card


    def _process_card(self, gameModel: GameModel, input: GameInputModel):
        next_person_index = self._derive_next_person(int(gameModel.whose_turn_index), gameModel.forward_direction, gameModel.participants_index_id_map)
        card:CardModel = self._extract_card(gameModel, input)
        
        if card.is_reverse:
            gameModel.forward_direction = not gameModel.forward_direction
            next_person_index = self._derive_next_person(int(gameModel.whose_turn_index), gameModel.forward_direction, gameModel.participants_index_id_map)
        
        if card.is_skip:
            next_person_index = self._derive_next_person(next_person_index, gameModel.forward_direction, gameModel.participants_index_id_map)

        if card.is_draw_2:
            next_person = gameModel.participants_index_id_map[str(next_person_index)]
            gameModel = gameModel.assign_cards_to_username(next_person, 2)
        
        if card.is_draw_4:
            next_person = gameModel.participants_index_id_map[str(next_person_index)]
            gameModel = gameModel.assign_cards_to_username(next_person, 4)

        if (not self._is_person_in_last_card_participants(gameModel, input)) \
                and len(self._extract_cards_of_person(gameModel, input)) == 1:
            gameModel = gameModel.assign_cards_to_username(input.username, 2)
        
        if self._is_person_in_last_card_participants(gameModel, input) \
                and (card.is_wild or card.is_draw_2 or card.is_draw_4 or card.is_reverse or card.is_skip):
            gameModel = gameModel.assign_cards_to_username(input.username, 2)
        
        gameModel = self._remove_card_from_person(gameModel, input)

        if not card.is_wild:
            gameModel.current_color = card.color

        user_cards_count = len(self._extract_cards_of_person(gameModel, input))
        if user_cards_count == 0:
            gameModel.winner_id_list.append(input.username)
            gameModel = self._remove_user_from_participants(input.username, gameModel)
            del gameModel.last_card_people_map[input.username]
        elif user_cards_count > 1:
            if input.username in gameModel.last_card_people_map:
                del gameModel.last_card_people_map[input.username]
        
        gameModel.whose_turn_index = next_person_index
        return True, gameModel


    def _remove_user_from_participants(self, username: str, gameModel: GameModel):
        idx = gameModel.participants_id_index_map[username]
        del gameModel.participants_index_id_map[str(idx)]
        del gameModel.participants_id_cards_map[username]
        del gameModel.participants_id_index_map[username]
        return gameModel


    def _extract_cards_of_person(self, gameModel: GameModel, input: GameInputModel):
        cards_uid = gameModel.participants_id_cards_map[input.username]
        return [gameModel.cards_sequence[gameModel.cards_uid_index_map[uid]] for uid in cards_uid]


    def _remove_card_from_person(self, gameModel: GameModel, input: GameInputModel):
        card = self._extract_card(gameModel, input)
        gameModel.cards_played_map[card.unique_id] = True
        gameModel.cards_uid_used_map[card.unique_id] = True
        gameModel.cards_played_sequence.append(card)
        gameModel.participants_played_sequence.append(input.username)

        participants_cards_for_user = gameModel.participants_id_cards_map[input.username]
        gameModel.participants_id_cards_map[input.username] = [el for el in participants_cards_for_user if el != input.plays_card_uid]
        return gameModel


    def _is_person_in_last_card_participants(self, gameModel: GameModel, input: GameInputModel):
        username = input.username
        return username in gameModel.last_card_people_map


    def _derive_next_person(self, whose_turn_index, forward_direction, participants_index_id_map):
        # Turn every participants into 0th index (might have missing index values)
        # Find next index
        # Convert back the index into gameIndex

        game_index_to_0th_index_map = {}
        zeroth_index_to_game_index_map = {}
        remaining_game_index_list = sorted([el for el in participants_index_id_map])
        for idx, game_index in enumerate(remaining_game_index_list):
            zeroth_index_to_game_index_map[idx] = int(game_index)
            game_index_to_0th_index_map[int(game_index)] = idx

        next_index = game_index_to_0th_index_map[whose_turn_index]
        if forward_direction:
            next_index += 1
        else:
            next_index -= 1
        n = len(participants_index_id_map)
        if n < 0:
            next_index = next_index + n
        next_index = next_index % n
        return zeroth_index_to_game_index_map[next_index]


    def _extract_card(self, gameModel: GameModel, input: GameInputModel):
        return CardModel.parse_obj(gameModel.cards_sequence[gameModel.cards_uid_index_map[input.plays_card_uid]])
