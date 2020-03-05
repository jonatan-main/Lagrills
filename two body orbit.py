# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 08:21:47 2020

@author: The LaGrills
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode
from mpl_toolkits.mplot3d import Axes3D

earth_radius = 6738.00 #Km
earth_mu = 398600.00 #Km^3/s^2

def diff_q(t, y, mu):
    rx, ry, rz, vx, vy, vz = y
    r = np.array([rx,ry,rz])
    
    #norm of radius vector
    norm_r = np.linalg.norm(r)
    
    #two body acceleration
    ax,ay,az = -r*mu/norm_r**3
    
    return [vx,vy,vz, ax,ay,az]

def plot(rs):
    fig = plt.figure(figsize=(18,6)) #set up figure
    ax = fig.add_subplot(111, projection='3d') #create the subplot
    
    #plot trajectory
    ax.plot(rs[:,0], rs[:,1], rs[:,2],'w--', label= 'trajectory')
    ax.plot([rs[0,0]],[rs[0,1]],[rs[0,2]],'wo', label = 'initial position')
    
    #plot central bodie
    u_,v_ = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    _x = earth_radius*np.cos(u_)*np.sin(v_)
    _y = earth_radius*np.sin(u_)*np.cos(v_)
    _z = earth_radius*np.cos(v_)
    ax.plot_surface(_x,_y,_z, cmap='Blues')
    
    #plot axes
    #l = earth_radius*2
    #x,y,z = [[0,0,0],[0,0,0],[0,0,0]]
    #u,v,w = [[l,0,0],[0,l,0],0,0,l]
    #ax.quiver(x,y,z,u,v,w, color = 'k')   
    #max_val = np.max(np.abs(rs))
    
    #ax.set_xlim(-max_val, max_val)
    #ax.set_ylim(-max_val, max_val)
    #ax.set_zlim(-max_val, max_val)
    
    #ax.set_xlim('X (Km)')
    #ax.set_ylim('Y (Km)')
    #ax.set_zlim('Z (Km)')
    
    #ax.set_aspect('equal')
    
    plt.legend()
    
    plt.show()
    
    
    
    
if __name__ == '__main__':
    #initial orbit parameters
    r_mag = earth_radius + 500 #km above surface
    v_mag = np.sqrt(earth_mu/r_mag) #km / s... how to calculate orbital velocity for a circular orbit
    
    #initial position and velocity vectors
    r0 = [r_mag, 0, 0]
    v0 = [0,v_mag,0]
    
    #time stuff
    t_span = 100*60.0
    dt= 100.00 #timestep
    steps = int(np.ceil(t_span/dt)) #number of steps
    
    #initialize lists
    ys = np.zeros((steps,6))
    ts = np.zeros((steps,1))
    
    #initial conditions
    y0 = r0+v0
    ys[0] = np.array(y0)
    step = 1
    
    #initialize solver
    solver= ode(diff_q)
    solver.set_integrator('lsoda')
    solver.set_initial_value(y0,0)
    solver.set_f_params(earth_mu)
    
    #fill orbit
    while solver.successful() and step<steps:
        solver.integrate(solver.t+dt)
        ts[step] = solver.t
        ys[step] = solver.y
        step+=1
    rs = ys[:,:3]
    
    plot(rs)
    
    
    
    
    
    