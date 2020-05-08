# -*- coding: utf-8 -*-
"""
Created on Thu May  7 19:10:55 2020

@author: Rushad
"""

import pygame
import numpy as np
import matplotlib.pyplot as plt
'''
#initialize the gui
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()
'''
#define the constants
lh = 10
lb = 10
freq = 2.4e9 #in Hz
power_trans = 5e-9

c = 3e8      

dist_vector = np.zeros(shape=(lh, lb))
for h in range(1,lh+1):
    for l in range(1,lb+1):
        dist = float(np.sqrt(l**2 + h**2))
        dist_vector[h-1][l-1] = dist

lambd = c/freq
power_rec_w = ((lambd/(4*np.pi*dist_vector))**2)*power_trans
power_db = 10*np.log10(1000*power_rec_w) 
fspl = 20*np.log10(dist_vector) + 20*np.log10(freq/1e3) - 27.55

plt.imshow(dist_vector)
plt.show()
plt.imshow(power_db)
plt.show()
plt.imshow(fspl)
plt.show()