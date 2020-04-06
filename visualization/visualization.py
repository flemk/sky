'''
Library to visualize the output of lander.py
'''
import matplotlib.pyplot as plt
import numpy as np

def xy_plot(c_list, xi=(0,700), yi=(0,400), plot=plt):
    '''
    Shows the movement of a dancer on the xy-plane.
    Example:

    import visualization.visualization as vi
    plt.clf()
    plt = vi.xy_plot(output.dancers[0].xy_history)
    for el in output.dancers:
        plt = vi.xy_plot(el.xy_history, plot=plt)
    plt.savefig('./visualization/xy_vi.png')
    '''
    plot.plot([el[0] for el in c_list], [el[1] for el in c_list])
    plot.xlim(xi[0], xi[1])
    plot.ylim(yi[0], yi[1])
    
    return plt

def contour(i_c, plot=plt):
    '''
    parameters:
    - i_c: input class, where the potential-function is inherted by i_c.potentiyl(x,y)
    '''
    delta = 25
    x = np.arange(0,700,delta)
    y = np.arange(0,400,delta)
    X,Y=np.meshgrid(x,y)
    Z = i_c.potential(X,Y)
    _, ax = plot.subplots()
    CS = ax.contour(X, Y, Z)
    ax.clabel(CS, inline=1, fontsize=10)
    plt.savefig('./visualization/contour_test.png')
    
    return plt

def add_border(lines, plot):
    '''
    The following is to implement:

    import kostils
    l = kostils.flatten(output.ground.border())
    plt = vi.xy_plot(l, plot=plt)
    plt.savefig('./visualization/xy_vi.png')
    '''
    pass

def add_target(lines, plot):
    '''
    The following is to implement:

    l = kostils.flatten(output.ground.target())
    plt = vi.xy_plot(l, plot=plt)
    plt.savefig('./visualization/xy_vi.png')
    '''
    pass