from math import copysign
from random import uniform
from kostils import flatten, intersect, distance
import numpy as np

class Ground:
    def __init__(self):
        '''
        The initialization does not take yet any arguments.

        Future plans for arguments:
        - border
          - reward for hit with border: self.border_reward
        - target
          - reward for hit with target: self.target_reward
        - checkpoints
          - reward for hit with checkpoint: self.checkpoint_reward
        - potential-function
        '''
        
        self.border_see_reward = 0
        self.border_hit_reward = -10
        self.target_see_reward = 1
        self.target_hit_reward = 100
        self.checkpoint_see_reward = 0
        self.checkpoint_hit_reward = 0
        self.cycle_reward = -1
        self.action_reward = [('up', 0),
                              ('right', 0), 
                              ('down', 0), 
                              ('left', 0), 
                              ('nop', -1), 
                              ('t-right', 0), 
                              ('t-left', 0), 
                              ('else', 0)]

    def potential(self, x: int, y: int) -> float:
        '''
        Returning the potential at point (x,y)
        '''
        return -7*((x+200)**2 + 8*(y-200)**2)/10000/113 +1

    def border(self):
        '''
        Returning the borders of the ground-plane as array of array, where the first tuple represents the (x,y)
        starting-point of a line, and the second the end-point.
        Intersecting with these lines should lead to done=True, and the task is failed.
        '''
        border = [[(100, 400), (700, 300)],
                  [(700, 300), (650, 000)],
                  [(650, 000), (50, 100)],
                  
                  [(300, 350), (300, 360)], #obstacles
                  [(300, 250), (300, 260)],
                  [(300, 150), (300, 160)]
                  ]

        return border

    def obstacles(self):
        '''
        Returning the obstacles of the ground-plane as array of array, where the first tuple represents the (x,y)
        starting-point of a line, and the second the end-point.
        Intersecting with these lines should lead to done=True, and the task is failed.
        '''
        pass

    def checkpoints(self):
        '''
        Returning the checkpoints of the ground-plane as array of array, where the first tuple represents the (x,y)
        starting-point of a line, and the second the end-point.
        '''
        checkpoint = [[(300, 100), (350, 400)]]
        
        return checkpoint

    def target(self):
        '''
        Returning the target-area (as line) of the ground-plane as array of array, where the first tuple represents the (x,y)
        starting-point of a line, and the second the end-point.
        Intersecting with these lines should lead to done=True, and the task is accomplished.
        '''
        target = [[(50, 100), (100, 400)]]
        
        return target


