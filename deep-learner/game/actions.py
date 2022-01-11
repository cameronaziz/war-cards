from typing import List, Optional

from game.card import Card, Ranks


class Action:
    card_played: Card
    chosen_opponent: Optional[int]
    chosen_opponent_card: Optional[Ranks]

    def __init__(
        self,
        idx: int,
        card_played: Card,
        chosen_opponent: Optional[int],
        chosen_opponent_card: Optional[Ranks],
    ):
        self.idx = idx
        self.card_played = card_played
        self.chosen_opponent = chosen_opponent
        self.chosen_opponent_card = chosen_opponent_card


class Actions:
    def __init__(self, players_count: int):
        self.players_count = players_count
        self.actions = Actions.create_actions(self.players_count)
        self.n = len(self.actions)

    @staticmethod
    def create_actions(players_count: int = 2):
        cards: List[Card] = []
        for idx, rank in enumerate(Ranks):
            card = Card(rank, idx)
            cards.append(card)

        idx = -1
        actions: List[Action] = []
        for card_played in cards:
            idx += 1
            no_choices = Action(idx, card_played, None, None)
            actions.append(no_choices)
            for chosen_opponent_index in range(players_count):
                idx += 1
                only_opponent = Action(idx, card_played, chosen_opponent_index, None)
                actions.append(only_opponent)
                for guessed_opponent_card in cards:
                    idx += 1
                    action = Action(
                        idx,
                        card_played,
                        chosen_opponent_index,
                        guessed_opponent_card.rank,
                    )
                    actions.append(action)
        return actions
