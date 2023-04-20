# -*- coding: utf-8 -*-
"""

Created on Tue Apr  4 15:30:29 2023

@author: Nahom Mossazghi


"""


# load packages 

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt 
from scipy import stats 
from itertools import combinations
from util import *
import csv
import re


# load data 
path = r'C:/Users/nmoss/Desktop/grad_stuff/phd/research/projects/b2/'

# Load PRaM data

datPRaM = pd.read_csv (path + 'data/PRaM_num.csv', header=None)
datAge = pd.read_csv (path + 'data/demo_age.csv', header=None)
raceLab = pd.read_csv (path + 'data/demo_race.csv', header=None)
pairLab = pd.read_csv (path + 'data/PRaM_pairLabels.csv', header=None)
pID = pd.read_csv (path + 'data/PRaM_pID.csv', header=None)



#Sort pairs accoring to prefered combination

words = ['police', 'firefighter', 'neighbors(yours)', 'conservatives(political)', 'liberals(political)', 'healthcare', 'voting', 'immigration', 'religion', 'science', 'anger', 'fear', 'joy', 'love', 'sadness', 'trust']
combinations_list = [list(c) for c in combinations(words, 2)]

# re-organize the dataframe according to the word combination

wPairLabel = []
x = []                  #index orders are saved as list

for i in range(len(combinations_list)):
    
    # Extract pair rating
    idx0 = pairLab[pairLab.iloc[:,1].str.contains(re.escape(combinations_list[i][0]))].index
    idx1 = pairLab[pairLab.iloc[:,2].str.contains(re.escape(combinations_list[i][1]))].index
    pIndx = idx0.intersection(idx1)
    
    # Extract pair label
    wPairLabeli = combinations_list[i][0] + '-' + combinations_list[i][1]
    wPairLabel.append(wPairLabeli)
    x.append(pIndx[0])
    
# Pair label rating    
datPRaM_conSort = datPRaM.iloc[:,x]   
datPRaM_conSort = datPRaM_conSort.rename(columns=dict(zip(datPRaM_conSort.columns, wPairLabel)))    
wPairLabel = pd.DataFrame(wPairLabel)    
# Convert to distance matrix
# Restructure RT into matrix data structure
    
Wmat = np.zeros((len(words), len(words)))    

t = 0
z = 0

for i in range(len(words)):
    for j in range(len(words)):
        
        if i == j:
            Wmat[i,j] = np.NaN
        
        elif j > i:
            Wmat[i,j] = datPRaM_conSort.iloc[t,0]
            Wmat[j,i] = datPRaM_conSort.iloc[t,0]
            
            t += 1

# Save variables as csv 
datPRaM_conSort.to_csv(path + '/data/pairdistances.csv', index=True)
wPairLabel.to_csv(path + '/data/PairLabels.csv', index=True)
pd.DataFrame(Wmat).to_csv(path + '/data/distMatrix.csv', index=True) 
    

#Indx racial groups 

bIndx =  raceLab[raceLab.iloc[:,0].str.contains('Black or African American')].index
wIndx =  raceLab[raceLab.iloc[:,0].str.contains('White')].index 
    
bPRaM = datPRaM_conSort.iloc[bIndx,:]
wPRaM = datPRaM_conSort.iloc[wIndx,:]


# Average pair distance
avgBSim = np.mean(bPRaM, axis=0)
avgWSim = np.mean(wPRaM, axis=0)

# maintain polarity
bPRaMz = stats.zscore(bPRaM, axis=0)  
wPRaMz = stats.zscore(wPRaM, axis=0)   
    
# Compute mean normalized association
bPRaMz_avg = np.mean(bPRaMz, axis=0);
wPRaMz_avg = np.mean(wPRaMz, axis=0);
    
# Generate distance matricies
bPRaM_Weights = weightedHeatmap(avgBSim, words,1); # Compute association matrix for Black participants
wPRaM_Weights = weightedHeatmap(avgWSim, words,1); # Compute association matrix for White participants   
    
# Splithalf Reliability
perm = 10000
# [rhobSpAM] = splitHalf_Reliability(bSpAMz, perm)
rhobPRaM = splitHalf_Reliability(bPRaMz, perm)

# [rhowSpAM] = splitHalf_Reliability(wSpAMz, perm)
rhowPRaM = splitHalf_Reliability(wPRaMz, perm)


# bSpAM_k = (rhobPRaM*(1-rhobSpAM))/(rhobSpAM*(1-rhobPRaM));
# wSpAM_k = (rhowPRaM*(1-rhowSpAM))/(rhowSpAM*(1-rhowPRaM));    
    

# Age
bAge = datAge.iloc[bIndx,:]
wAge = datAge.iloc[wIndx,:]
Age = np.vstack([bAge, wAge])


pairLabel = wPairLabel

blackCode = np.concatenate([np.ones(len(bIndx)), np.zeros(len(wIndx))])
perm = 1000   
    
# Concatonate data Needs to be structured as Pair-by-participants
# Original
# SpAM_cat = [bSpAM; wSpAM];
PRaM_cat = np.vstack([bPRaM, wPRaM])


# Normalized
# SpAMz_cat = [bSpAMz, wSpAMz]
# PRaMz_cat = [bPRaMz, wPRaMz]


# bObsPairsSpAM = [] 
# pPairsSpAM = []
bObsPairsPRaM = []
pPairsPRaM = []
z = 0

for i in range(len(pairLabel)):
    z += 1
    print(z)
    
    # Isolate pair data 
    # ySpAM = SpAM_cat[:,i]
    yPRaM = PRaM_cat[:,i]
    
    # betaObs_SpAM, pval_SpAM = regPairDiff(blackCode, Age, ySpAM, perm)
    betaObs_PRaM, pval_PRaM = regPairDiff(blackCode, Age, yPRaM, perm)
    
    # bObsPairsSpAM = [bObsPairsSpAM; betaObs_SpAM];
    # PairsSpAM = [pPairsSpAM; pval_SpAM];
    bObsPairsPRaM.append(betaObs_PRaM)
    pPairsPRaM.append(pval_PRaM)
    
