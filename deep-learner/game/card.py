from enum import Enum
from typing import Optional


class Ranks(Enum):
    ARCHER = (1, 4)
    PRIEST = (2, 2)
    SWORDSMAN = (3, 2)
    SHIELDWALL = (4, 2)
    ENGINEER = (5, 2)
    MERCHANT = (6, 1)
    HORSEMAN = (7, 1)
    KING = (8, 1)


class Position(Enum):
    DECK = 0
    HAND = 1
    PLAYED = 2


class Card:
    rank: Ranks
    idx: Optional[int]
    position: Position = Position.DECK

    def __init__(self, rank: Ranks, idx: Optional[int] = None):
        self.idx = idx
        self.rank = rank

    def play(self):
        self.position = Position.PLAYED

    def observation(self):
        base = [0, 0, 0, 0, 0, 0, 0, 0]
        base[self.score - 1] = 1
        return base

    score = property(lambda self: self.rank.value[0])
    amount = property(lambda self: self.rank.value[1])


def get_card_rank(card: Optional[Card]):
    if card is None:
        return None
    return card.rank.name


def get_card_value(card: Optional[Card]):
    if card is None:
        return 0
    return card.score
