#!/usr/bin/python

import itertools
import numpy as np

PRECISION = 8
CLIP = 1e-8   


# convert an integer into a vector of Ising variables +/-1    
def bitToInt(v):
    v = np.asarray(v)
    s = ''.join(str(int(e)) for e in v)
    s = s[::-1]
    num = int(s,2)
    return num
def intToIsing(num, n_spins):
    
    assert(num < 2**n_spins)
    
    s = format(num, '0'+str(n_spins)+'b')
    v = np.asarray([2.*int(c)-1. for c in s])
    
    return v


# convert a vector of ordered Ising variables +/-1 into an integer
def isingToInt(v):
    
    v = (np.asarray(v)+1.)/2.
    s = ''.join(str(int(e)) for e in v)
    num = int(s, 2)
    
    return num   


# generate BAS with specified rows and columns
def bars_and_stripes(rows, cols):
    
    data = [] 
    
    for h in itertools.product([0,1], repeat=cols):
        pic = np.repeat([h], rows, 0)
        data.append(pic.ravel().tolist())
          
    for h in itertools.product([0,1], repeat=rows):
        pic = np.repeat([h], cols, 1)
        data.append(pic.ravel().tolist())
    
    data = np.unique(np.asarray(data), axis=0)
    
    return data

# compute histogram from samples
def get_histogram(samples):
    samples = np.array(samples)
    n_samples, n_qubits = samples.shape

    histogram = [0 for _ in range(2**n_qubits)]
    for sample in samples:        
        idx = bitToInt(sample)
        histogram[idx] += 1./float(n_samples)
    
    assert(round(sum(histogram), PRECISION)==1.)
    return histogram


def distance(target, free_angle,type):
        
    if type == 'standard':
        return standard(target, free_angle)
        
    elif type == 'circular':
        return circular(target, free_angle)
        
    
def standard(target, free_angle):
        
    res = target - free_angle
    return res
        
        
def circular(target, free_angle):
    
    diff = target - free_angle
    abs_diff = np.abs(diff)
    cond = abs_diff <= 1.
    res = np.multiply( np.sign(diff), np.multiply(abs_diff, cond)) +\
          np.multiply( np.sign(free_angle), np.multiply(2.-abs_diff, 1.-cond) )
    return res
    
        
def rescale(angles):
        
    new_angles = np.multiply((angles + 2), (angles < -1)) + \
         np.multiply((angles - 2), (angles > 1)) + \
         np.multiply(angles, (np.abs(angles)<=1))
    return new_angles

def plots(ax1,ax2,ax_b,ax_c,fig,costs,bas,hist_sample,best_hist,n,m):
    index = np.arange(2**(n*m))
    bar_width = 0.3
    opacity = 0.5
    ax1.cla()
    ax1.plot(range(len(costs)), costs, color='#1f78b4')
    ax1.set_xlabel(r'Iteration')
    ax1.set_ylabel(r'KL')
    ax1.grid()
    #------------------------------------------
    '''ax_c = fig.add_axes([0.37,0.2,0.105,0.05])'''
    ax_c.cla()
    ax_c.set_xticks([])
    ax_c.set_yticks([])
    ax_c.text(0.1,0.1, '{:.2e}'.format(costs[-1]),fontsize=12)
    #-------------------------------------------
    y_position, width, height = 0.7, 0.05, 0.07
    '''ax_b = []
    ax_b.append(fig.add_axes([0.55,y_position,width,height]))
    ax_b.append(fig.add_axes([0.606,y_position,width,height]))
    ax_b.append(fig.add_axes([0.65,y_position,width,height]))
    ax_b.append(fig.add_axes([0.75,y_position,width,height]))
    ax_b.append(fig.add_axes([0.795,y_position,width,height]))
    ax_b.append(fig.add_axes([0.851,y_position,width,height])) '''  

    for i in range(bas.shape[0]):
        
        ax_b[i].cla()
        ax_b[i].matshow(bas[i].reshape(n, m), vmin=-1, vmax=1)
    
        ax_b[i].set_xticks([])
        ax_b[i].set_yticks([])
    
        ax_b[i].set_xticks([0.5], minor=True);
        ax_b[i].set_yticks([0.5], minor=True);
    
        ax_b[i].grid(which='minor', color='black', linestyle='-', linewidth=0.75)
    #-------------------------------------------    
    
    ax2.cla()
    
    
    rects1 = ax2.bar(index-bar_width/2., 
                 best_hist,
                 bar_width,
                 alpha=opacity,
                 color='b',
                 label='Guess')
    
    rects2 = ax2.bar(index+bar_width/2.,
                 hist_sample,
                 bar_width,
                 alpha=opacity,
                 color='r',
                 label='Truth')
    
    ax2.set_xlabel(r'Configuration')
    ax2.set_ylabel(r'Probability')
    ax2.set_ylim(top=0.25)
    
    
    #fig.tight_layout(pad=1, w_pad=1, h_pad=1)
    fig.canvas.draw()

