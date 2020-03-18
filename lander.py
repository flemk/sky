import numpy as np
from dqn import Agent
import sky
#from utils import plotLearning
import matplotlib.pyplot as plt

if __name__ == '__main__':
    env = sky.make()

    lr = 0.0005
    n_games = 500
    #ToDo: input_dims
    agent = Agent(gamma=0.99, epsilon=1.0, lr=lr, input_dims=[34],
                  n_actions=5, mem_size=1000000, batch_size=64)

    agent.load_modes()
    filename = 'lander.png'
    scores = []
    eps_history = []

    score = 0

    for i in range(n_games):
        done = False
        if i % 10 == 0 and i > 0:
            avg_score = np.mean(scores[max(0, i-10):(i+1)])
            print('episode:', i, '| score:', score, '| average score: %.3f' % avg_score,
                  '| epsilon: %.3f' % agent.epsilon)
        else:
            print('episode:', i, '| score:', score)

        observation = env.reset()
        #print('observation:', observation)
        score = 0
        t = 0
        while not done:
            '''
            one game: ending, when done=True
            '''
            action = agent.choose_action(observation)
            #print('action:', action)
            observation_, reward, done, info = env.step(action)
            #print('observation_:', observation_)
            #print('done:', done)
            score += reward
            agent.store_transition(observation, action, reward, observation_,
                                   int(done))
            observation = observation_
            agent.learn()

        print('info:', info)

        scores.append(score)
        eps_history.append(agent.epsilon)

    x = [i+1 for i in range(n_games)]
    #plotLearning(x, scores, eps_history, filename)
    plt.plot(x, scores)
    plt.plot(x, eps_history)
    plt.savefig(filename)
    agent.save_models()