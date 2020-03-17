import numpy as np
from dqn import Agent
import sky
#from utils import plotLearning

if __name__ == '__main__':
    env = sky.make()

    lr = 0.0005
    n_games = 100
    #ToDo: input_dims
    agent = Agent(gamma=0.99, epsilon=1.0, lr=lr, input_dims=[3],
                  n_actions=4, mem_size=1000000, batch_size=64)

    filename = 'lander.png'
    scores = []
    eps_history = []

    score = 0

    for i in range(n_games):
        done = False
        if i % 10 == 0 and i > 0:
            avg_score = np.mean(scores[max(0, i-10):(i+1)])
            print('episode', i, 'score', score, 'average score %.3f' % avg_score,
                  'epsilon %.3f' % agent.epsilon)
        else:
            print('episode', i, 'score', score)

        observation = env.reset()
        score = 0
        while not done:
            '''
            one game: ending, when done=True
            '''
            action = agent.choose_action(observation)
            print(action)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_,
                                   int(done))
            observation = observation_
            agent.learn()

        scores.append(score)
        eps_history.append(agent.epsilon)

    x = [i+1 for i in range(n_games)]
    #plotLearning(x, scores, eps_history, filename)