# from pyfiglet import figlet_format

from typing import List

from ml import Agent

from game.actions import Action, Actions
from game.card import Ranks
from game.deck import Deck
from game.game import Game
from game.observation import Observation
from game.players import Player, Players, State


class Env:
    def __init__(
        self, players_count: int, start_player: int, agent: Agent, actions: Actions
    ):
        self.agent = agent
        self.actions = actions
        self.start_player = start_player
        self.deck = Deck()
        self.players = Players(self.deck, players_count, start_player)
        self.game = Game(self.players, self.deck)

    def reset(self):
        self.deck.reset()
        self.players.reset()

    def step(self, action: Action):
        return self.game.step(action)

    def end_game(self):
        alive_players = self.get_alive_players()
        player_alive = alive_players[self.start_player]

        if player_alive is None:
            return -1, True

        player_card_score = player_alive.get_card().score

        for alive in alive_players:
            alive_card_rank_value = alive.get_card().score
            if alive_card_rank_value > player_card_score:
                return -1, True

        return 1, True

    def get_alive_players(self):
        alive: List[Player] = []
        for player in self.players.players:
            if player is None:
                continue
            if player.state != State.DEAD:
                alive.append(player)
        return alive

    def one_alive_player(self):
        alive_players = self.get_alive_players()
        return len(alive_players) == 1

    def no_cards_left(self):
        return self.deck.is_empty()

    def check_end_game(self):
        return self.one_alive_player() and self.no_cards_left()

    def start_turn(self):
        current_player = self.players.get_current_player()
        current_player.set_shieldwall(False)
        is_end_game = self.check_end_game()
        if is_end_game:
            return self.end_game(), current_player, None
        current = self.players.get_current_player()
        card = self.deck.draw()
        current.add_card(card)
        return None, current_player, card

    def end_turn(self, played_card: Ranks):
        current_player = self.players.get_current_player()
        current_player.hand.play_card(played_card.value[0])

    def progress_turn(self):
        while True:
            next_player = self.players.set_to_next_player()
            if next_player.idx == self.start_player:
                break
            if next_player.state == State.DEAD:
                continue
            end_game, _current_player, draw_card = self.start_turn()
            if end_game is not None:
                rank = "" if draw_card is None else draw_card.rank.value[0]
                print(
                    "Player {} drew {} and triggered end game".format(
                        next_player.idx,
                        rank,
                    )
                )
                return True
            played, hand = self.get_observation()
            observation = Observation.convert_raw(hand, played)
            action_idx = self.agent.choose(observation)
            action = self.actions.actions[action_idx]
            _reward, done, invalid = self.step(action)
            invalid_text = ", invalid move" if invalid else ""
            print(
                "Player {} played {} {}".format(
                    next_player.idx, action.card_played.rank, invalid_text
                )
            )
            if invalid:
                return True
            if not done:
                self.end_turn(action.card_played.rank)
        return False

    def get_observation(self):
        first_card, second_card = self.players.get_observation()
        hand = [first_card, second_card]
        played = self.deck.get_observation()
        return played, hand
