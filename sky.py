from math import copysign
from random import uniform

class Ground:
    def __init__(self):
        pass

    def potential(self, x, y):
        '''
        Returning the potential (aka. the score)
        The higher the potential -> the closer the target
        '''
        return 700 - x

    def border(self):
        '''
        Returning the borders of the ground-plane
        Intersecting with these lead to done=True, and the task is failed
        '''
        border = [[(100, 400), (700, 300)],
                  [(700, 300), (650, 000)],
                  [(650, 000), (50, 100)],
        
                  [(300, 350), (310, 350)], #obstacles
                  [(300, 300), (310, 300)], 
                  [(300, 250), (310, 250)],
                  [(300, 200), (310, 200)],
                  [(300, 150), (310, 150)],
                  [(300, 100), (310, 100)]]

        return border

    def target(self):
        '''
        Returning the "target-area"
        Intersecting with these lines lead to done=True, and the task is accomplished
        '''
        target = [[(50, 100), (100, 400)],
                  [(45, 100), (95, 400)]]
        
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
        [3] Calculating reward (self.score)
        [4] Returning Intersections from [1], [2] & [3] with done-flag and coordinates of the dancer
        '''
        #Returning intersections of border, intersections of Sichtlinien, x/y-coordinates
        border_intersections = []
        view_intersections = []
        ground_border = self.ground.border()
        ground_target = self.ground.target()
        done = False

        #[1]
        for border in self.border():
            for g_line in ground_border:
                p, q = intersect(g_line, border)
                if (    (border[0][0] <= p <= border[1][0] or border[0][0] >= p >= border[1][0])
                    and (border[0][1] <= q <= border[1][1] or border[0][1] >= q >= border[1][1])
                    and (g_line[0][0] <= p <= g_line[1][0] or g_line[0][0] >= p >= g_line[1][0])
                    and (g_line[0][1] <= q <= g_line[1][1] or g_line[0][1] >= q >= g_line[1][1])
                ):
                    #print('line-intersection with border at:', p, q)
                    self.score -= 100 #ToDo: Make variable
                    done = True
                    border_intersections.append((p,q))
            for g_line in ground_target:
                p, q = intersect(g_line, border)
                if (    (border[0][0] <= p <= border[1][0] or border[0][0] >= p >= border[1][0])
                    and (border[0][1] <= q <= border[1][1] or border[0][1] >= q >= border[1][1])
                    and (g_line[0][0] <= p <= g_line[1][0] or g_line[0][0] >= p >= g_line[1][0])
                    and (g_line[0][1] <= q <= g_line[1][1] or g_line[0][1] >= q >= g_line[1][1])
                ):
                    #print('line-intersection with Target-area at:', p, q)
                    self.score += 100 #ToDo: Make variable
                    done = True

        #[2]
        for view in self.view():
            for g_line in ground_border:
                p, q = intersect(g_line, view)
                if (    (view[0][0] <= p <= view[1][0] or view[0][0] >= p >= view[1][0])
                    and (view[0][1] <= q <= view[1][1] or view[0][1] >= q >= view[1][1])
                    and (g_line[0][0] <= p <= g_line[1][0] or g_line[0][0] >= p >= g_line[1][0])
                    and (g_line[0][1] <= q <= g_line[1][1] or g_line[0][1] >= q >= g_line[1][1])
                ):
                    #print('view-intersection with border at:', p, q)
                    view_intersections.append((p,q))
            for g_line in ground_target:
                p, q = intersect(g_line, border)
                if (    (border[0][0] <= p <= border[1][0] or border[0][0] >= p >= border[1][0])
                    and (border[0][1] <= q <= border[1][1] or border[0][1] >= q >= border[1][1])
                    and (g_line[0][0] <= p <= g_line[1][0] or g_line[0][0] >= p >= g_line[1][0])
                    and (g_line[0][1] <= q <= g_line[1][1] or g_line[0][1] >= q >= g_line[1][1])
                ):
                    #print('view-intersection with Target-area at:', p, q)
                    view_intersections.append((p,q))

        #[3]
        self.score += self.potential - self.potential_

        #[?] ToDo: Maybe add coordinates of self.ground.target to return-statement?
        #[4]
        info = []
        return [view_intersections, border_intersections, self.border], self.score, done, info

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
            #DOWN
            self.y -= self.v
        elif (action == 2):
            #LEFT
            self.x -= self.v
        elif (action == 3):
            #RIGHT
            self.x += self.v
        else:
            pass

        self.potential = self.ground.potential(self.x, self.y)

        return self.update()

def intersect(line_a, line_b):
    '''
    Returns the intersection of two infinite lines,
    each difined by two points.
    
    line_a: static
    line_b: relative
    '''
    #Vertical flags
    v_f_a, v_f_b = False, False
    m_a, m_b = False, False
    
    dya = line_a[1][1]-line_a[0][1]    
    dxa = line_a[1][0]-line_a[0][0]
    if (dxa == 0):
        v_f_a = line_a[0][0]
    else:
        m_a = dya/dxa
    c_a = line_a[0][1]
    
    dyb = line_b[1][1]-line_b[0][1]
    dxb = line_b[1][0]-line_b[0][0]
    if (dxb == 0):
        v_f_b = line_b[0][0]
    else:
        m_b = dyb/dxb
    c_b = line_b[0][1]

    if (dxb == 0 or dyb == 0):
        '''
        Case distinction between m_b == 0 and m_b != 0
        Two different forms of calculation
        
        ToDo: below calculation can be moved inside this if-clause
        '''
        a = lambda x: m_a * x + c_a
        b = lambda x: m_b * x + c_b
    else:
        a = lambda x: m_a * (x - line_a[0][0]) + c_a
        b = lambda x: m_b * (x - line_b[0][0]) + c_b
        o = (-c_a + line_a[0][0] * m_a + c_b - line_b[0][0] * m_b)/(m_a - m_b)
        result = (o, b(o))
        return result
        
    if (v_f_b):
        result = (v_f_b, a(v_f_b - line_a[0][0]))
    elif (v_f_a):
        result = (v_f_a, b(v_f_a))
    elif (m_a != m_b):
        o = ((c_b - c_a)/(m_a - m_b))
        result = (o + line_a[0][0], b(o))
    else:
        result = (False, False)
    return result

class Environment:
    def __init__(self, xi, yi, a_initial=0, v_initial=10, n=1, width=25, height=25):
        self.xi = xi
        self.yi = yi
        self.a_initial = a_initial
        self.v_initial = v_initial
        self.n = n = 1
        self.width = width
        self.height = height
        
        self.dancers = []
        self.ground = Ground()

        self.reset()

    def reset(self):
        [self.dancers.append(Dancer(ground=self.ground, 
                                    x=uniform(self.xi[0], self.xi[1]), 
                                    y=uniform(self.yi[0], self.yi[1]), 
                                    width=self.width, 
                                    height=self.height, 
                                    v=self.v_initial))
        for _ in range(self.n)]

        #For the default early-alpha usage, only one dancer is necessary:
        self.dancer = self.dancers[0]

        observation, _, _, _ = self.dancer.update()
        return observation

    def step(self, action):
        observation, reward, done, info = self.dancer.event(action)
        return observation, reward, done, info

def make():
    env = Environment([600, 700], [100, 300])
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