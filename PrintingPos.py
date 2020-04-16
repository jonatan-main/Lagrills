# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 09:59:43 2020

@author: Mitzie
"""


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure

from mpl_toolkits.mplot3d import Axes3D

from mpl_toolkits import mplot3d

fig = plt.figure()
ax = plt.axes(projection='3d')


earth = open("nEarth.txt","r")
sun   = open("nSun.txt","r")
jup   = open("nJup.txt","r")
ven   = open("nVen.txt","r")
sat1  = open("nSat1.txt","r")

f = [earth,sun,jup,ven,sat1]
size = [2,100,10,0.5,0.01]
colors = ["#3D9839","#F6FF05","#C18B00","#F0C577","#080303"]


class body(object):
    def __init__(self, pos, size, color):
        self.pos = pos
        self.size = size
        self.color = color
        
E = body(f[0],size[0],colors[0])
S = body(f[1],size[1],colors[1])
J = body(f[2],size[2],colors[2])
V = body(f[3],size[3],colors[3])
S1 = body(f[4],size[4],colors[4])

def drawPlanets(fs, size, color):
    fss = fs
    ss = size
    cc = color
    f1 = fss.read()
    f1 = f1.replace("[", "")
    f1 = f1.replace("]", "")
    xyz = f1.split(",")
    num = []
    
    for x in range(len(xyz)-1): 
        curnum = float(xyz[x])
        num.insert(x,curnum)
    
    xpos = num[0::3]
    ypos = num[1::3]
    zpos = num[2::3]
    
    ax.scatter3D(xpos,ypos,zpos,s=ss,c=cc)
        
        
drawPlanets(E.pos,E.size,E.color)
drawPlanets(S.pos,S.size,S.color)
drawPlanets(J.pos,J.size,J.color)
drawPlanets(V.pos,V.size,V.color)    
#drawPlanets(S1.pos,S1.size,S1.color)

#for i in f:
    #drawPlanets(i,size[i],colors[i])
    

plt.xlabel("Distance x (AU)")
plt.ylabel("Distance y (AU)")
plt.ylabel("Distance z (AU)")
plt.title("The system")
# Hide grid lines
ax.grid(False)

# Hide axes ticks
ax.set_xticks([])
ax.set_yticks([])
#ax.set_zticks([])





