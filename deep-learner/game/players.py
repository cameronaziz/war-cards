from enum import Enum
from typing import List, Optional

from game.card import Card, Ranks, get_card_rank, get_card_value
from game.deck import Deck


class State(Enum):
    TURN = 0
    WAIT = 1
    DEAD = 2


class Player_Hand:
    def __init__(self, first_card: Optional[Card], second_card: Optional[Card]):
        self.first_card = first_card
        self.second_card = second_card

    def get_observation(self):
        rank_1 = get_card_value(self.first_card)
        rank_2 = get_card_value(self.second_card)
        first = self.first_card if rank_1 < rank_2 else self.second_card
        second = self.second_card if rank_1 < rank_2 else self.first_card
        return [first, second]

    def full_hand(self):
        return self.first_card is not None and self.second_card is not None

    def add_card(self, card: Optional[Card]):
        if self.full_hand():
            raise Exception(
                "Player already has 2 cards {} {}".format(
                    get_card_rank(self.first_card), get_card_rank(self.second_card)
                )
            )
        if self.first_card is None:
            self.first_card = card
        else:
            self.second_card = card

    def play_card(self, card_rank: int):
        if self.first_card is not None and self.first_card.score == card_rank:
            self.first_card.play()
            self.first_card = None
        elif self.second_card is not None and self.second_card.score == card_rank:
            self.second_card.play()
            self.second_card = None

    def get_cards(self):
        cards: List[Card] = []
        if self.first_card is not None:
            cards.append(self.first_card)
        if self.second_card is not None:
            cards.append(self.second_card)
        return cards

    def set(self, first_card: Optional[Card], second_card: Optional[Card] = None):
        self.first_card = None
        self.second_card = None
        self.first_card = first_card
        self.second_card = second_card


class Player:
    hand: Player_Hand
    state: State
    is_shielded = False

    def __init__(self, card: Optional[Card], idx: int, state: Optional[State]):
        self.state = state if state is not None else State.WAIT
        self.hand = Player_Hand(card, None)
        self.idx = idx

    def set_shieldwall(self, is_shielded: Optional[bool] = True):
        self.is_shielded = is_shielded

    def add_card(self, card: Optional[Card]):
        self.hand.add_card(card)

    def current_cards(self, excluded_card: Optional[Ranks] = None):
        cards = self.hand.get_cards()
        current_cards: List[Card] = []
        has_excluded = False
        for card in cards:
            if card is not None:
                if card.rank == excluded_card and not has_excluded:
                    has_excluded = True
                else:
                    current_cards.append(card)
        return current_cards

    def get_card(self, excluded_card: Optional[Ranks] = None):
        cards = self.current_cards(excluded_card)
        if len(cards) > 1 and excluded_card is not None:
            raise Exception("Player has more than 1 card")
        if len(cards) == 0:
            cards = self.current_cards()
            ranks: List[Ranks] = []
            for card in cards:
                if card is not None:
                    ranks.append(card.rank)
            raise Exception(
                "Player has no card, hand {}, excluded_card {}".format(
                    ranks, excluded_card
                )
            )
        return cards[0]

    def get_observation(self):
        hand = self.hand.get_observation()
        return hand

    def kill(self):
        self.state = State.DEAD


class Players:
    def __init__(self, deck: Deck, players_count: int, start_player: int):
        self.deck = deck
        self.start_player = start_player
        self.n = players_count

        self.players: List[Optional[Player]] = [None for _ in range(self.n)]

    def reset(self):
        for idx, _ in enumerate(self.players):
            card = self.deck.draw()
            state = State.TURN if idx == self.start_player else State.WAIT

            playerInstance = Player(
                card,
                idx,
                state,
            )
            self.players[idx] = playerInstance

    @staticmethod
    def is_player(player: Optional[Player], error_message: Optional[str] = None):
        if player is None:
            message = error_message if error_message is not None else "Player is None"
            raise Exception(message)
        return player

    def get_current_player(self):
        for idx in range(len(self.players)):
            player = Players.is_player(
                self.players[idx],
                "Players.get_player received invalid index of {}".format(idx),
            )
            if player.state == State.TURN:
                return player
        raise Exception("Players.current_player: No current player")

    def draw(self):
        current_player = self.get_current_player()
        card = self.deck.draw()
        if card == None:
            return False
        current_player.add_card(card)
        return True

    def get_next_player(self):
        return self.get_offset_player(1)

    def get_previous_player(self):
        return self.get_offset_player(-1)

    def set_to_next_player(self):
        next_player = self.get_next_player()
        current_player = self.get_current_player()
        current_player.state = State.WAIT
        next_player.state = State.TURN
        return next_player

    def get_player(self, idx: Optional[int] = None):
        if idx is None:
            return None
        return Players.is_player(
            self.players[idx],
            "Players.get_player received invalid index of {}".format(idx),
        )

    def get_offset_player(self, offset: int = 0):
        for i in range(self.n):
            player = Players.is_player(self.players[i])
            if player.state == State.TURN:
                next_idx = (i + offset) % self.n
                return Players.is_player(self.players[next_idx])
        raise Exception("Players.get_offset_player: No current player")

    def get_observation(self):
        current_player = self.get_current_player()
        hand = current_player.get_observation()
        return hand
