from math import copysign
from random import uniform
from kostils import flatten, intersect
import numpy as np

class Ground:
    def __init__(self):
        pass

    def potential(self, x, y):
        '''
        Returning the potential (aka. the score)
        The higher the potential -> the closer the target
        '''
        return 7 - (x/100)

    def border(self):
        '''
        Returning the borders of the ground-plane
        Intersecting with these lead to done=True, and the task is failed
        '''
        border = [[(100, 400), (700, 300)],
                  [(700, 300), (650, 000)],
                  [(650, 000), (50, 100)],
                  
                  #[(300, 350), (310, 350)], #obstacles
                  #[(300, 300), (310, 300)], 
                  #[(300, 250), (310, 250)],
                  #[(300, 200), (310, 200)],
                  #[(300, 150), (310, 150)],
                  #[(300, 100), (310, 100)]
                  ]

        return border

    def target(self):
        '''
        Returning the "target-area"
        Intersecting with these lines lead to done=True, and the task is accomplished
        '''
        target = [[(50, 100), (100, 400)]]
        #          [(300, 100), (350, 400)]] #checkpoint
        
        return target


class Dancer:
    def __init__(self, ground, x, y, width, height, v):
        self.ground = ground
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.height = height
        self.v = int(v)
        self.score = 0
        self.reward = 0
        self.potential = 0
        self.potential_ = 0
        self.potential_history = []

    def border(self):
        #Grenzen des Dancers: Wenn intersection mit diesen: Game over
        border = [[(self.x, self.y), (self.x, self.y + self.height)],
                  [(self.x, self.y + self.height),(self.x + self.width, self.y + self.height)],
                  [(self.x + self.width, self.y), (self.x + self.width, self.y + self.height)],
                  [(self.x, self.y), (self.x + self.width, self.y)]]
        
        return border

    def view(self):
        #Sichtlinien: Dienen als input für deep learning
        view = [[(self.x-100, self.y-50), (self.x, self.y+self.height//2)],
                [(self.x-100, self.y-25), (self.x, self.y+self.height//2)],
                [(self.x-100, self.y+self.height//2), (self.x, self.y+self.height//2)],
                [(self.x-100, self.y+self.height+25), (self.x, self.y+self.height//2)],
                [(self.x-100, self.y+self.height+50), (self.x, self.y+self.height//2)]]

        return view   

    def update(self):
        '''
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
        #[?] ToDo: Maybe add coordinates of self.ground.target to observation-return-statement?

        # --------------------------------------
        # Configurations
        # Determine the output of this function.
        # --------------------------------------
        # append_point_none
        # Determines wheter point_none should be appended to output-array,
        # if there is no valid intersection, or not.
        append_point_none = True
        point_none = (False, False)
        # only_one_intersection:
        # Allows only one intersection per border. If there is no valid intersection,
        # point_none will be appended. Works only in combination with append_point_none = True
        only_one_intersection = True 

        # ------------------------
        # Pre-Declaring variables.
        # ------------------------
        if (only_one_intersection):
            border_intersections = [[], []] # *[0] means all (invalid ones too!) intresections
            view_intersections = [[], []]   # *[1] means only one intersection per dancer.border -> will be in observation
        else:
            border_intersections = []
            view_intersections = []
        info = ''
        ground_border = self.ground.border()
        ground_target = self.ground.target()
        done = False

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
                    #print('line-intersection with border at:', p, q)
                    #self.reward -= 10 #ToDo: Make variable
                    self.reward -= abs(self.reward)
                    done = True
                    info = 'crashed'
                    border_intersections[0].append((p,q)) if only_one_intersection else border_intersections.append((p,q))
                elif (append_point_none):
                    #print('none-line-intersection with border at:', point_none)
                    border_intersections[0].append(point_none) if only_one_intersection else border_intersections.append(point_none)
            for g_line in ground_target:
                p, q = intersect(g_line, border)
                if (    (border[0][0] <= p <= border[1][0] or border[0][0] >= p >= border[1][0])
                    and (border[0][1] <= q <= border[1][1] or border[0][1] >= q >= border[1][1])
                    and (g_line[0][0] <= p <= g_line[1][0] or g_line[0][0] >= p >= g_line[1][0])
                    and (g_line[0][1] <= q <= g_line[1][1] or g_line[0][1] >= q >= g_line[1][1])
                ):
                    #print('line-intersection with Target-area at:', p, q)
                    self.reward += 50 #ToDo: Make variable
                    #Due to checkpoint (second goal), the following line was changed from "done = True" to:
                    done = True if self.x < 100 else False
                    info = 'goal'
                    border_intersections[0].append((p,q)) if only_one_intersection else border_intersections.append((p,q))
                elif (append_point_none):
                    #print('none-line-intersection with Target-area at:', point_none)
                    border_intersections[0].append(point_none)

            if (only_one_intersection):
                border_intersections[1].append(
                    [next((item for item in border_intersections[0] if item is not point_none), point_none)])
                border_intersections[0] = []

            if (done):
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
                    #print('view-intersection with border at:', p, q)
                    view_intersections[0].append((p,q)) if only_one_intersection else view_intersections.append((p,q))
                elif (append_point_none):
                    #print('none-view-intersection with border at:', point_none)
                    view_intersections[0].append(point_none) if only_one_intersection else view_intersections.append(point_none)
            ''' [!] The observation shall not contain view-intersection with the target.
            for g_line in ground_target:
                p, q = intersect(g_line, border)
                if (    (border[0][0] <= p <= border[1][0] or border[0][0] >= p >= border[1][0])
                    and (border[0][1] <= q <= border[1][1] or border[0][1] >= q >= border[1][1])
                    and (g_line[0][0] <= p <= g_line[1][0] or g_line[0][0] >= p >= g_line[1][0])
                    and (g_line[0][1] <= q <= g_line[1][1] or g_line[0][1] >= q >= g_line[1][1])
                ):
                    #print('view-intersection with Target-area at:', p, q)
                    view_intersections[0].append((p,q)) if only_one_intersection else view_intersections.append((p,q))
                elif (append_point_none):
                    #print('none-view-intersection with Target-area at:', point_none)
                    view_intersections[0].append(point_none) if only_one_intersection else view_intersections.append(point_none)
            '''
            if (only_one_intersection):
                view_intersections[1].append(
                    [next((item for item in view_intersections[0] if item is not point_none), point_none)])
                view_intersections[0] = []

        # [3] ----------------------------------------------------
        # Calculating reward (self.reward) by multiple parameters.
        # --------------------------------------------------------
        
        # ---------------------------------
        # From potential calculated reward:
        #self.reward += self.potential - self.potential_
        
        # ----------------------------------
        # If the dancer didn't hit the goal,
        # the score will be reduced:
        #if (info != 'goal'):
        #    self.reward -= 1

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

        self.reward -= 1
        self.score += self.reward

        reward = self.reward
        self.reward = 0

        # [4] ------------------------------------------------------------------------------------
        # Returning Intersections from [1], [2] & [3] with done-flag and coordinates of the dancer
        # 1. Configuration for use with one-dimensional intersection arrays (only_one_intersection = False):
        #    observation = [view_intersections, border_intersections, self.border()]
        # 2. Configuration for use with only_one_intersection = True:
        #    observation = [view_intersections[1], border_intersections[1], self.border()]
        observation = [view_intersections[1], border_intersections[1], self.border()] if \
            only_one_intersection else [view_intersections, border_intersections, self.border()]
        observation = np.array(flatten(observation)).flatten()

        return observation, reward, done, info

    def event(self, action):
        '''
        Applying the action and updation the dancer
        '''
        self.potential_ = self.ground.potential(self.x, self.y)
        self.potential_history.append(self.potential_)

        if (action == 0):
            #UP
            self.y += self.v
        elif (action == 1):
            #RIGHT
            self.x += self.v
        elif (action == 2):
            #DOWN
            self.y -= self.v
        elif (action == 3):
            #LEFT
            self.x -= self.v
        elif (action == 4):
            #NOP
            # score will be reduced if agent does "nothing"
            self.score -= 1
            pass
        elif (action == 5):
            #TURN R
            pass
        elif (action == 6):
            #TURN L
            pass
        else:
            pass
            
        self.potential = self.ground.potential(self.x, self.y)

        return self.update()

class Environment:
    def __init__(self, xi, yi, a_initial=0, v_initial=10, n=1, width=25, height=25, random=True):
        #v_initial should be lower than the width and height
        self.xi = xi
        self.yi = yi
        self.a_initial = a_initial
        self.v_initial = v_initial
        self.width = width
        self.height = height
        self.n = n = 1
        self.random = random
        
        self.dancers = []
        self.ground = Ground()

        self.reset()

    def reset(self):
        [self.dancers.append(Dancer(ground=self.ground, 
                                    x=uniform(self.xi[0], self.xi[1]) if self.random else self.xi, 
                                    y=uniform(self.yi[0], self.yi[1]) if self.random else self.yi, 
                                    width=self.width, 
                                    height=self.height, 
                                    v=self.v_initial))
        for _ in range(self.n)]

        #For the default early-alpha usage, only one dancer is necessary:
        self.dancer = self.dancers[-1]

        observation, _, _, _ = self.dancer.update()
        return observation

    def step(self, action):
        observation, reward, done, info = self.dancer.event(action)
        return observation, reward, done, info

def make():
    # Random Configuration:
    # env = Environment([600, 700], [100, 300])
    # Fixed-Starting-Point Configuration:
    env = Environment(650, 188, random=False, v_initial=25)
    return env

''' 
Above configuration was tested under the following declarations
'''
'''
# ------------------------------------------------
# Declaring Variables:
# x/y - Interval for spawning n-Elements of Dancer 
# with initial velocity v_initial.
# ------------------------------------------------
xi = [600, 700] #max with current ground.border & ground.target: xi = [0, 700]
yi = [100, 300] #max with current ground.border & ground.target: yi = [0, 400]
v_initial = 10
n = 1
width = 25
height = 25

# ------------------------------------------------
# Creating n-dancers on different starting-points.
# ------------------------------------------------
dancers = []
ground = Ground()
for i in range(n):
    dancers.append(Dancer(ground=ground, 
                        x=uniform(xi[0], xi[1]), 
                        y=uniform(yi[0], yi[1]), 
                        width=width, 
                        height=height, 
                        v=v_initial))
'''