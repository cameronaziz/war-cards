from typing import Optional

from game.actions import Action
from game.card import Ranks
from game.deck import Deck
from game.players import Player, Players

invalid_move = -100
dumb_move = 0
no_change = 0
bad_move = 0
kill_move = 100
win_move = 1000
die_move = -1


class Game:
    def __init__(self, players: Players, deck: Deck):
        self.players = players
        self.deck = deck

    def player_has_card(self, current_player: Player, card_rank: Ranks):
        hand = current_player.get_observation()
        for card in hand:
            if card is None:
                continue
            if card.score == card_rank.value[0]:
                return True
        return False

    def is_correct_choices(self, action: Action, current_player: Player):
        card_played = action.card_played
        chosen_opponent = action.chosen_opponent
        chosen_opponent_card = action.chosen_opponent_card

        if current_player.idx == chosen_opponent:
            return False

        if card_played is None:
            return False
        if card_played.rank == Ranks.ARCHER:
            return chosen_opponent is not None and chosen_opponent_card is not None
        if card_played.rank == Ranks.PRIEST:
            return chosen_opponent is not None and chosen_opponent_card is None
        elif card_played.rank == Ranks.SWORDSMAN:
            return chosen_opponent is not None and chosen_opponent_card is None
        elif card_played.rank == Ranks.SHIELDWALL:
            return chosen_opponent is None and chosen_opponent_card is None
        elif card_played.rank == Ranks.ENGINEER:
            return chosen_opponent is not None and chosen_opponent_card is None
        elif card_played.rank == Ranks.MERCHANT:
            return chosen_opponent is not None and chosen_opponent_card is None
        elif card_played.rank == Ranks.HORSEMAN:
            return chosen_opponent is None and chosen_opponent_card is None
        elif card_played.rank == Ranks.KING:
            return chosen_opponent is None and chosen_opponent_card is None
        else:
            return False

    def is_targeted_shieldwall(self, action: Action, opponent: Optional[Player]):
        chosen_opponent = action.chosen_opponent
        if chosen_opponent is None or opponent is None:
            return True
        elif opponent.idx == chosen_opponent and opponent.is_shielded:
            return False
        else:
            return True

    def is_valid_move(
        self, action: Action, current_player: Player, opponent: Optional[Player]
    ):
        is_correct_choices = self.is_correct_choices(action, current_player)
        is_targeted_shieldwall = self.is_targeted_shieldwall(action, opponent)
        player_has_card = self.player_has_card(current_player, action.card_played.rank)
        return is_correct_choices and is_targeted_shieldwall and player_has_card

    def step(self, action: Action):
        card_rank = action.card_played.rank
        opponent = self.players.get_player(action.chosen_opponent)
        chosen_opponent_rank = action.chosen_opponent_card

        current_player = self.players.get_current_player()
        valid_move = self.is_valid_move(action, current_player, opponent)
        if not valid_move:
            return invalid_move, True, True

        # Archer
        if card_rank == Ranks.ARCHER:
            opponent_player = Players.is_player(opponent)
            opponent_card_rank = opponent_player.get_card().rank
            if chosen_opponent_rank == opponent_card_rank:
                # self.add_known_card(card_rank, opponent)
                return kill_move, False, False
            else:
                return no_change, False, False
        # Priest
        elif card_rank == Ranks.PRIEST:
            # self.add_known_card(card_rank, opponent)
            return no_change, False, False
        # Swordsman
        elif card_rank == Ranks.SWORDSMAN:
            opponent_player = Players.is_player(opponent)
            opponent_card_rank = opponent_player.get_card().score
            remaining_card_rank = current_player.get_card(card_rank).score
            if remaining_card_rank > opponent_card_rank:
                # self.add_known_card(card_rank, opponent)
                return kill_move, False, False
            elif remaining_card_rank < opponent_card_rank:
                return die_move, True, False
            else:
                return no_change, False, False
        # Shieldwall
        elif card_rank == Ranks.SHIELDWALL:
            current_player.set_shieldwall()
            return no_change, False, False
        # Engineer
        elif card_rank == Ranks.ENGINEER:
            opponent_player = Players.is_player(opponent)
            opponent_card = opponent_player.get_card()
            opponent_card.play()
            if opponent_card.rank == Ranks.KING:
                opponent_player.kill()
                return kill_move, False, False
            card = self.deck.draw()
            if card is None:
                opponent_player.kill()
                return kill_move, False, False
            opponent_player.hand.set(card)
            return no_change, False, False
        # Merchant
        elif card_rank == Ranks.MERCHANT:
            opponent_player = Players.is_player(opponent)
            opponent_card = opponent_player.get_card()
            remaining_card = current_player.get_card(card_rank)
            current_player.hand.set(opponent_card)
            opponent_player.hand.set(remaining_card)
            return no_change, False, False
        # Horseman
        elif card_rank == Ranks.HORSEMAN:
            remaining_card_rank = current_player.get_card(card_rank).rank
            if (
                remaining_card_rank == Ranks.KING
                or remaining_card_rank == Ranks.MERCHANT
            ):
                return invalid_move, True, False
            return no_change, False, False
        # Crown
        elif card_rank == Ranks.KING:
            return die_move, True, False
        else:
            return invalid_move, True, True
