from random import randint

class only_shooting_agent(object):
    """Agent with unlimited supply of bullets"""
    done_ = 1
    def __init__(self, action_space):
        self.reward = 0
        self.actions_performed = 0
        # stores the available actions 
        '''
        ACTION_MEANING = {
    0 : "NOOP",
    1 : "FIRE",
    2 : "UP",
    3 : "RIGHT",
    4 : "LEFT",
    5 : "DOWN",
    6 : "UPRIGHT",
    7 : "UPLEFT",
    8 : "DOWNRIGHT",
    9 : "DOWNLEFT",
    10 : "UPFIRE",
    11 : "RIGHTFIRE",
    12 : "LEFTFIRE",
    13 : "DOWNFIRE",
    14 : "UPRIGHTFIRE",
    15 : "UPLEFTFIRE",
    16 : "DOWNRIGHTFIRE",
    17 : "DOWNLEFTFIRE",
}
        '''
        self.action_space = action_space
    
    def save_oberservation_to_text_file(self, observation):
        """
        function used to print the 2d matric to a file and try to analyse it
        :param observation:
        :return:
        """

        f = open('sums.txt','a')
        for rows in observation:
            for col in rows:
                f.write(str(str(self.summation_it(col))))
            f.write('\n')
        f.close()

    # You should modify this function
    def act(self, observation, reward, done):
        return randint(10, 17)


    def summation_it(self, on):
        print(on)
        sum = 0
        for li in on:
            sum += li
        if sum == 0:
            return 11
        elif sum == 390:
            return 22
        elif sum == 484:
            return 33
        elif sum == 513:
            return 44
        else:
            return 53