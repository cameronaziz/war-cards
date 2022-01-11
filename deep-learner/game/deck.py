import random
from typing import List, Optional, Tuple

from game.card import Card, Position, Ranks


class Deck:
    def __init__(self):
        total_card_count = 0
        for card_count in Ranks:
            _, count = card_count.value
            total_card_count += count
        self.total_card_count = total_card_count
        self.cards: List[Card] = []

    def reset(self):
        self.cards: List[Card] = []
        offset = 0
        for rank in Ranks:
            _, count = rank.value
            for idx in range(count):
                card_idx = offset + idx
                card = Card(rank, card_idx)
                self.cards.append(card)
            offset += count
        random.shuffle(self.cards)

    def get_observation(self):
        played: List[Ranks] = []
        for card in self.cards:
            if card.position == Position.PLAYED:
                played.append(card.rank)

        observation: List[Tuple[Ranks, int]] = []

        for rank in Ranks:
            observation.append((rank, 0))

        for rank in played:
            for idx, obs_rank in enumerate(observation):
                if obs_rank[0] == rank:
                    obs_rank = (obs_rank[0], obs_rank[1] + 1)
                    observation[idx] = obs_rank
        return observation

    def is_empty(self):
        for card in self.cards:
            if card is not None and card.position == Position.DECK:
                return False
        return True

    @staticmethod
    def shuffle(cards: List[Optional[Card]]):
        shuffled: List[Card] = []
        idx = -1
        for rank in Ranks:
            _, count = rank.value
            for _ in range(count):
                idx += 1
                card = Card(rank, idx)
                shuffled.append(card)
        random.shuffle(cards)
        return shuffled

    def next_card(self):
        for card in self.cards:
            if card is None:
                return None
            if card.position == Position.DECK:
                return card
        return None

    def draw(self):
        card = self.next_card()
        if card is None:
            return None
        card.position = Position.HAND
        return card

    @staticmethod
    def rank_counts(ranks: List[int]):
        cards = filter(lambda played: played == 1, ranks)
        return len(list(cards))

    @staticmethod
    def cards_to_ranks(cards: List[int]):
        return [
            Deck.rank_counts(cards[:4]),
            Deck.rank_counts(cards[4:6]),
            Deck.rank_counts(cards[6:8]),
            Deck.rank_counts(cards[8:10]),
            Deck.rank_counts(cards[10:12]),
            Deck.rank_counts(cards[12:13]),
            Deck.rank_counts(cards[13:14]),
            Deck.rank_counts(cards[14:]),
        ]
