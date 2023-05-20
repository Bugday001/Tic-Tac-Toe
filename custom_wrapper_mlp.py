from socket import gaierror
import numpy as np
import time # For debugging.

import gym
import numpy as np

from TicTacToe_game import TicGame

class TicEnv(gym.Env):
    def __init__(self, seed=0, board_size=3, silent_mode=True, limit_step=True, isTrain=True):
        super().__init__()
        self.game = TicGame(seed=seed, board_size=board_size, silent_mode=silent_mode)
        self.game.reset()

        self.action_space = gym.spaces.Discrete(9) # 3x3
        
        self.observation_space = gym.spaces.Box(
            low=-1, high=1,
            shape=(self.game.cell_num, self.game.cell_num),
            dtype=np.int8
        ) # 0: empty, 0.5: snake body, 1: snake head, -1: food

        self.board_size = board_size
        self.grid_size = board_size ** 2 # Max length of snake is board_size^2
        # # self.max_growth = self.grid_size - self.init_snake_size
        self.isTrain = isTrain
        self.done = False

        if limit_step:
            self.step_limit = self.grid_size ** 2 / 2 + 1 # More than enough steps to get the food.
        else:
            self.step_limit = 1e9 # Basically no limit.
        self.reward_step_counter = 0

    def reset(self):
        self.game.reset()

        self.done = False
        self.reward_step_counter = 0

        obs = self._generate_observation()
        return obs
    
    def step(self, action):
        self.done, info = self.game.step([action//3, action%3]) # info = {"snake_size": int, "snake_head_pos": np.array, "prev_snake_head_pos": np.array, "food_pos": np.array, "food_obtained": bool}
        obs = self._generate_observation()
        if self.done == 0 and self.isTrain:
            # get the valid actions as a boolean array
            valid_actions = np.array([self.game._check_action_validity(a) for a in range(self.action_space.n)])
            # get the indices of the valid actions
            valid_indices = np.where(valid_actions)[0]
            # randomly choose one of the valid indices
            if valid_indices.size == 0:
                print(obs, self.done)
            action = np.random.choice(valid_indices)
            self.done, info = self.game.step([action//3, action%3]) # info = {"snake_size": int, "snake_head_pos": np.array, "prev_snake_head_pos": np.array, "food_pos": np.array, "food_obtained": bool}
            obs = self._generate_observation()

        reward = 0.0
        self.reward_step_counter += 1

        if self.reward_step_counter > self.step_limit: # Step limit reached, game over.
            self.reward_step_counter = 0
            self.done = 2
        
        if self.done == -1:
            reward = 10
        elif self.done == 1:
            reward = -10
        else:
            reward = 0

        reward = reward * 0.1 # Scale reward
        return obs, reward, self.done, info
    
    def render(self):
        self.game.render()

    def get_action_mask(self):
        return np.array([[self.game._check_action_validity(a) for a in range(self.action_space.n)]])
    
    def _generate_observation(self):
        obs = self.game.g_map
        return obs

# Test the environment using random actions
# NUM_EPISODES = 100
# RENDER_DELAY = 0.001
# from matplotlib import pyplot as plt

# if __name__ == "__main__":
#     env = TicEnv(silent_mode=False)
    
#     # Test Init Efficiency
#     # print(MODEL_PATH_S)
#     # print(MODEL_PATH_L)
#     num_success = 0
#     for i in range(NUM_EPISODES):
#         num_success += env.reset()
#     print(f"Success rate: {num_success/NUM_EPISODES}")

#     sum_reward = 0

#     # 0: UP, 1: LEFT, 2: RIGHT, 3: DOWN
#     action_list = [1, 1, 1, 0, 0, 0, 2, 2, 2, 3, 3, 3]
    
#     for _ in range(NUM_EPISODES):
#         obs = env.reset()
#         done = False
#         i = 0
#         while not done:
#             plt.imshow(obs, interpolation='nearest')
#             plt.show()
#             action = env.action_space.sample()
#             # action = action_list[i]
#             i = (i + 1) % len(action_list)
#             obs, reward, done, info = env.step(action)
#             sum_reward += reward
#             if np.absolute(reward) > 0.001:
#                 print(reward)
#             env.render()
            
#             time.sleep(RENDER_DELAY)
#         # print(info["snake_length"])
#         # print(info["food_pos"])
#         # print(obs)
#         print("sum_reward: %f" % sum_reward)
#         print("episode done")
#         # time.sleep(100)
    
#     env.close()
#     print("Average episode reward for random strategy: {}".format(sum_reward/NUM_EPISODES))
