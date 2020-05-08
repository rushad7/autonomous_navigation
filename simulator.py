# -*- coding: utf-8 -*-
"""
Created on Thu May  7 19:10:55 2020

@author: Rushad
"""

import turtle as t
import numpy as np
#import matplotlib.pyplot as plt

#define the constants
freq = 2.4e9 #in Hz
power_trans = 5e-9
c = 3e8      
lambd = c/freq

def static_ap(lh, lb):
    '''
    Initializes the fixed AP at (0,0 )and it's power feild 
    distribution, which is used to calculate the distances
    '''
    global dist_vector_s
    dist_vector_s = np.zeros(shape=(lh, lb))
    for h in range(1,lh+1):
        for l in range(1,lb+1):
            dist = float(np.sqrt(l**2 + h**2))
            dist_vector_s[h-1][l-1] = dist
            
    power_rec_w = ((lambd/(4*np.pi*dist_vector_s))**2)*power_trans
    power_db = 10*np.log10(1000*power_rec_w)
    
    return power_db


def set_new_ap(lh, lb, internode_dist):
    '''
    Initializes a new AP at point (internode_dist,0),
    assuming that static_ap(lb,lh) is initialized at (0,0)
    '''
    dist_vector = np.zeros(shape=(lh, lb))
    for h in range(1,lh+1):
        for l in range(1,lb+1):
            dist = float(np.sqrt(internode_dist**2 + h**2))
            internode_dist = internode_dist-1
            dist_vector[h-1][l-1] = dist
            
    power_rec_w = ((lambd/(4*np.pi*dist_vector))**2)*power_trans
    power_db = 10*np.log10(1000*power_rec_w)
    
    return power_db

#fspl = 20*np.log10(dist_vector_ap1) + 20*np.log10(freq/1e3) - 27.55

'''
plt.imshow(power_static_db)
plt.show()
plt.imshow(power_ap1_db)
plt.show()
plt.imshow(p_norm)
plt.show()
'''

def boundry_init(lb, lh):
    '''
    Define the boundry of your simulations
    lb --> breadth (lenght along  X axis)
    lh --> breadth (lenght along  Y axis)
    '''
    t.forward(int(lb))
    t.left(90)
    t.forward(int(lh)) 
    t.left(90)
    t.forward(int(lb)) 
    t.left(90)
    t.forward(int(lh))
    t.left(90)

def node_init(lb, lh, internode_dist):
    '''
    Setup locations of nodes and power fields
    '''
    t.penup()
    t.goto(0,lh)
    t.pendown()
    t.circle(7)
    t.write("Node 1")
    power_static = static_ap(lb, lh)
    t.penup()
    t.goto(internode_dist,lh)
    t.pendown()
    t.circle(7)
    t.write("Node 2")
    power_ap = set_new_ap(lb, lh, internode_dist)
    global power_total
    power_total = (power_static + power_ap)/2
    
    return power_total, 

def nav(source, goal, lb, lh, dist):
    if (source[0] < lb and source[1] < lh) and (goal[0] < lb and goal[1] < lh):
        t.penup()
        t.goto(source)
        t.write("SOURCE")
        try:
            for h in range(1, lh+1):
                for l in range(1, lb+1):
                    neighbours = { (l-1, h):dist[l-1][h], (l+1, h):dist[l+1][h], (l, h):dist[l][h+1], (l, h+1):dist[l][h+1], (l+1, h-1):dist[l+1][h-1], (l+1, h+1):dist[l+1][h+1], (l-1, h-1):dist[l-1][h-1], (l-1, h+1):dist[l-1][h+1] }
                    print(neighbours)
                    '''have to decompose into key and value --> find max --> compute cost --> then move
                    '''
        except IndexError:
            pass
        

def run_sim(lb, lh, internode_dist):
    boundry_init(int(lb),int(lh))
    power_field = node_init(lb, lh, internode_dist)
    print(power_field)
    t.mainloop()
    
run_sim(lb=100, lh=100, internode_dist=100)
