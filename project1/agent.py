import pdb
class Agent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space
        self.reward = 0
        self.actions_performed = 0
        self.state = [[0]*160] * 210
        self.p_x = 0
        self.p_y = 0
        self.r_x = 0
        self.r_y = 0
        #self.state = self.state * 210
    
    def summation_it(self, on):
        #print(on)
        sum_ = 0
        for li in on:
            sum_ += li
        if sum_ == 0:
            return 'B'
            #blank
        elif sum_ == 390:
            return 'W'
            #wall
        elif sum_ == 538:
            return 'S'
            #score
        elif sum_ == 513:
            print('player inserted')
            return 'P'
            #player
        else:
            #robot
            return 'R'

    def populate_state(self, observation):
        for row in range(len(observation)):
                for col in range(len(observation[row])):
                    self.state[row][col] = self.summation_it(observation[row][col])
        return self.state
        
        
    def get_position_of_agent(self):
        for row in range(len(self.state)):
            for col in range(len(self.state[row])):
                if self.state[row][col] == 'P':
                    print('player found',row,col)
                    return row,col
        return 0,0
    
    def get_position_robots(self, row, col):
        for row in range(len(self.state)):
            for col in range(len(self.state[row])):
                if self.state[row][col] == 'R':
                    print('robot found',row,col)
                    return row,col
        return 0,0

    # You should modify this function
    def act(self, observation, reward, done):
        self.actions_performed += 1
        self.reward += reward 
        # simple reflex agent, hence not storing the obervation 
        if self.actions_performed % 20 == 0:
            print('populating')
            self.state = self.populate_state(observation)
            if self.actions_performed == 20:
                f = open('sumsssss.txt','a')
                for row in range(len(self.state)):
                    for col in range(len(self.state[row])):
                        f.write(self.state[row][col])
                    f.write('\n')
                f.close()
            #print(self.state)
        
        if self.actions_performed > 19:
            p_x, p_y = self.get_position_of_agent()
            #print(p_x,p_y)
            if p_x != 0 and p_y != 0:
                p_x += 5
                r_x, r_y = self.get_position_robots(p_x,p_y)
                if r_x != 0 and r_y != 0:
                    slope = (r_y - p_y)/(r_x-p_x)
                    print('slope',slope)
            #print('reached here')
            return self.action_space.sample()
        else:
            return self.action_space.sample()

            


        #print(self.actions_performed,'actions performed')
        

