# %% [markdown]
# <a href="https://colab.research.google.com/github/cameronaziz/war-cards/blob/main/deep-learner/main.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# %%


# %%
# Dependencies
import pickle
import random
from itertools import count
from os.path import dirname, exists
from typing import List

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from matplotlib import style
from pyfiglet import figlet_format
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras import optimizers
from tensorflow.python.keras.backend import dtype

# from google.colab import drive

# %%
# %tensorflow_version 2.x

# %%
# Config
opponent_count = 2
invalid_move = -100
dumb_move = 100
no_change = 100
bad_move = 100
kill_move = 100
win_move = 100
die_move = 100
# dumb_move = -25
# no_change = 0
# bad_move = -1
# kill_move = 1
# win_move = 10
# die_move = -10

# %%
use_g_drive = False
gdrive_storage_location = "/content/gdrive/"
gdrive_location = gdrive_storage_location + "My Drive/data/"
training_location = gdrive_storage_location + "My Drive/training/"
state_memory_location = "state_memory.obj"
action_memory_location = "action_memory.obj"
reward_memory_location = "reward_memory.obj"
terminal_memory_location = "terminal_memory.obj"
settings_memory_location = "settings.obj"
checkpoint_path = training_location + "cp.ckpt"
checkpoint_dir = dirname(checkpoint_path)

# %%
# Constants
counts = [4, 2, 2, 2, 2, 1, 1, 1]
players_count = opponent_count + 1
hand_possibilites = 15 * 14
players_indicies = [i for i in range(0, players_count)]

# %%
# Read and write to Google Drive


class GDrive:
    @staticmethod
    def mount():
        drive.mount(gdrive_storage_location)

    @staticmethod
    def write(data, file_name):
        filehandler = open(GDrive.file_name(file_name), "wb")
        pickle.dump(data, filehandler)
        filehandler.close()

    @staticmethod
    def read(file_name, safe=True):
        exists = GDrive.exists(file_name) if safe else True
        if exists == False:
            return None
        file = open(GDrive.file_name(file_name), "rb")
        object_file = pickle.load(file)
        file.close()
        return object_file

    @staticmethod
    def exists(file_name):
        return exists(GDrive.file_name(file_name))

    @staticmethod
    def file_name(file_name):
        return gdrive_location + file_name


if use_g_drive:
    GDrive.mount()

# %%
# Build permutations


def permutate(counts):
    permutatations = []
    ranks = []

    def build(lists, prefix=[]):
        if not lists:
            permutatations.append(tuple(prefix))
            return
        first = lists[0]
        rest = lists[1:]
        for item in first:
            build(rest, prefix + [item])

    for count in counts:
        amount = list(range(count + 1))
        ranks.append(amount)

    build(ranks)
    return permutatations


def compress(permutations):
    compressed = []
    start = 0
    for count in counts:
        items = permutations[start : start + count]
        filtered = list(filter(lambda played: played == 1, list(items)))
        compressed.append(len(filtered))
        start += count
    return tuple(compressed)


# %%
class Replay:
    def __init__(self, max_size, input_shape):
        self.mem_size = max_size
        self.mem_cntr = 0
        self.input_shape = input_shape

        self.state_memory = np.zeros((self.mem_size, *input_shape), dtype=np.int32)
        self.new_state_memory = np.zeros((self.mem_size, *input_shape), dtype=np.int32)

        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.bool)
        self.setup()

    def setup(self):
        if use_g_drive:
            saved = GDrive.read(settings_memory_location)
            if (
                saved == None
                or saved[0] != self.mem_size
                or saved[1] != self.input_shape
            ):
                self.write_settings()
                return
            self.mem_cntr = saved[2]
            state_memory = GDrive.read(state_memory_location)
            print(state_memory)
            action_memory = GDrive.read(action_memory_location)
            print(action_memory)
            reward_memory = GDrive.read(reward_memory_location)
            print(reward_memory)
            terminal_memory = GDrive.read(terminal_memory_location)
            print(terminal_memory)
            # if len(state_memory) > 0 \
            #     len(action_memory) > 0 and \
            #     len(reward_memory) > 0 and \
            #     len(terminal_memory) > 0:
            self.state_memory = state_memory
            self.action_memory = action_memory
            self.reward_memory = reward_memory
            self.terminal_memory = terminal_memory
            #   return
            # self.write_settings()

    def write_settings(self):
        settings = (self.mem_size, self.input_shape, self.mem_cntr)
        GDrive.write(settings, settings_memory)

    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = done

        self.mem_cntr += 1
        if self.mem_cntr % 50 == 0:
            self.g_drive_store()

    def g_drive_store(self):
        if use_g_drive:
            GDrive.write(self.state_memory, state_memory)
            GDrive.write(self.action_memory, action_memory)
            GDrive.write(self.reward_memory, reward_memory)
            GDrive.write(self.terminal_memory, terminal_memory)
            self.write_settings()

    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)

        states = self.state_memory[batch]
        states_ = self.new_state_memory[batch]
        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        dones = self.terminal_memory[batch]

        return states, actions, rewards, states_, dones


