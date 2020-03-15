import gym
from dqn import Agent
from utils import plotLearning
#from gym import wrappers

if __name__ == '__main__':
    env = gym.make('LunarLander-v2')
    lr = 0.0005
    n_games = 100
    agent = Agent(gamma=0.99, epsilon=1.0, lr=lr, input_dims=[8],
                  n_actions=4, mem_size=1000000, batch_size=64)

    filename = 'lunarlander.png'
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
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_,
                                   int(done))
            observation = observation_
            agent.learn()

        scores.append(score)
        ep_history.append(agent.epsilon)

    x = [i+1 for i in range(n_games)]
    plotLearning(x, scores, eps_history, filename)

