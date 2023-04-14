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
import statsmodels.api as sm
rom sklearn.linear_model import LinearRegression
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
        p[i,:] = np.random.permutation(ntimes)
        
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


def regPairDiff(dumX, cov, Y, perm):
#     Predict pair differences among a binary category in Y
# 	  dumX is a dummy code variable being used to predict Y
# 	  cov is a matrix of covariates included in the model
# 	  Y is a continuous vector 
# 	  perm is the number of permutations used to compare against the observed beta
#     Dimensions of duX, cov, and Y should all align
        
#     Generate the permutations
    pComb = ccbi_randperm(len(dumX),perm)
    
#     Generate constant
    con = np.ones(len(dumX),1)
    
#     Estimate observed beta
    xModel = [con,dumX,cov]
    betaObs = LinearRegression().fit(Y, xModel)
    betaObs = betaObs.coef_[1]
    
    betaPerm = []
    for p in range(perm):
        xPermModel = [con, dumX(pComb(p,:)) ,cov]
        bPerm = LinearRegression().fit(Y,xPermModel)
        betaPerm.append(bPerm.coef_[1])
        
    
    if betaObs > 0:
        nBbeyond = len(np.where((betaPerm>betaObs)))
	    pval = nBbeyond/perm
        
    elif betaObs < 0:
	    nBbeyond = len(np.where(betaPerm<betaObs));
	    pval = nBbeyond/perm
        
    else:
        raise ValueError('observed beta is exactly equal to 0')
        
    return betaObs, pval



def FDR(p,q):
    # FORMAT [pID,pN] = FDR(p,q)
 
    # p   - vector of p-values
    # q   - False Discovery Rate level
    #
    # pID - p-value threshold based on independence or positive dependence
    # pN  - Nonparametric p-value threshold
    
    p = p[np.isfinite(p)]  # Toss NaN's
    p, origIndx = np.sort(p), np.argsort(p)
    _, origIndx = np.argsort(origIndx)
    
    V = len(p)
    I = np.transpose(range(0,V))
    
    cVID = 0
    cVN =  sum([1/(i+1) for i in range(V)])
    
    ID = p[np.max(np.where(p<=I/V*q/cVID))]
    pN = p[np.max(np.where(p<=I/V*q/cVN))]
    
    pthrID = pthrID[origIndx]
    pthrN = pthrN[origIndx]
    
    
    
   
    
    

    
    

    
 





















