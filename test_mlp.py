import time
import random

from sb3_contrib import MaskablePPO

from custom_wrapper_mlp import TicEnv
from TicTacToe_alpha_beta import alpha_ai

MODEL_PATH = r"trained_models_mlp/ppo_snake_187500_steps"

NUM_EPISODE = 10

RENDER = True
FRAME_DELAY = 0.05 # 0.01 fast, 0.05 slow
ROUND_DELAY = 5

seed = random.randint(0, 1e9)
print(f"Using seed = {seed} for testing.")


if RENDER:
    env = TicEnv(seed=seed, limit_step=False, silent_mode=False, isTrain=False)
else:
    env = TicEnv(seed=seed, limit_step=False, silent_mode=True, isTrain=False)

# Load the trained model
model = MaskablePPO.load(MODEL_PATH)

total_reward = 0
total_score = 0
min_score = 1e9
max_score = 0

for episode in range(NUM_EPISODE):
    obs = env.reset()
    episode_reward = 0
    done = False
    
    num_step = 0
    info = None

    sum_step_reward = 0

    retry_limit = 9
    print(f"=================== Episode {episode + 1} ==================")
    alpha = alpha_ai()
    step_counter = 0
    while not done:
        if env.game.player == 1:
            action, _ = model.predict(obs, action_masks=env.get_action_mask())

            num_step += 1

            obs, reward, done, info = env.step(action)
            
        elif env.game.player == -1:
            x, y = alpha.ai_move(env.game.g_map)
            print(x, y)
            env.game.step([x, y])
            env.game.player = 1
        if RENDER:
            env.render()
            time.sleep(FRAME_DELAY)
    
    if RENDER:
        time.sleep(ROUND_DELAY)

env.close()
