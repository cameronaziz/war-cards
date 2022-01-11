from typing import List, Optional, Tuple

from utils.observation import convert_to_observation

from game.card import Card, Ranks, get_card_value


class Observation:
    @staticmethod
    def convert_raw(hand: List[Optional[Card]], played: List[Tuple[Ranks, int]]):
        observation: List[int] = []
        hand_observation = Observation.hand_observation(hand)
        observation.extend(hand_observation)
        played_observation = Observation.played_observation(played)
        observation.extend(played_observation)
        return observation

    @staticmethod
    def played_observation(played: List[Tuple[Ranks, int]]):
        observation: List[int] = []
        for card in played:
            item = Observation.played_card_observation(card)
            observation.extend(item)
        return observation

    @staticmethod
    def played_card_observation(played: Tuple[Ranks, int]):
        card, count = played
        observation: List[int] = []
        for idx in range(card.value[1]):
            if idx + 1 <= count:
                observation.append(1)
            else:
                observation.append(0)
        return observation

    @staticmethod
    def hand_observation(hand: List[Optional[Card]]):
        observation: List[int] = []
        for card in hand:
            observation += Observation.card_observation(card)
        return observation

    @staticmethod
    def card_observation(card: Optional[Card]):
        value = get_card_value(card)
        return convert_to_observation(value, 8)
