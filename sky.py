import pyglet
from pyglet.window import key
from math import copysign
from random import uniform

window = pyglet.window.Window(width=800, height=400)
#pyglet.gl.glClearColor(255,255,255,1)

class Ground:
    def __init__(self):
        pass

    def potential(self):
        pass

class Dancer:
    '''
    '''
    def __init__(self, x, y, v):
        self.x = int(x)
        self.y = int(y)
        self.v = int(v)
        self.score = 0
        
        image = pyglet.image.load('C://Users/franz/Pictures/Saved Pictures/rdot.png')
        self.sprite = pyglet.sprite.Sprite(image, x, y)
        self.sprite.scale = 0.05

    def update(self):
        self.sprite.x = int(self.x)
        self.sprite.y = int(self.y)
        self.sprite.draw()

    def border(self):
        '''[(self.sprite.x, self.sprite.y), (self.sprite.x, self.sprite.y + self.sprite.height)],
            [(self.sprite.x, self.sprite.y + self.sprite.height),(self.sprite.x + self.sprite.width, self.sprite.y + self.sprite.height)],
            [(self.sprite.x + self.sprite.width, self.sprite.y), (self.sprite.x + self.sprite.width, self.sprite.y + self.sprite.height)],
            [(self.sprite.x, self.sprite.y), (self.sprite.x + self.sprite.width, self.sprite.y)],'''
        border = [
            
            [(self.sprite.x-100, self.sprite.y-50), (self.sprite.x, self.sprite.y+self.sprite.height//2)], #Sichtlinien
            ]
        '''[(self.sprite.x-100, self.sprite.y-25), (self.sprite.x, self.sprite.y+self.sprite.height//2)],
            [(self.sprite.x-100, self.sprite.y+self.sprite.height//2), (self.sprite.x, self.sprite.y+self.sprite.height//2)],
            [(self.sprite.x-100, self.sprite.y+self.sprite.height+25), (self.sprite.x, self.sprite.y+self.sprite.height//2)],
            [(self.sprite.x-100, self.sprite.y+self.sprite.height+50), (self.sprite.x, self.sprite.y+self.sprite.height//2)]]'''
        return border
        

@window.event
def on_draw():
    window.clear();
    [dancer.update() for dancer in dancers]
    
    # --------------------
    # Drawing a rectangle.
    # --------------------
    '''lines = [[(100, 100), (200, 100)],
             [(200, 100), (200, 200)],
             [(100, 200), (200, 200)],
             [(100, 100), (100, 200)],

             [(150, 100), (550, 800)],
             [(100, 400), (800, 200)]]'''
    lines = [[(100, 400), (700, 300)],
             [(50, 100), (100, 400)],
             [(700, 300), (650, 000)],
             [(650, 000), (50, 100)],

             [(45, 100), (95, 400)], #target-area
             [(300, 350), (310, 350)], #obstacles
             [(300, 300), (310, 300)], 
             [(300, 250), (310, 250)],
             [(300, 200), (310, 200)],
             [(300, 150), (310, 150)],
             [(300, 100), (310, 100)]
             ]
    # DEBUG --start
    lines = [[(50, 100), (100, 400)],
             [(45, 100), (95, 400)]]
    # DEBUG --end
    
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
    [check_intersections(dancer, lines) for dancer in dancers]

def check_intersections(dancer, lines):
    # -----------------------------
    # Helper-functions for clarity.
    # -----------------------------
    sign = lambda x: copysign(1, x)
    line = lambda x_0, y_0, x_1, y_1: ("v2i", (x_0, y_0, x_1, y_1))
    
    # -----------------------
    # Drawing Dancers border.
    # -----------------------
    rectl = dancer.border()
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
            if (rect[0][0] <= p <= rect[1][0]
                and rect[0][1] <= q <= rect[1][1]
                and (line[0][0] <= p <= line[1][0] or line[0][0] >= p >= line[1][0])
                and (line[0][1] <= q <= line[1][1] or line[0][1] >= q >= line[1][1])
                ):
                pass
            pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
                                     ('v2i', (int(p), int(q))),
                                     ('c3B', (255, 0, 0)))
            print(p,q)
            #    dancer.score -= 10 #ToDo: Make variable
            i += 1
        j += 1

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

    a = lambda x: m_a * (x - line_a[0][0]) + c_a
    b = lambda x: m_b * (x - line_b[0][0]) + c_b
    print('a(x) =', m_a, '* x +', c_a)
    print('b(x) =', m_b, '* x +', c_b) 
    if (v_f_b):
        result = (v_f_b, a(v_f_b - line_a[0][0]))
    elif (v_f_a):
        result = (v_f_a, b(v_f_a))
    elif (m_a != m_b):
        o = ((c_b - c_a)/(m_a - m_b))
        print('o: ', o)
        result = (o + line_a[0][0], b(o + line_a[0][0]))
    else:
        result = (False, False)
    return result

@window.event
def on_key_press(key, modifiers):
    '''
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

# ------------------------------------
# Declaring Variables (Interval, ...).
# ------------------------------------
xi = [0, 400]
yi = [0, 400]
v_initial = 10
n = 1

# -----------------------------------------------
# Creating n dancer on different starting-points.
# -----------------------------------------------
dancers = []
for i in range(n):
    dancers.append(Dancer(uniform(xi[0], xi[1]), uniform(yi[0], yi[1]), v_initial))

pyglet.app.run()

