import pyglet
from pyglet.window import key
from math import copysign
from random import uniform

class Ground:
    def __init__(self):
        pass

    def potential(self):
        '''
        Returning the potential (aka. the score)
        The higher the potential -> the closer the target
        '''
        pass

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
        
        image = pyglet.image.load('C://Users/franz/Pictures/Saved Pictures/rdot.png')
        self.sprite = pyglet.sprite.Sprite(image, x, y)
        self.sprite.scale = 0.05

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
        [3] Returning Intersections from [1] & [2] with done-flag and coordinates of target-area
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
                    self.score -= 10 #ToDo: Make variable
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

        #[?] ToDo: Maybe add coordinates of self.ground.target to return-statement?
        #[3]
        return [view_intersections, border_intersections, self.border()]

    def gui_update(self):
        '''
        Function is deprecated and will be removed in future versions

        Update-function for use with pyglet GUI
        Updates sprite-coordinates and runs normal self.update
        '''
        self.sprite.x = int(self.x)
        self.sprite.y = int(self.y)
        self.sprite.draw()

        return self.update()

    def event(self, action):
        '''
        Applying the action and updation the dancer
        '''
        if (action == 0):
            pass
        elif (action == 1):
            pass
        elif (action == 2):
            pass
        elif (action == 3):
            pass
        else:
            pass

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

# ---------------
# Configurations.
# ---------------
pyglet_enable = True

# ------------------------------------------------
# Declaring Variables:
# x/y - Interval for spawning n-Elements of Dancer 
# with initial velocity v_initial.
# ------------------------------------------------
xi = [0, 400]
yi = [0, 400]
v_initial = 10
n = 1
width = 25  # only for dancer.sprite.scale = 0.05
height = 25 # only for dancer.sprite.scale = 0.05

# -----------------------------------------------
# Creating n dancer on different starting-points.
# -----------------------------------------------
dancers = []
ground = Ground()
for i in range(n):
    dancers.append(Dancer(ground=ground, 
                        x=uniform(xi[0], xi[1]), 
                        y=uniform(yi[0], yi[1]), 
                        width=width, 
                        height=height, 
                        v=v_initial))

# -------------------------------------------------------------
# Run pyglet graphical representation, if pyglet_enable is set.
# -------------------------------------------------------------
if (pyglet_enable):
    window = pyglet.window.Window(width=800, height=400)
    #pyglet.gl.glClearColor(255,255,255,1)

    @window.event
    def on_key_press(key, modifiers):
        '''
        Function is deprecated and will be removed in future versions.
        
        Keys represent joystick for dancers
        '''
        for dancer in dancers:
            if (key == pyglet.window.key.UP):
                dancer.y += dancer.v
            elif (key == pyglet.window.key.DOWN):
                dancer.y -= dancer.v
            elif (key == pyglet.window.key.LEFT):
                dancer.x -= dancer.v
            elif (key == pyglet.window.key.RIGHT):
                dancer.x += dancer.v
            else:
                pass
    
    @window.event
    def on_draw():
        '''
        Function is deprecated and will be removed in future versions.
        '''
        window.clear()

        # ---------------------------
        # Updating every dancer once.
        # ---------------------------
        [dancer.gui_update() for dancer in dancers]

        # ------------------------------------------
        # Receiving the border-lines from the ground
        # and draw them on pyglet canvas (optional).
        # ------------------------------------------
        lines = ground.border()
        [lines.append(el) for el in ground.target()]
    
        line = lambda x_0, y_0, x_1, y_1: ("v2i", (x_0, y_0, x_1, y_1))
        [pyglet.graphics.draw(2,pyglet.gl.GL_LINES,
                              line(lines[0][0],
                                   lines[0][1],
                                   lines[1][0],
                                   lines[1][1]),
                              ('c4B', (0, 0, 255, 255, 0, 0, 255, 255)) )
        for lines in lines]

        # ----------------------------------
        # Checking intersection with dancer.
        # ----------------------------------
        #[check_intersections(dancer, lines) for dancer in dancers]

    def check_intersections(dancer, lines):  
        '''
        Function is deprecated and will be removed in future versions.
        '''
        # -----------------------
        # Drawing Dancers border.
        # -----------------------
        rectl = dancer.border()
        line = lambda x_0, y_0, x_1, y_1: ("v2i", (x_0, y_0, x_1, y_1))
        [pyglet.graphics.draw(2,pyglet.gl.GL_LINES,
                              line(lines[0][0],
                                   lines[0][1],
                                   lines[1][0],
                                   lines[1][1]),
                               ('c4B', (0, 255, 0, 255, 0, 255, 0, 255)) )
        for lines in rectl]

        # -------------------------------------
        # Check, if there are any intersections
        # betwen the outlines of the dancer and
        # the border.
        # -------------------------------------
        j = 0
        for line in lines:
            i = 0
            for rect in rectl:
                p, q = intersect(line, rect)
                if ((rect[0][0] <= p <= rect[1][0] or rect[0][0] >= p >= rect[1][0])
                    and (rect[0][1] <= q <= rect[1][1] or rect[0][1] >= q >= rect[1][1])
                    and (line[0][0] <= p <= line[1][0] or line[0][0] >= p >= line[1][0])
                    and (line[0][1] <= q <= line[1][1] or line[0][1] >= q >= line[1][1])
                    ):
                    pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
                                         ('v2i', (int(p), int(q))),
                                         ('c3B', (255, 0, 0)))
                    #print('Intersection at', p, q)
                    dancer.score -= 10 #ToDo: Make variable
                i += 1
            j += 1

    pyglet.app.run()
else:
    pass

