import numpy as np
import tensorflow as tf
from pyfiglet import figlet_format

from game import Actions, Env, Observation
from ml import Agent, graph
from utils.print import print_state

opponent_count = 2
players_count = opponent_count + 1
start_player = 0

if __name__ == "__main__":
    tf.compat.v1.enable_eager_execution()
    actions = Actions(players_count)

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

    env = Env(players_count, start_player, agent, actions)
    n_games = 100000
    scores = np.zeros(n_games)
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
            end_game, current_player, draw_card = env.start_turn()
            played, hand = env.get_observation()
            observation = Observation.convert_raw(hand, played)
            if end_game is not None:
                reward, done = end_game
                agent.store(observation, observation, -1, reward, done)
            action_idx = agent.choose(observation)
            action = actions.actions[action_idx]
            reward, done, _invalid = env.step(action)
            score += reward
            end_observation = env.get_observation()
            print_state(turn, draw_card, played, hand, action, reward, done)
            played_, hand_ = env.get_observation()
            observation_ = Observation.convert_raw(hand_, played_)
            agent.store(observation, observation_, action_idx, reward, done)
            if not done:
                env.end_turn(action.card_played.rank)
            agent.learn()
            if not done:
                done = env.progress_turn()
        eps_history.append(agent.epsilon)
        scores[i] = score

        last_fifty = scores[max(0, i - 50) : i + 1]
        avg_score = np.mean(last_fifty)
        one_plus = i + 1
        if one_plus % 50 == 0:
            score_color = "red" if avg_score < 0 else "green"
            print(figlet_format("Episode {}".format(i + 1), font="pawp"))
            print(figlet_format("Last 50: {}".format(avg_score), font="small"))
            history.insert(0, avg_score)
            print(history)
            # graph(scores)
