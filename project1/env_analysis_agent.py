import argparse
import gym
from gym import wrappers, logger
import numpy

PLAYER_WIDTHPIXELS = 5
PLAYER_HEIGHTPIXELS = 20
PLAYER_WIDTH = 3
PLAYER_HEIGHT = 5
MAKE_ACTION = 10
PLAYER = 44
BLANK = 11
WALL = 22
ROBOT = 55
ROBOT_PIXELS = 72


class Agent(object):
    """The world's simplest agent!"""

    def __init__(self, action_space):
        self.skip = 2
        self.envrionment_representation = [[None]*160 for _ in range(210)]
        self.action_space = action_space
        self.actions_num = 0
        self.robot_count = 0
        # Increments at start too hence start with -1
        self.level_count = -1
        # Keeps track of which wall to move along
        self.wallToCheck = 'left'

    def formState(self, observation):
        sum_ = 0
        for value in observation:
            sum_ += value
        if sum_ == 0:
            return BLANK
        elif sum_ == 390:
            return WALL
        elif sum_ == 538:
            return 33
            # score
        elif sum_ == 513:
            return PLAYER
        else:
            self.robot_count += 1
            return ROBOT

    def transformEnvironment(self, observe):
        for row in range(len(observe)):
            for col in range(len(observe[row])):
                self.envrionment_representation[row][col] = int(self.formState(observe[row][col]))

    def getPlayerLocationInGrid(self):
        # this function can return incorrect player position as bullet also contains the same pixel value
        x , y = numpy.where(numpy.array(self.envrionment_representation) ==
                           PLAYER)
        if len(x) > 0 and len(y) > 0 :
            return x[0],y[0]
        else:
            return 0,0

    def wall_if_present_on_x_axis(self, player_x, player_y, robot_y):
        if robot_y < player_y:
            increment = -2
        else:
            increment = 2

        for i in range(player_y, robot_y + 1, increment):
            if self.envrionment_representation[player_x][i] == WALL:
                return True
        return False

    def wall_if_present_on_y_axis(self, player_x, player_y, robot_x):
        if robot_x < player_x:
            increment = -2
        else:
            increment = 2
        for i in range(player_x, robot_x + 1, increment):
            if self.envrionment_representation[i][player_y] == WALL:
                return True
        return False

    def checkForRobot(self, player_x, player_y):
        x,y = numpy.where(numpy.array(self.envrionment_representation) == ROBOT)
        xy = []
        if len(x) > 0 and len(y) > 0:
            xy = list(zip(x,y))

        for item in xy:
            if item[0] == player_x:
                if not self.wall_if_present_on_x_axis(player_x,player_y,item[1]):
                    return 'y', item[0], item[1]
            if item[1] == player_y:
                if not self.wall_if_present_on_y_axis(player_x,player_y,
                                                      item[0]):
                    return 'x', item[0], item[1]
        return 'not found', 0, 0


    def checkForDownWall(self, player_x, player_y):
        down_wall = 0
        buffer_pixels = 1

        x = player_x
        y = player_y

        # For bottom wall
        while self.envrionment_representation[x][y] == PLAYER:
            x += 1
        # At this point we are at the bottom extreme of the player
        if self.envrionment_representation[x + buffer_pixels][y] == WALL:
            down_wall = 1

        return down_wall

    def checkForUpWall(self, player_x, player_y):
        up_wall = 0
        buffer_pixels = 1

        x = player_x
        y = player_y

        # For top wall
        while self.envrionment_representation[x][y] == PLAYER:
            x -= 1
        # At this point we are at the top extreme of the player
        if self.envrionment_representation[x - buffer_pixels][y] == WALL:
            up_wall = 1

        return up_wall


    def checkForRightWall(self, player_x, player_y):
        right_wall = 0
        buffer_pixels = 4

        x = player_x
        y = player_y

        # For right wall
        while self.envrionment_representation[x][y] == PLAYER:
            y += 1
        # At this point we are at the right extreme of the player
        if self.envrionment_representation[x][y + buffer_pixels - 1] == BLANK and self.envrionment_representation[x][y + buffer_pixels] == WALL:
            right_wall = 1
        elif self.envrionment_representation[x][y + buffer_pixels] == BLANK:
            # If gap is not as big as player then its a wall
            count_pixels = 0

            while self.envrionment_representation[x][y + buffer_pixels] == BLANK:
                x += 1
                count_pixels += 1
                if count_pixels == PLAYER_HEIGHTPIXELS:
                    break

            if count_pixels < PLAYER_HEIGHTPIXELS:
                right_wall = 1

        return right_wall


    def checkForLeftWall(self, player_x, player_y):
        left_wall = 0
        buffer_pixels = 4

        x = player_x
        y = player_y

        # For left wall
        while self.envrionment_representation[x][y] == PLAYER:
            y -= 1

        # At this point we are at the left extreme of the player
        if self.envrionment_representation[x][y - buffer_pixels + 1] == BLANK and self.envrionment_representation[x][y - buffer_pixels] == WALL:
            # One left movement covers about 4 to 5 pixels of the foot hence we need to
            # maintain those many pixels in between which is 4 pixels from position considered (head top pixel).
            left_wall = 1
        elif self.envrionment_representation[x][y - buffer_pixels] == BLANK:
            # If gap is not as big as player then its a wall
            count_pixels = 0

            while self.envrionment_representation[x][y - buffer_pixels] == BLANK:
                x += 1
                count_pixels += 1
                if count_pixels == PLAYER_HEIGHTPIXELS:
                    break

            if count_pixels < PLAYER_HEIGHTPIXELS:
                left_wall = 1

        return left_wall


    def tryUpwards(self, up):
        if up == 0:
            # Move up
            action = 2
        else:
            # Move right
            action = 3
            # Set wall to move along as up
            self.wallToCheck = 'up'
        return action


    def tryDownwards(self, down):
        if down == 0:
            # Move down
            action = 5
        else:
            # Move left
            action = 4
            # Set wall to move along as down
            self.wallToCheck = 'down'
        return action


    def tryLeftMotion(self, left):
        if left == 0:
            # Move left
            action = 4
        else:
            # Move up
            action = 2
            # Set wall to move along as left
            self.wallToCheck = 'left'
        return action


    def tryRightMotion(self, right):
        if right == 0:
            # Move right
            action = 3
        else:
            # Move down
            action = 5
            # Set wall to move along as right
            self.wallToCheck = 'right'
        return action


    def determineMotion(self, player_x, player_y):
        # We move clockwise
        action = 0
        if self.wallToCheck == 'left':
            # Try to move along left wall by getting to it first and then up
            left = self.checkForLeftWall( player_x, player_y)

            if left == 0:
                # Move left
                action = 4
            else:
                # Move upwards if left wall present
                up = self.checkForUpWall( player_x, player_y)
                action = self.tryUpwards(up)

        elif self.wallToCheck == 'right':
            # Try to move along right wall by getting to it first and then down

            right = self.checkForRightWall( player_x, player_y)

            if right == 0:
                # Move right
                action = 3
            else:
                # Move downwards if right wall present
                down = self.checkForDownWall( player_x, player_y)
                action = self.tryDownwards(down)

        elif self.wallToCheck == 'up':
            # Try to move along top wall by getting to it first and then right

            up = self.checkForUpWall( player_x, player_y)

            if up == 0:
                # Move up
                action = 2
            else:
                # Move right if top wall present
                right = self.checkForRightWall( player_x, player_y)
                action = self.tryRightMotion(right)

        elif self.wallToCheck == 'down':
            # Try to move along bottom wall by getting to it first and then left

            down = self.checkForDownWall( player_x, player_y)

            if down == 0:
                # Move down
                action = 5
            else:
                # Move left if bottom wall present
                left = self.checkForLeftWall( player_x, player_y)
                action = self.tryLeftMotion(left)
        return action

    def fireAction(self,found, player_x,player_y,robot_x,robot_y):
        result = 0
        if found == 'x':
            #'Found vertically adjacent to player'
            if robot_x > player_x:
                result = 13  # downfire
            else:
                result = 10  # upfire
        elif found == 'y':
            # Found horizontally adjacent to player
            if robot_y > player_y:
                result = 11  # rightfire
            else:
                result = 12  # leftfir

        return result

    def act(self, observation, reward, done):
        self.actions_num += 1
        action = 0

        if self.actions_num > 24 and (self.actions_num % self.skip == 0):
            # robot count stores number of 55 pixels in the array
            previous_count = self.robot_count
            self.robot_count = 0
            self.transformEnvironment(observation)
            # If robot_count has increased then definitely new level
            if self.robot_count - previous_count >= ROBOT_PIXELS:
                self.level_count += 1
                print('Levels done : ' + str(self.level_count))
            action = 0

            player_x, player_y = self.getPlayerLocationInGrid()
            if player_x != 0 and player_y != 0:
                # Find a robot in line with bot.
                found, robot_x, robot_y = self.checkForRobot(player_x+6,
                                                             player_y+1)
                if found != 'not found':
                    self.skip = 8
                    action = self.fireAction(found, player_x,player_y,robot_x,robot_y)
                else:
                    self.skip = 2
                    action = self.determineMotion( player_x, player_y)
        return action


## YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
## ANOTHER MAIN PROGRAM
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--env_id', nargs='?', default='Berzerk-v0', help='Select the environment to run')
    args = parser.parse_args()

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = gym.make(args.env_id)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    outdir = 'random-agent-results'

    env.seed(0)
    agent = Agent(env.action_space)

    episode_count = 100
    reward = 0
    done = False
    score = 0
    special_data = {}
    special_data['ale.lives'] = 3
    ob = env.reset()
    while not done:
        action = agent.act(ob, reward, done)
        ob, reward, done, x = env.step(action)
        score += reward
        env.render()

    # Close the env and write monitor result info to disk
    print("Your score: %d" % score)
    env.close()