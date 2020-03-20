'''
custom utils library by Franz Ludwig Kostelezky
'''
import math

def flatten(ls: list) -> list:
    """This function returns a flattend list from an inputed nested list.

    Args:
        ls (list): The nested list, which should be converted to a flattend list.

    Returns:
        list

    """
    result = []
    if ls is not None:
        for element in ls:
            if type(element) is list:
                for subelement in flatten(element):
                    result.append(subelement)
            else:
                result.append(element)
    else:
        result = False
    return result

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

def sign(x: float) -> bool:
    '''
    Returns True if the sign of x is positive
    ans False if the sign of x is negative.
    '''
    return False if (x-abs(x) < 0) else True

def distance(p: tuple, q: tuple) -> float:
    '''
    Returns the distance between two n-multidimensional points.
    The parameters p and q need to be n-dimensional tuples.
    '''
    sum = 0
    if (len(p) == len(q)):
        for i in range(len(p)):
            sum += (p[i] - q[i]) ** 2
        return math.sqrt(sum)
    else:
        raise IndexError('p and q need to have identical dimensions')
    pass