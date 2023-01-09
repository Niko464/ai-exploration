import os
import sys

p = os.path.abspath("..")
sys.path.append(p)


import numpy as np
from common.neuralNetwork.ActivationFuncs import *
from src.MPRMember import *
from src.MPREnvironment import *
import time
import random
import numpy as np
import sys

# def print_modifications(frame, event, arg):
#     if event == 'call':
#         print(f'{frame.f_code.co_filename}:{frame.f_lineno}: {frame.f_code.co_name}')


# sys.settrace(print_modifications)

"""
Steps to take:
- Optimize environment
- Change observation for each player to use raytracing
- Implement PPO environment
"""
def main():
	amtPlayers = 1000
	ais = [None] * amtPlayers
	random.seed(10)
	np.random.seed(10)

	start = time.time()
	for i in range(amtPlayers):
		ais[i] = MPRMember(str(i), 1)
		ais[i].randomize()

	env = MPREnvironment(amtPlayers)
	observations = env.reset(shouldRender=False)
	done = False
	rewards = []
	datafromAi = [None] * amtPlayers
	while not done:
		for i in range(amtPlayers):
			datafromAi[i] = ais[i].predict(observations[i])
		observations, rewards, done, _ = env.step(datafromAi)
	end = time.time()
	print(f"Done ({round(end - start, 2)}s)")



if __name__ == "__main__":
	main()