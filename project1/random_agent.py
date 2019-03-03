class random_agent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space
        self.reward = 0
        self.actions_performed = 0
        

    # You should modify this function
    def act(self, observation, reward, done):
        return self.action_space.sample()