# %%
# Create Actions


class Actions:
    def __init__(self):
        cards = Deck.create_counts()
        actions = []
        for card_played in cards:
            actions.append((card_played, None, None))
            for chosen_opponent_index in range(players_count):
                actions.append((card_played, chosen_opponent_index, None))
                for guessed_opponent_card in cards:
                    actions.append(
                        (card_played, chosen_opponent_index, guessed_opponent_card)
                    )
        self.actions = actions
        self.n = len(actions)

    def key_to_action(self, index):
        return self.actions[index]

    def action_to_key(self, action):
        return self.actions.index(action)


# %%
class Deck:
    def __init__(self):
        self.redeal()
        # self.cards = Deck.shuffle()
        # self.ranks = [card['rank'] for card in self.cards]

    def redeal(self):
        self.cards = Deck.shuffle().copy()
        # self.ranks = [card['rank'] for card in self.cards]

    def in_deck(self) -> List[object]:
        in_deck = []
        for card in self.cards:
            if card["in_deck"] == True:
                in_deck.append(card)
        return in_deck

    def is_played_card(self, id):
        card = next(c for c in self.cards if c["id"] == id)
        if card["is_played"] == True:
            return 1
        return 0

    def played_cards(self):
        played = (
            self.is_played_card(0),
            self.is_played_card(1),
            self.is_played_card(2),
            self.is_played_card(3),
            self.is_played_card(4),
            self.is_played_card(5),
            self.is_played_card(6),
            self.is_played_card(7),
            self.is_played_card(8),
            self.is_played_card(9),
            self.is_played_card(10),
            self.is_played_card(11),
            self.is_played_card(12),
            self.is_played_card(13),
            self.is_played_card(14),
        )
        return played

    def played_rank_count(self, rank):
        cards = filter(
            lambda card: card["rank"] == rank and card["is_played"] == True, self.cards
        )
        return len(list(cards))

    def played_ranks(self):
        played = (
            self.played_rank_count(1),
            self.played_rank_count(2),
            self.played_rank_count(3),
            self.played_rank_count(4),
            self.played_rank_count(5),
            self.played_rank_count(6),
            self.played_rank_count(7),
            self.played_rank_count(8),
        )
        return played

    @staticmethod
    def check(amount, index):
        if amount > index:
            return 1
        return 0

    @staticmethod
    def fill(played_count, max):
        base = list(np.zeros(max))
        return [Deck.check(played_count, i) for i, x in enumerate(base)]

    def played_card_ranks(self, rank=None):
        items = self.played_ranks()

        ranks = (
            Deck.fill(items[0], 4)
            + Deck.fill(items[1], 2)
            + Deck.fill(items[2], 2)
            + Deck.fill(items[3], 2)
            + Deck.fill(items[4], 2)
            + Deck.fill(items[5], 1)
            + Deck.fill(items[6], 1)
            + Deck.fill(items[7], 1)
        )

        return tuple(ranks)

    @staticmethod
    def rank_counts(ranks):
        cards = filter(lambda played: played == 1, ranks)
        return len(list(cards))

    @staticmethod
    def cards_to_ranks(cards_copy):
        return [
            Deck.rank_counts(cards_copy[:4]),
            Deck.rank_counts(cards_copy[4:6]),
            Deck.rank_counts(cards_copy[6:8]),
            Deck.rank_counts(cards_copy[8:10]),
            Deck.rank_counts(cards_copy[10:12]),
            Deck.rank_counts(cards_copy[12:13]),
            Deck.rank_counts(cards_copy[13:14]),
            Deck.rank_counts(cards_copy[14:]),
        ]

    @staticmethod
    def ranks_to_key(ranks):
        one = (ranks[0] + 1) * 10000000
        two = (ranks[1] + 1) * 1000000
        three = (ranks[2] + 1) * 100000
        four = (ranks[3] + 1) * 10000
        five = (ranks[4] + 1) * 1000
        six = (ranks[5] + 1) * 100
        seven = (ranks[6] + 1) * 10
        eight = (ranks[7] + 1) * 1
        return one + two + three + four + five + six + seven + eight

    @staticmethod
    def key_to_ranks(key):
        one = (key // 10000000) - 1
        two = (key // 1000000) - 1
        three = (key // 100000) - 1
        four = (key // 10000) - 1
        five = (key // 1000) - 1
        six = (key // 100) - 1
        seven = (key // 10) - 1
        eight = (key % 10) - 1
        return (one, two, three, four, five, six, seven, eight)

    def draw(self):
        if len(self.in_deck()) == 0:
            return None
        card = self.in_deck()[0]
        card["in_deck"] = False
        return card

    def deal(self):
        hands = []
        for x in range(players_count):
            card = self.draw()
            hands.append((card, None))
        return hands

    @staticmethod
    def shuffle():
        cards = []
        rank = 1
        id = 0
        for amount in counts:
            for _ in range(amount):
                cards.append(
                    {"rank": rank, "in_deck": True, "is_played": False, "id": id}
                )
                id += 1
            rank += 1
        random.shuffle(cards)
        return cards

    @staticmethod
    def create_counts():
        cards = []
        for idx in range(len(counts)):
            cards.append(idx + 1)
        return cards


# %%
class Game_State:
    def __init__(self):
        self.player_index = 0
        self.build_players()

    def build_players(self):
        self.deck = Deck()
        self.deck.redeal()
        hands = self.deck.deal()
        self.players = []
        for idx in range(players_count):
            self.players.append(self.player(hands[idx]))

    def player(self, hand):
        return {"is_dead": False, "hand": hand}

    def current_player_draw(self):
        if len(self.deck.in_deck()) == 0:
            return False
        self.draw(self.player_index)
        return True

    def draw(self, index=None):
        player_index = self.player_index if index == None else index
        card = self.deck.draw()
        if card == None:
            return False
        first = self.players[player_index]["hand"][0]
        self.players[player_index]["hand"] = (first, card)
        return True

    def get_player_hand(self, player_index=None):
        index = self.player_index if player_index == None else player_index
        return self.players[index]["hand"]

    def get_rank(self, card):
        if card == None:
            return None
        return card["rank"]

    def get_player_ranks(self, card_rank=None, player_index=None):
        first, second = self.get_player_hand(player_index)
        first = self.get_rank(first)
        second = card_rank if second == None else second["rank"]
        ranks = [first]
        if second == None or first == None:
            ranks.append(second)
            return ranks
        if first > second:
            ranks.insert(0, second)
            return ranks
        ranks.append(second)
        return ranks

    def get_member_ranks(self, member_index: int):
        first, second = self.get_player_hand(member_index)
        second = second["rank"]
        ranks = [first["rank"]]
        if first["rank"] > second:
            ranks.insert(0, second)
            return ranks
        ranks.append(second)
        return ranks

    def get_current_state(self, card_rank):
        first, second = self.get_player_ranks(card_rank)
        hand = Game.hand_to_key((first, second))
        played = Deck.ranks_to_key(self.in_deck().played_ranks(card_rank))
        state = [hand, played]
        return state

    def reset(self):
        self.build_players()
        self.player_index = 0

    def get_played_obs(self, rank):
        return list(self.deck.played_card_ranks(rank))

    @staticmethod
    def get_card_obs(card):
        obs = np.zeros(8, dtype=np.int8).tolist()
        if card:
            obs[card - 1] = 1
        return obs

    def get_hand_obs(self, hand):
        first = Game_State.get_card_obs(hand[0])
        second = Game_State.get_card_obs(hand[1])
        obs = first
        for item in list(second):
            obs.append(item)
        return obs


# %%
class Game_Play:
    def __init__(self, state):
        self.game_state = state
        self.player_index = 0

    def next_player(self, player_index=None):
        index = self.player_index if player_index == None else player_index
        next_player = index + 1
        next_player_index = next_player % players_count
        if next_player_index == self.player_index:
            return None

        if self.game_state.players[next_player_index]["is_dead"]:
            return self.next_player(next_player_index)

        return next_player_index

    def progress_turn(self, actions, agent):
        next_player = self.next_player()

        # Everyone Dead
        if next_player == None:
            return True

        self.game_state.player_index = next_player

        card = self.game_state.deck.draw()

        # No more cards
        if card == None:
            return True

        current_player = self.game_state.players[next_player]
        remaining_card = current_player["hand"][0]
        self.game_state.players[next_player]["hand"] = (remaining_card, card)
        hand = current_player["hand"]
        hand_state = (hand[0]["rank"], hand[1]["rank"])

        hand = self.game_state.get_hand_obs(hand_state)
        played = self.game_state.get_played_obs(card["rank"])
        for item in played:
            hand.append(item)

        choice = agent.choose(hand)
        action = actions.key_to_action(choice)
        reward, done = self.play(action)

        if done == True:
            current_player["is_dead"] = True

        ## players turn again
        if next_player == self.game_state.player_index:
            return False

        return self.progress_turn(actions, agent)

    def has_card(self, card_rank):
        hand = self.game_state.get_player_hand()
        if hand[0] != None and hand[0]["rank"] == card_rank:
            return True
        if hand[1] != None and hand[1]["rank"] == card_rank:
            return True
        return False

    def discard_card(self, player_id):
        player_hand = self.game_state.players[player_id]["hand"]
        card = player_hand[0]
        card["is_played"] = True
        next_card = self.game_state.deck.draw()
        self.game_state.players[player_id]["hand"] = (next_card, None)

    def play_card(self, card_rank):
        player_hand = list(self.game_state.get_player_hand())
        first_card = player_hand[0]
        second_card = player_hand[1]
        played_card = first_card if first_card["rank"] == card_rank else second_card
        remaining_card = second_card if first_card["rank"] == card_rank else first_card
        played_card["is_played"] = True
        self.game_state.players[self.game_state.player_index]["hand"] = tuple(
            [remaining_card, None]
        )

    def play_swordsman(self, action, remaining_card):
        (card_rank, opponent, opponent_choice) = action
        opponent_card = self.game_state.players[opponent]["hand"][0]["rank"]
        if remaining_card["rank"] > opponent_card:
            # self.add_known_card(card_rank, opponent)
            return kill_move, False
        elif remaining_card["rank"] < opponent_card:
            return die_move, True
        else:
            return no_change, False

    def play_archer(self, action):
        (card_rank, opponent, opponent_choice) = action
        opponent_card = self.game_state.players[opponent]["hand"][0]["rank"]
        if opponent_choice == opponent_card:
            # self.add_known_card(card_rank, opponent)
            return kill_move, False
        else:
            return no_change, False

    def play(self, action):
        (card_rank, opponent, opponent_choice) = action

        # Did they choose themselves?
        if opponent_choice == self.game_state.player_index:
            return invalid_move, True

        if self.has_card(card_rank) == False:
            return invalid_move, True

        self.play_card(card_rank)
        remaining_card = self.game_state.get_player_hand()[0]
        self.game_state.players[self.game_state.player_index]["hand"] = tuple(
            [remaining_card, None]
        )

        # Are we out of cards?
        if remaining_card is None:
            return invalid_move, True
        # Archer
        if card_rank == 1:
            if opponent_choice == None or opponent == None:
                return invalid_move, True
            return self.play_archer(action)
        # Priest
        elif card_rank == 2:
            if opponent_choice != None or opponent == None:
                return invalid_move, True
            # self.add_known_card(card_rank, opponent)
            return no_change, False
        # Swordsman
        elif card_rank == 3:
            if opponent_choice != None or opponent == None:
                return invalid_move, True
            return self.play_swordsman(action, remaining_card)
        # Shieldwall
        elif card_rank == 4:
            if opponent != None or opponent_choice != None:
                return invalid_move, True
            return no_change, False
        # Engineer
        elif card_rank == 5:
            if opponent_choice != None or opponent == None:
                return invalid_move, True
            self.discard_card(opponent)
            return no_change, False
        # Merchant
        elif card_rank == 6:
            if opponent_choice != None or opponent == None:
                return invalid_move, True
            # self.add_known_card(card_rank, opponent)
            self.game_state.players[self.player_index]["hand"] = (
                self.game_state.players[opponent]["hand"][0],
                None,
            )
            self.game_state.players[opponent]["hand"] = (remaining_card, None)
            return no_change, False
        # Horseman
        elif card_rank == 7:
            if opponent != None or opponent_choice != None:
                return invalid_move, True
            return no_change, False
        # Crown
        elif card_rank == 8:
            if opponent != None or opponent_choice != None:
                return invalid_move, True
            return die_move, True
        else:
            return invalid_move, True


# %%
class Game:
    def __init__(self):
        self.game_state = Game_State()
        self.game_play = Game_Play(self.game_state)

    def end_game_reward(self):
        remaining_hand = self.game_state.players[0]["hand"]
        remaining_card = (
            remaining_hand[0] if remaining_hand[1] == None else remaining_hand[1]
        )

        won = True
        opponents = ""

        for idx, player in enumerate(self.game_state.players):
            if player["is_dead"]:
                opponents += "D"
                if len(self.game_state.players) != idx + 1:
                    opponents += " - "
                continue
            hand = player["hand"]
            card = hand[0] if hand[1] == None else hand[1]
            opponents += str(card["rank"])
            if len(self.game_state.players) != idx + 1:
                opponents += " - "
            if card == None:
                continue
            if card["rank"] > remaining_card["rank"]:
                won = False

        won_text = "WON" if won else "LOST"
        text = "{}: {}".format(won_text, remaining_card["rank"])
        print(figlet_format(text, font="starwars"))
        print(figlet_format(opponents, font="univers"))

        return 1000 if won == True else 0

    def get_observation(self, is_after, played_card=None):
        successful = True
        if played_card == None:
            successful = self.game_state.current_player_draw()
            # if successful == False:
            #   hand = self.game_state.get_hand_obs(hand_state)
            #   played = self.game_state.get_played_obs(rank)
            #   for item in played:
            #     hand.append(item)
            #   return hand, True

        rank = played_card if is_after == False else None
        hand_state = self.game_state.get_player_ranks(played_card)
        hand = self.game_state.get_hand_obs(hand_state)
        played = self.game_state.get_played_obs(rank)
        for item in played:
            hand.append(item)
        if successful == False:
            return hand, True
        return hand, False

    def reset(self):
        self.game_state.reset()

    def progress(self, actions, agent):
        return self.game_play.progress_turn(actions, agent)

    def step(self, action):
        hand = self.game_state.get_player_ranks()
        played = compress(self.game_state.deck.played_cards())
        state = (hand, played)
        reward, done = self.game_play.play(action)
        return state, reward, done

    def end_game(self, reward, done):
        return win_move, True

    def discard_card(self, player_id):
        player_hand = self.game_state.players[player_id]["hand"]
        card = player_hand[0]
        card["is_played"] = True
        next_card = self.deck.draw()
        self.game_state.players[player_id]["hand"] = (next_card, None)

    @staticmethod
    def hand_to_key(hand):
        first_card = 10 if hand[0] == None else hand[0] * 10
        second_card = 0 if hand[0] == None else hand[1]
        return first_card + second_card

    @staticmethod
    def key_to_hand(key):
        first_card = key // 10
        second_card = key % 10
        return (first_card, second_card)


# %%
class DDQN(keras.Model):
    def __init__(self, n_actions, fc1_dims, fc2_dims):
        super(DDQN, self).__init__()
        self.dense1 = keras.layers.Dense(fc1_dims, activation="relu")
        self.dense2 = keras.layers.Dense(fc2_dims, activation="relu")
        self.V = keras.layers.Dense(1, activation=None)
        self.A = keras.layers.Dense(n_actions, activation=None)

    def call(self, state):
        x = self.dense1(state)
        x = self.dense2(x)
        V = self.V(x)
        A = self.A(x)

        Q = V + (A - tf.math.reduce_mean(A, axis=1, keepdims=True))

        return Q

    def advantage(self, state):
        x = self.dense1(state)
        x = self.dense2(x)
        A = self.A(x)

        return A


# %%
class Agent:
    def __init__(
        self,
        lr,
        gamma,
        n_actions,
        epsilon,
        batch_size,
        input_dims,
        epsilon_dec=1e-3,
        eps_end=0.01,
        mem_size=1000000,
        fc1_dims=128,
        fc2_dims=128,
        replace=100,
    ):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_dec = epsilon_dec
        self.eps_min = eps_end
        self.replace = replace
        self.batch_size = batch_size

        self.learn_step_counter = 0
        self.memory = Replay(mem_size, input_dims)
        self.q_eval = DDQN(n_actions, fc1_dims, fc2_dims)
        self.q_next = DDQN(n_actions, fc1_dims, fc2_dims)

        self.q_eval.compile(optimizer=Adam(learning_rate=lr), loss="mean_squared_error")
        self.q_next.compile(optimizer=Adam(learning_rate=lr), loss="mean_squared_error")

    def store(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose(self, observation):
        if np.random.random() < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            state = np.array([observation])
            actions = self.q_eval.advantage(state)
            action = tf.math.argmax(actions, axis=1).numpy()[0]

        return action

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return

        if self.learn_step_counter % self.replace == 0:
            self.q_next.set_weights(self.q_eval.get_weights())

        states, actions, rewards, states_, dones = self.memory.sample_buffer(
            self.batch_size
        )

        q_pred = self.q_eval(states)
        q_next = self.q_next(states_)
        q_target = q_pred.numpy()
        max_actions = tf.math.argmax(self.q_eval(states_), axis=1)
        for idx, terminal in enumerate(dones):
            q_target[idx, actions[idx]] = rewards[idx] + self.gamma * q_next[
                idx, max_actions[idx]
            ] * (1 - int(dones[idx]))

        self.q_eval.train_on_batch(states, q_target)

        self.epsilon = (
            self.epsilon - self.eps_dec if self.epsilon > self.eps_min else self.eps_min
        )
        self.learn_step_counter += 1


# %%
def get_print_rank(card_list):
    for idx, item in enumerate(card_list):
        if item == 1:
            return idx + 1
    return "None"


def print_state(turn, start_observation, end_observation, action, reward, done):
    hand_first = start_observation[:8]
    rank_first = get_print_rank(hand_first)
    hand_second = start_observation[8:16]
    rank_second = get_print_rank(hand_second)
    played_start = start_observation[16:]
    played_end = end_observation[16:]
    print(
        "   Turn {} - Start {} Hand {} {} - Card Played {} - End {} Reward {} Done {}".format(
            turn,
            Deck.cards_to_ranks(played_start),
            rank_first,
            rank_second,
            action[0],
            Deck.cards_to_ranks(played_end),
            reward,
            done,
        )
    )


if __name__ == "__main__":
    tf.compat.v1.enable_eager_execution()
    # tf.compat.v1.disable_eager_execution()
    actions = Actions()
    env = Game()
    epsilon = 1.0
    gamma = 0.99
    learning_rate = 0.005
    batch_size = 64
    input_dims = [31]
    agent = Agent(
        lr=learning_rate,
        gamma=gamma,
        n_actions=actions.n,
        epsilon=epsilon,
        batch_size=batch_size,
        input_dims=input_dims,
    )

    n_games = 100000
    scores = []
    eps_history = []
    history = [-100]

    for i in range(n_games):
        done = False
        score = 0
        env.reset()
        turn = 0
        print("Episode {}".format(i))

        while not done:
            turn += 1
            start_observation, start_done = env.get_observation(True, None)
            if start_done == True:
                done = True
                reward = env.end_game_reward()
                score += reward
                agent.store(
                    start_observation, action_key, reward, start_observation, True
                )
                continue

            action_key = agent.choose(start_observation)
            action = actions.key_to_action(action_key)
            played = action[0]
            state, reward, done = env.step(action)
            score += reward
            end_observation, end_done = env.get_observation(done, action[0])
            print_state(turn, start_observation, end_observation, action, reward, done)
            is_done = end_done or done
            agent.store(start_observation, action_key, reward, end_observation, is_done)
            env.progress(actions, agent)
            agent.learn()
        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[-50:])
        one_plus = i + 1
        if one_plus % 50 == 0:
            score_color = "red" if avg_score < 0 else "green"
            print(figlet_format("Episode {}".format(i + 1), font="pawp"))
            print(figlet_format("Last 50 {}".format(avg_score), font="letters"))
            # cprint(figlet_format('Game {} \n'.format(i + 1), font='letters'), 'blue', None, attrs=['bold'])
            # cprint(figlet_format('{}'.format(avg_score), font='letters'), score_color, None, attrs=['bold'])
            history.insert(0, avg_score)
            print(history)
