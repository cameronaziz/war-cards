from typing import List, Optional, Tuple

from game import Action, Card, Ranks
from game.card import get_card_rank


def get_print_rank(card_list: List[int]):
    for idx, item in enumerate(card_list):
        if item == 1:
            return idx + 1
    return "None"


def get_action_text(action: Action):
    opponent_card = (
        "None"
        if action.chosen_opponent_card is None
        else action.chosen_opponent_card.name
    )

    opponent = 0 if action.chosen_opponent is None else action.chosen_opponent
    return "Played {} Opponent {} Pick {}".format(
        action.card_played.rank.name,
        opponent,
        opponent_card,
    )


def get_played_text(played: List[Tuple[Ranks, int]]):
    cards = ["{} {}".format(card.name, count) for card, count in played]
    text = ""
    for card in cards:
        text += card + " "
    return text


def get_hand_text(hand: List[Optional[Card]]):
    text = ""
    for card in hand:
        if card is None:
            text += "None "
        else:
            text += card.rank.name + " "
    return text


def print_state(
    turn: int,
    draw_card: Optional[Card],
    played: list[Tuple[Ranks, int]],
    hand: List[Optional[Card]],
    action: Action,
    reward: float,
    done: bool,
):
    draw_text = get_card_rank(draw_card)
    action_text = get_action_text(action)
    hand_text = get_hand_text(hand)
    played_text = get_played_text(played)
    print("   Turn {} Draw {}".format(turn, draw_text))
    print("      State {} Hand {}".format(played_text, hand_text))
    print("      {}".format(action_text))
    print("      Reward {} Done {}".format(reward, done))
