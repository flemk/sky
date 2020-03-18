Have a look at: blog.kostelezky.com

Software concept

1. Environment is classified in sky.py
2. Deep Q-Network is classified in dqn.py
3. lander.py is the executable. In it, the actual processing takes part
4. kostils.py is a custom utility-library

Introduction

As I had a coffee-break with a Friend of mine (cheers to Andi), we began to talk how it would be possible to simulate a human queue at ski-lifts. Those of you, who are familiar with skiing may know already what point I'm trying to make.
It may occur, when there is a lot of rush at a specific ski-lift, that there exit different strategies that may lead faster to reaching the lift: For example when the queue takes a curve, the advance inside the queue may be much more faster at the outside of the curve.
In this kind-of study I wanted to examine those different strategies with computational simulations.

First Concept

The first attempt of simulaiton, was to model the queue with a three-dimensional potential-field. The ground-potential at a specific point (x,y) must be some kind of ratio of distance (between the starting region and the target-area) and direction where to go. So I decided to take the following assumptions for the ground-potential:

1. The starting-point has the highest potential.
2. The target point must have a potential of zero.

With these points in mind, we can move on. We want to simulate the behaviour of human-beings, so we need to create elements, which represent them. These elements shall be created by a time-based function c(t) at points in the starting region. c(t) represents the rush of elements.
Note that we project a 2d field on our 3d potential-field. The negative gradient of the potential-field represents hereby the direction where one element should go next, to reach the target as fast as possible.
As soon as elements reach the target-area, they can be removed likewise with a time dependent function r(t), representing the capacity of transportation of the ski-lift.

But how to model those elements? And how to make sure they dont overlap? We decided to go on with a gaussian bell at the points (x,y) of one element. This bell will be added to the ground-potential, altering the gradient in the area of this specific point. So if not genereted at the same starting point, two or more elements may never overlap, due to their property to move only to the direction of the negative gradient.
With that being said, we recieve the following animation of descending gaussiang bells on the ground-potential:  Hereby the bottom left corner (deep blue) represents the target-area and the top right corner (red) is representing the starting region. The ground-potential was calculated using the function 0.05x**2+y.

The disadvantages of this attempt are obvious. The algorithm is already known and ist described by the "gradient descent method". This model allows only a view in the future based on the gradient at the current point. Modeled like this, it's only a one dimensional optimization problem. We could not apply deep learning on it (or at least it wouldn't make any sense).
But it gives us a better understanding of the problem.

Second Concept

The main goal of the second concept was to apply q-learning on the problem. Due to the needlessness of the potential-field, we can reduce the problem now on two dimensions. In the following, we consider the problem as seen from the top. Doing so, we choose the following method:

1. We create elements with defined properties: maximum speed, maximum acceleration, score.
2. Each timestep the score will be reduced, so that the model has the need "to do something", to not lose more points.
3. If the element is accelerating towards the target-area it will receive points.
4. If the element reaches the target-area, it will receive even more points. If the element is removed by r(t) the task counts as accomplished.
5. If the element hits a specified border, or another element, points will be removed and the task counts as failed.

As you probably already saw, it may makes sense to reconsider the usage of a potential field to calculate the received points in (3).
Using the pyglet library, the following model was created in python:


Here the left (double-lined) border represents the target-area and the right border is representing the starting region. The lines located in the middle of the plane could act as some kind of obstacle, for example a turnstile. Obviously the red dot represents an element.

Applying q-learning
In this first try of applying q-learning, the agent shall receive as inputs the current position of the element and multiple points intersections of lines going from the element in multiple directions (representing its view, as shown in the following figure). As output, the agent shall give coordinates, in which direction it wants to accelerate. Firstly we will neglect the impact of non-static acceleration.

be prepared for the results of applying q-learning
