# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 14:44:07 2023

@author: Nahom Mossazghi
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt 
from scipy import stats 
from itertools import combinations
import math
import csv



def weightedHeatmap(PairData, words, PlotHM):
    
    
    '''
    Restructure RT into matrix data structure
    
    '''
    
    Wmat = np.zeros((len(words),len(words))) 
    t = 0
    z = 0
    
    for i in range(len(words)):
        for j in range(len(words)):
            
            if i == j:
                Wmat[i,j] = np.NaN
            
            elif j > i:
                Wmat[i,j] = PairData[t]
                Wmat[j,i] = PairData[t]            
                t += 1  
                
                
    if PlotHM == 1:
        plt.imshow(Wmat, cmap='RdBu')
        plt.colorbar()
        plt.xticks(range(len(words)), words, rotation='vertical')
        plt.yticks(range(len(words)), words)
        plt.show()
        
    return Wmat
        
def ccbi_randperm(ntimes, nperm):
    
    '''
    #  p = ccbi_randperm(nitems,nperm)
    #  Parameters: number of items, number of random permutations
    #  Output: a matrix with nperm rows;
    #  Each row is an index of permuted item positions.
    
    #  returns a matrix (n,nitems)
    #  each row is a random permutation of nitems (labelled 1:nitems)
    #  produces n such permutations
    #  the random seed is changed at every call
    '''
    
    p = np.zeros((nperm, ntimes))        
    for i in range(nperm):
        p[i,:] = np.random.permutation(ntimes) + 1
        
    return p
                 

def splitHalf_Reliability(dat, perm):
    """
    Compute the reliability within a measure
    This analysis splits the data into 2 halfs and then averages the similarity structure
    This analysis is repeated
    """
    pSplit = ccbi_randperm(dat.shape[1], perm)

    rho = []
    for p in range(perm):
        # Split data
        if dat.shape[1] % 2 == 0:  # is even
            frstHalf = dat.iloc[:, pSplit[p, :(pSplit.shape[1]//2)]]
            scndHalf = dat.iloc[:, pSplit[p, (pSplit.shape[1]//2):]]

        elif dat.shape[1] % 2 == 1:  # is odd
            frstHalf = dat.iloc[:, pSplit[p, :int(np.floor(pSplit.shape[1]/2))]]
            scndHalf = dat.iloc[:, pSplit[p, int(np.ceil(pSplit.shape[1]/2)):]]
        # Avg dist of each half
        avgFrstHalf = frstHalf.mean(axis=1)
        avgScndHalf = scndHalf.mean(axis=1)

        # Correlate halves
        rhoI = np.corrcoef(avgFrstHalf, avgScndHalf)[0,1]

        rho.append(rhoI)
    
    rho = np.mean(rho)

    return rho
        























