# -*- coding: utf-8 -*-
"""
Created on Thu May  7 19:10:55 2020

@author: Rushad
"""

import pygame
import numpy as np
import matplotlib.pyplot as plt

#define the constants
lh = 10
lb = 10
freq = 2.4e9 #in Hz
power_trans = 5e-9
c = 3e8      
lambd = c/freq

def static_ap(lh, lb):
    '''
    Initializes the fixed AP at (0,0 )and it's power feild 
    distribution, which is used to calculate the distances
    '''
    dist_vector = np.zeros(shape=(lh, lb))
    for h in range(1,lh+1):
        for l in range(1,lb+1):
            dist = float(np.sqrt(l**2 + h**2))
            dist_vector[h-1][l-1] = dist
            
    power_rec_w = ((lambd/(4*np.pi*dist_vector))**2)*power_trans
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

#initialize the gui
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('2D Navigation Simulator')
clock = pygame.time.Clock()

set_points = 0
mouse_cache = []
while set_points<=2:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                set_points = set_points+1
                x, y = pygame.mouse.get_pos()
                pygame.draw.circle(gameDisplay, (0,0,255), (x,y), 20)
                mouse_cache.append([x,y])
                print("STATIC POINT INITIALIZED")

        pygame.display.update()
        clock.tick(60)

if set_points > 2:
    lb = np.sqrt((mouse_cache[0][1] - mouse_cache[1][1])**2 + (mouse_cache[0][0] - mouse_cache[1][0])**2)
    lh = np.sqrt((mouse_cache[1][1] - mouse_cache[2][1])**2 + (mouse_cache[1][0] - mouse_cache[2][0])**2)
    print(lb,lh)
                    
                    
pygame.quit()