from snake import Snake
# from mytry import Snake
import random
import numpy as np
from keras import Sequential
from collections import deque
from keras.layers import Dense
from keras.optimizers import adam_v2

class DeepQNetwork:
    def __init__(self, env):

        self.action_space = 4
        self.state_space = 12
        self.epsilon = 1
        self.decayEpsilon = .9 
        self.minEpsilon = .01
        self.gamma = .9
        self.batch = 300 
        self.learningRate = 0.001
        self.layers = [128, 128, 128]
        self.timestamp = deque(maxlen=2500)
        self.model = self.build_model()


    def build_model(self):
        model = Sequential()
        model.add(Dense(self.layers[0], input_shape=(self.state_space,), activation='relu'))
        model.add(Dense(self.layers[1], activation='relu'))
        model.add(Dense(self.layers[2], activation='relu'))
        model.add(Dense(self.action_space, activation='softmax'))
        model.compile(loss='mse', optimizer=adam_v2.Adam(lr=self.learningRate))
        return model


    def memory(self, state, action, reward, nextState, done):
        self.timestamp.append((state, action, reward, nextState, done))


    def action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        values = self.model.predict(state)
        return np.argmax(values[0])

    def replay(self):

        if len(self.timestamp) < self.batch:
            return
        clips = random.sample(self.timestamp, self.batch)
        states = np.array([i[0] for i in clips])
        actions = np.array([i[1] for i in clips])
        rewards = np.array([i[2] for i in clips])
        nextStates = np.array([i[3] for i in clips])
        dones = np.array([i[4] for i in clips])

        states = np.squeeze(states)
        nextStates = np.squeeze(nextStates)

        Q = rewards + self.gamma*(np.max(self.model.predict_on_batch(nextStates), axis=1))*(1-dones)
        FullQ = self.model.predict_on_batch(states)

        index = np.array([i for i in range(self.batch)])
        FullQ[[index], [actions]] = Q

        self.model.fit(states, FullQ, epochs=1, verbose=0)
        if self.epsilon > self.minEpsilon:
            self.epsilon *= self.decayEpsilon


print('test')
episode = 50
env_infos = {'States: only walls':{'state_space':'no body knowledge'}, 'States: direction 0 or 1':{'state_space':''}, 'States: coordinates':{'state_space':'coordinates'}, 'States: no direction':{'state_space':'no direction'}}
env = Snake()

print('test')
sumReward = []
agent = DeepQNetwork(env)
for e in range(episode):
    state = env.reset()
    state = np.reshape(state, (1, 12))
    score = 0

    for i in range(10000):
        action = agent.action(state)

        prev_state = state
        next_state, reward, done, _ = env.step(action)
        score += reward
        next_state = np.reshape(next_state, (1, 12))
        agent.memory(state, action, reward, next_state, done)
        state = next_state

        agent.replay()
        if done:
            print(f'Final state: {str(prev_state)}')
            print(f'Episode: {e+1}/{episode}, score: {score}')
            break
    sumReward.append(score)










    




  
    
