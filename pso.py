#!/usr/bin/python

__author__ = "Marcello Benedetti"

import numpy as np


class PSO(object):

    def __init__(self, n_parameters, n_particles, omega, phip, phig, type):
        
        assert(n_parameters > 0)
        assert(n_particles > 0)
        assert(omega >= 0)
        assert(phip >= 0)
        assert(phig >= 0)
        assert(type in ['standard', 'circular'])
        
        self.S = n_particles
        self.D = n_parameters
        self.phip = phip
        self.phig = phig
        self.omega = omega
        self.type = type
        self.iteration = 0
        self.history = [] 
    
        # Initialize positions and velocities
        self.v = np.random.uniform(-2, +2, size=(self.S, self.D))
        self.x = np.random.uniform(-1, +1, size=(self.S, self.D))
        
        # Initilize bests
        self.p = np.zeros_like(self.x)          # best particle positions
        self.fp = np.zeros(self.S)              # best particle function values
        self.g = []                             # best swarm position
        self.fg = 1e100                         # best swarm cost (artificial)
        self.idxg = 0                           # best swarm index (artificial)
        self.iterg = 0                          # best swarm iteration
        
        # Add position to history
        self.history.append(self.x.copy())
    
        # Initialize the particle's best known position 
        self.p = self.x.copy()
       
        # Initialize a temporary global best using index 0
        self.g = self.p[0, :].copy()
         
  
    def run(self, fxs):
        
        if self.iteration == 0:    
            
            self.fp = fxs
            for i in range(self.S):        

                # If the current particle's position is better than the swarm's,
                # update the best swarm position
                if self.fp[i]<self.fg:
                    self.fg = self.fp[i]
                    self.g = self.p[i, :].copy()
                    self.idxg = i
                    self.iterg = self.iteration
                
        else:
            for i in range(self.S):            
                
                fx = fxs[i]
                            
                # Compare particle's best position (if constraints are satisfied)
                if fx<self.fp[i]:
                    self.p[i, :] = self.x[i, :].copy()
                    self.fp[i] = fx.copy()

                    # Compare swarm's best position to current particle's position
                    if fx<self.fg:
                        self.fg = fx
                        self.g = self.x[i, :].copy()
                        self.idxg = i
                        self.iterg = self.iteration

        self.v = self.omega * self.v + \
                 self.phip * np.multiply( np.random.rand(self.S,self.D) , self.distance(self.p, self.x) ) + \
                 self.phig * np.multiply( np.random.rand(self.S,self.D) , self.distance(self.g, self.x) )
        
        ###
        #next_x = self.x + self.v
        #idx_small = np.where(np.abs(self.distance(self.x, next_x)).mean(1) < 0.025)[0]
        #idx_bad = np.where( self.fp > np.median(self.fp))[0]
        #idx = np.intersect1d(idx_small, idx_bad)
        
        #print(idx, self.fp[idx])
        
        #self.x = next_x
        #if idx.shape[0]>0:
        #    self.x[idx,:] = np.random.uniform(-1, +1, size=(idx.shape[0], self.D))
        #    self.v[idx,:] = np.random.uniform(-2, +2, size=(idx.shape[0], self.D)) 
        #    self.p[idx,:] = self.x[idx,:].copy()
        ###
        
        #GOOD 
        self.x = self.x + self.v 
        
        while np.sum(np.abs(self.x)>1)>0:
            self.x =  self.rescale(self.x)
        
        # Add position to history
        self.history.append(self.x.copy())
         
        # Increase iteration count
        self.iteration += 1
            
        return self.g, self.fg, self.idxg, self.iterg
            
            
    def distance(self, target, free_angle):
        
        if self.type == 'standard':
            return self.standard(target, free_angle)
        
        elif self.type == 'circular':
            return self.circular(target, free_angle)
        
    
    def standard(self, target, free_angle):
        
        res = target - free_angle
        return res
        
        
    def circular(self, target, free_angle):
    
        diff = target - free_angle
        abs_diff = np.abs(diff)
        cond = abs_diff <= 1.
        res = np.multiply( np.sign(diff), np.multiply(abs_diff, cond)) +\
              np.multiply( np.sign(free_angle), np.multiply(2.-abs_diff, 1.-cond) )
        return res
    
        
    def rescale(self, angles):
        
        new_angles = np.multiply((angles + 2), (angles < -1)) + \
             np.multiply((angles - 2), (angles > 1)) + \
             np.multiply(angles, (np.abs(angles)<=1))
        return new_angles
    
