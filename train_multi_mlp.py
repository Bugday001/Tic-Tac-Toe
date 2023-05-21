import os
import sys
import numpy as np

from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

from custom_multi_mlp import TicEnv

# 创建环境实例
env = TicEnv()
env = ActionMasker(env, TicEnv.get_action_mask)
# 创建两个智能体：A和B，使用MaskablePPO算法，并指定各自的策略网络结构（可以自定义）
agent_a = MaskablePPO("MlpPolicy", env, verbose=1)
agent_b = MaskablePPO("MlpPolicy", env, verbose=1)

# 定义训练回调函数：在每个时间步更新对方的策略参数，并生成无效动作掩码（比如不能撞墙）
def callback_a(_locals, _globals):
  # 更新B的策略参数为A的策略参数（零和博弈中双方共享策略）
  agent_b.policy.load_state_dict(agent_a.policy.state_dict())

  
  # 设置A的无效动作掩码
  agent_a.set_invalid_action_mask(~agent_a.get_action_mask())

# 定义训练回调函数：类似于A，但是要注意B的动作空间是反向的（0-下，1-上，2-右，3-左）
def callback_b(_locals, _globals):
  # 更新A的策略参数为B的策略参数（零和博弈中双方共享策略）
  agent_a.policy.load_state_dict(agent_b.policy.state_dict())
  
  
  # 设置B的无效动作掩码
  agent_b.set_invalid_action_mask(~agent_b.get_action_mask())

# 训练两个智能体，指定训练步数和回调函数
agent_a.learn(total_timesteps=10000, callback=callback_a)
agent_b.learn(total_timesteps=10000, callback=callback_b)

# 测试两个智能体，观察他们的行为
obs = env.reset()
for i in range(10):
  action_a, _states = agent_a.predict(obs)
  action_b, _states = agent_b.predict(obs)
  obs, reward, done, info = env.step([action_a, action_b])
  print(f"Step {i}: A={action_a}, B={action_b}, reward={reward}, done={done}")