class Dancer:
    def __init__(self, ground: Ground, x: int, y: int, width: int, height: int, v_initial: int, a_initial: float):
        '''
        Initializes a Dancer with the following properties:
        - ground: The ground on which the dancer is acting (important for borders and potential)
        - x, y: coordinates where the dancer is located
        - width, height: measures of the Dancer
        - v_initial: initial velocity. Determines the maximum speed of the dancer (pixel per cycle)
          v_initial should be lower than the width and height: v_initial <= width, height
        - a_initial: acceleration. Determines how fast the dancer can accelerate
          [!] Not yet implemented

        Also the following properties are initialized:
        - score: defines the sum of the rewards the dancer got
        - reward: will be set 0 after every update(). Defines the reward the Agent will receive
        - potential, potential_: potential before coordinates were updated in event() and after
        - potential_history: each cycle the potential will be added to the potential_history array
        '''
        self.ground = ground
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.v = int(v_initial)
        self.a = a_initial

        self.score = 0
        self.reward = 0
        self.potential = 0
        self.potential_ = 0
        self.potential_history = []
        self.xy_history = []
        self.reward_history = []
        self.action_history = []

    def border(self):
        '''
        Returns the border as array of array, of the Dancer, where the first tuple represents the (x,y)
        starting-point of a line, and the second the end-point.

        These lines are to determine, wether the Dancer is hitting something or not.
        '''
        border = [[(self.x, self.y), (self.x, self.y + self.height)],
                  [(self.x, self.y + self.height),(self.x + self.width, self.y + self.height)],
                  [(self.x + self.width, self.y), (self.x + self.width, self.y + self.height)],
                  [(self.x, self.y), (self.x + self.width, self.y)]]
        
        return border

    def view(self):
        '''
        Returns the view-lines as array of array, of the Dancer, where the first tuple represents the (x,y)
        starting-point of a line, and the second the end-point.

        These lines act as "what the dancer sees".
        '''
        view = [[(self.x-100, self.y-100), (self.x, self.y)],#left side
                [(self.x-100, self.y+self.height//2), (self.x, self.y+self.height//2)],
                [(self.x-100, self.y+self.height+100), (self.x, self.y+self.height)],

                [(self.x+self.width//2, self.y-100), (self.x+self.width//2, self.y)],#mid part
                [(self.x+self.width//2, self.y+self.height+100), (self.x+self.width//2, self.y+self.height)],
                
                [(self.x+self.width+100, self.y-100), (self.x+self.width, self.y)],#right side
                [(self.x+self.width+100, self.y+self.height//2), (self.x+self.width, self.y+self.height//2)],
                [(self.x+self.width+100, self.y+self.height+100), (self.x+self.width, self.y+self.height)],
                ]

        return view   

    def update(self):
        '''
        This function is used in Environment.step() and equals it.
        It returns primarily the observation and the result of the action that was taken by the agent.
        
        It basically breaks down to four steps:
        [1] Calculating intersections of dancer.border with ground.border and ground.target
            [1.a] Determinig wether Dancer is in target-area or not (done-flag)
        [2] Calculating intersections of dancer.view with ground.border and ground.target
        [3] Calculating reward (self.reward)
        [4] Returning Intersections from [1], [2] & [3] with done-flag and coordinates of the dancer

        Additional to [1] & [2]: 
        1.  If there is no valid intersection a none_point will be added to the return statement, if 
            append_point_none is set True:
                append_point_none = True
        2.  If only_one_intersection is set True, only one intersection per line will be allowed.
            if:
                only_one_intersection = True
        '''

        # ------------------------
        # Pre-Declaring variables.
        # ------------------------
        border_intersections = [[], []]         # *[0] means all (invalid ones too!) intresections
        view_intersections = [[], []]           # *[1] means only one intersection per dancer.border -> will be in observation output
        info = ''
        done = False
        point_none = (False, False)             # Will be appended, if there is no vail intersection
        ground_border = self.ground.border()
        ground_target = self.ground.target()

        # [1] -----------------------------------------------
        # Calculating intersections of dancer.border with 
        # ground.border and ground.target and determinig 
        # wether Dancer is in target-area or not (done-flag).
        # ---------------------------------------------------
        for border in self.border():
            for g_line in ground_border:
                p, q = intersect(g_line, border)
                if (    (border[0][0] <= p <= border[1][0] or border[0][0] >= p >= border[1][0])
                    and (border[0][1] <= q <= border[1][1] or border[0][1] >= q >= border[1][1])
                    and (g_line[0][0] <= p <= g_line[1][0] or g_line[0][0] >= p >= g_line[1][0])
                    and (g_line[0][1] <= q <= g_line[1][1] or g_line[0][1] >= q >= g_line[1][1])
                ):
                    info = 'crashed'
                    done = True
                    self.reward += self.ground.border_hit_reward                    
                    border_intersections[0].append((p,q))
                    #print('line-intersection with border at:', p, q)
                else:
                    border_intersections[0].append(point_none)
                    #print('none-line-intersection with border at:', point_none)
            for g_line in ground_target:
                p, q = intersect(g_line, border)
                if (    (border[0][0] <= p <= border[1][0] or border[0][0] >= p >= border[1][0])
                    and (border[0][1] <= q <= border[1][1] or border[0][1] >= q >= border[1][1])
                    and (g_line[0][0] <= p <= g_line[1][0] or g_line[0][0] >= p >= g_line[1][0])
                    and (g_line[0][1] <= q <= g_line[1][1] or g_line[0][1] >= q >= g_line[1][1])
                ):
                    info = 'goal'
                    done = True
                    self.reward += self.ground.target_hit_reward
                    border_intersections[0].append((p,q))
                    #print('line-intersection with Target-area at:', p, q)
                else:
                    border_intersections[0].append(point_none)
                    #print('none-line-intersection with Target-area at:', point_none)

            # Only one (if available valid, else point_none) intersection will be appended to output array:
            border_intersections[1].append(
                [next((item for item in border_intersections[0] if item is not point_none), point_none[0])])
            border_intersections[0] = []

            if (done):
                # If a border was hit: game over
                break

        # [2] ------------------------------------
        # Calculating intersections of dancer.view 
        # with ground.border and ground.target.
        # ----------------------------------------
        for view in self.view():
            for g_line in ground_border:
                p, q = intersect(g_line, view)
                if (    (view[0][0] <= p <= view[1][0] or view[0][0] >= p >= view[1][0])
                    and (view[0][1] <= q <= view[1][1] or view[0][1] >= q >= view[1][1])
                    and (g_line[0][0] <= p <= g_line[1][0] or g_line[0][0] >= p >= g_line[1][0])
                    and (g_line[0][1] <= q <= g_line[1][1] or g_line[0][1] >= q >= g_line[1][1])
                ):
                    self.reward += self.ground.border_see_reward
                    #view_intersections[0].append((p,q))
                    view_intersections[0].append(distance((p,q), view[1])) #passing distance instead of coordinates
                    #print('view-intersection with border at:', p, q)
                else:
                    view_intersections[0].append(point_none)
                    #print('none-view-intersection with border at:', point_none)

            # Only one (if available valid, else point_none) intersection will be appended to output array:
            view_intersections[1].append(
                [next((item for item in view_intersections[0] if item is not point_none), point_none[0])])
            view_intersections[0] = []

        ''' In this version, view-intersections will be passed seperatly'''
        for view in self.view():
            for g_line in ground_target:
                p, q = intersect(g_line, border)
                if (    (border[0][0] <= p <= border[1][0] or border[0][0] >= p >= border[1][0])
                    and (border[0][1] <= q <= border[1][1] or border[0][1] >= q >= border[1][1])
                    and (g_line[0][0] <= p <= g_line[1][0] or g_line[0][0] >= p >= g_line[1][0])
                    and (g_line[0][1] <= q <= g_line[1][1] or g_line[0][1] >= q >= g_line[1][1])
                ):
                    self.reward += self.ground.target_see_reward
                    #view_intersections[0].append((p,q))
                    view_intersections[0].append(distance((p,q), view[1])) #passing distance instead of coordinates
                    #print('view-intersection with Target-area at:', p, q)
                else:
                    view_intersections[0].append(point_none)
                    #print('none-view-intersection with Target-area at:', point_none)

            # Only one (if available valid, else point_none) intersection will be appended to output array:
            view_intersections[1].append(
                [next((item for item in view_intersections[0] if item is not point_none), point_none[0])])
            view_intersections[0] = []

        # [3] ----------------------------------------------------
        # Calculating reward (self.reward) by multiple parameters.
        # --------------------------------------------------------
        
        # -------------------------------------
        # From potential calculated reward:
        self.reward += self.potential - self.potential_

        # ------------------------------------
        # Aborting, when score gets below -50:
        #if (self.score <= -50):
        #    self.reward -= 5
        #    done = True
        #    info = 'score_negative_aborted'
        # -------------------------------------
        # Aborting, when reward gets below -50:
        #if (self.reward <= -50):
        #    self.reward -= 5
        #    done = True
        #    info = 'reward_negative_aborted'
        # -------------------------------------
        # Each cycle reward get reduced by 1:
        self.reward += self.ground.cycle_reward

        # Adding reward to score
        self.score += self.reward

        # Passing reward and resetting it
        reward = self.reward
        self.reward = 0
        self.reward_history.append(reward)

        # [4] ---------------------------------
        # Return the observation with done flag
        # and additional parameters:
        observation = [view_intersections[1], self.x, self.y, self.x + self.width, self.y + self.height]
        observation = np.array(flatten(observation)).flatten()

        return observation, reward, done, info

    def event(self, action: int) -> tuple:
        '''
        Applying the action choosen by the dqn and updation the dancer.

        Turning (action == (5||6)) is not yet implemented.
        '''
        self.potential_ = self.ground.potential(self.x, self.y)
        self.potential_history.append(self.potential_)
        self.xy_history.append((self.x, self.y))
        self.action_history.append(action)

        if (action == 0):
            #Moving up
            self.y += self.v
            self.reward += self.ground.action_reward[action][1]
        elif (action == 1):
            #Moving right
            self.x += self.v
            self.reward += self.ground.action_reward[action][1]
        elif (action == 2):
            #Moving down
            self.y -= self.v
            self.reward += self.ground.action_reward[action][1]
        elif (action == 3):
            #Moving left
            self.x -= self.v
            self.reward += self.ground.action_reward[action][1]
        elif (action == 4):
            #No operation
            self.reward += self.ground.action_reward[action][1]
            pass
        elif (action == 5):
            #Turning right
            self.reward += self.ground.action_reward[action][1]
            pass
        elif (action == 6):
            #Turning left
            self.reward += self.ground.action_reward[action][1]
            pass
        else:
            self.reward += self.ground.action_reward[action][1]
            pass
            
        self.potential = self.ground.potential(self.x, self.y)

        return self.update()

class Environment:
    '''
    This class "Environment" acts as interface between training-programm and Agent-Acting-definition.
    Aka: This class returns returns the observation.

    It is: Agent (in the dqn) equals to the class Dancer (sky).
    '''
    def __init__(self, xi, yi, a_initial=0, v_initial=10, n=1, width=25, height=25, random=True):
        '''
        Creating an Environment:
        - if random is set True: xi and yi must be a two dimensional touple, representing the starting-area, where the Agent will start.
          Else if random is set False: xi and yi need to be integers, representing a fixed starting point.
        - n-Elements will be spawned, but only the last one is used for acting. (early alpha)
        - a_initial, v_initial, width, height will be passed as they are to the Agent.
        '''
        self.xi = xi
        self.yi = yi
        self.a_initial = a_initial
        self.v_initial = v_initial
        self.width = width
        self.height = height
        self.n = n
        self.random = random
        
        self.dancers = []
        self.ground = Ground()

        self.reset()

    def reset(self) -> tuple:
        '''
        This function resets the Dancer:
        Creates a new one, defines it as active Agent, and passes its observation as result.
        '''
        [self.dancers.append(Dancer(ground=self.ground, 
                                    x=uniform(self.xi[0], self.xi[1]) if self.random else self.xi, 
                                    y=uniform(self.yi[0], self.yi[1]) if self.random else self.yi, 
                                    width=self.width, 
                                    height=self.height, 
                                    v_initial=self.v_initial,
                                    a_initial=self.a_initial))
        for _ in range(self.n)]

        #For the default early-alpha usage, only one dancer is necessary:
        self.dancer = self.dancers[-1]

        observation, _, _, _ = self.dancer.update()
        return observation

    def step(self, action: int) -> tuple:
        '''
        The next action choosen will be evaluated by the Dancer and its outputs will be passes as result.
        action needs to be an integer.
        '''
        observation, reward, done, info = self.dancer.event(action)
        return observation, reward, done, info

def make(xi=650, yi=188, random=False, v_initial=25, a_initial=0, width=25, height=25):
    '''
    This function passes by the parameters created environment.
    xi, yi, a_initial=0, v_initial=10, n=1, width=25, height=25, random=True
    
    [Ex.1] Example for a random configuration:
    xi = [600, 700], yi = [100, 300]

    [Ex.2] Example for a fixed starting-point configuration:
    xi = 650, yi = 188, random = False
    '''
    env = Environment(xi=xi, yi=yi, random=random, v_initial=v_initial, width=width, height=height)
    return env