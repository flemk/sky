import numpy as np
from dqn import Agent
import sky
import matplotlib.pyplot as plt

'''
This does something
'''

# [1] Defining the dqn parameters
imput_dimensions = 14
n_actions = 5 #aka output
epsilon = 1.0
gamma = 0.99
lr = 0.0005
mem_size = 1000000
batch_size = 64

# [2] Load presaved model
load_checkpoint = True
save_checkpoint = True

# [3] Training parameters
n_games = 10000
filename = 'lander.png'

if __name__ == '__main__':
    scores = []
    eps_history = []
    info_history = []
    env = sky.make(random=True, xi=(100,650-25), yi=(100,300-25), width=25, height=25)
    agent = Agent(gamma=gamma, epsilon=epsilon, lr=lr, input_dims=[imput_dimensions],
                  n_actions=n_actions, mem_size=mem_size, batch_size=batch_size)

    if (load_checkpoint):
        agent.load_modes()

    for i in range(n_games):
        score = 0
        done = False
        observation = env.reset()
        while not done:
            '''
            one game: ending, when done=True
            '''
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_,
                                   int(done))
            observation = observation_
            agent.learn()

        if i % 10 == 0 and i > 0:
            avg_score = np.mean(scores[max(0, i-10):(i+1)])
            print(i, 'episode', info, '|| score:', score, '| average score: %.3f' % avg_score,
                  '| epsilon: %.3f' % agent.epsilon, '| training done:', round(i/n_games, 2))
        else:
            print(i, 'episode', info, '|| score:', score)

        scores.append(score)
        eps_history.append(agent.epsilon)
        info_history.append(info)

    print('training ended with:', [[el, info_history.count(el)] for el in ('crashed', 'goal')])

    if (save_checkpoint):
        agent.save_models()
        print('[+] model saved')

    # -------------------
    # Plotting and output
    # -------------------
    x = [i+1 for i in range(n_games)]

    # First axis: Scores
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Episode')
    ax1.set_ylabel('score per Episode', color=color)
    ax1.plot(x, scores, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Second axis: epsilon
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('epsilon', color=color)  # we already handled the x-label with ax1
    ax2.plot(x, eps_history, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Output
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(filename)