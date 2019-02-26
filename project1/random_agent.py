class random_agent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space
        self.reward = 0
        self.actions_performed = 0
        

    # You should modify this function
    def act(self, observation, reward, done):
        self.actions_performed += 1
        self.reward += reward 
        print(self.actions_performed,'actions performed')
        return self.action_space.sample()