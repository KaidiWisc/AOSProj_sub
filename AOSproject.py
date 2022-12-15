# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 23:57:27 2022

# three functions to support the calculation in Main file

@author: Kaidi Peng
"""

import numpy as np
from scipy.stats import pearsonr


def Motion_Vector_Cal(field1,field2,w):
# This function will calculate the motion vector between field1 and field2 based  on morph technique
# field1: precip. or TQV field at the first time
# fields: precip. or TQV field at the second time
# w: the actual window size is 2*w+1. It defines the size of neighborhood to calculate correlation

    xsize=np.shape(field1)[1]
    ysize=np.shape(field1)[0]
       
   # T1: V southward motion vector
   # T2: U eastward motion vectot
    
    T1=np.zeros((ysize,xsize))
    T2=np.zeros((ysize,xsize))
    
    for j in range(0,ysize):
        for i in range(0,xsize):
            
            x1=max(i-w,0)
            x2=min(i+w,xsize)
            y1=max(j-w,0)
            y2=min(j+w,ysize)
            
            win=field1[y1:y2,x1:x2]
            # if the sub-field1 is not rainy, I do not care its movement
            if np.sum(np.sum(win))==0:
                
                T1[j,i]=0  
                T2[j,i]=0 
                
            else:
                winR=np.zeros((ysize,xsize))

                for jj in range(0,ysize):
                    for ii in range(0,xsize):

                        xx1=max(ii-w,0)
                        xx2=min(ii+w,xsize)
                        yy1=max(jj-w,0)
                        yy2=min(jj+w,ysize)

                        win2=field2[yy1:yy2,xx1:xx2]
                        
                        if np.sum(np.sum(win2))==0:
                            
                            # if sub-field1 is rainy but sub-field2 is not rainy, this pair will not be selected
                            winR[jj,ii]=0   
                        else:
                            newwin1=win.flatten()
                            newwin2=win2.flatten()
                            len1=len(newwin1)
                            len2=len(newwin2)
                            comlen=min(len1,len2)
                            newwin1=newwin1[0:comlen]
                            newwin2=newwin2[0:comlen]
                            
                            # calculate R for sub-field1 and sub-field2
                            winR[jj,ii]= pearsonr(newwin1, newwin2)[0]
                            
                            
                # find the best R, use it to calculate motion vector
                winR[np.isfinite(winR)==False]=0
                
                index=np.argmax(winR)
                row, col = divmod(index, winR.shape[1])

                T1[j,i]=(row-(j))  #  y southward movement is positive
                T2[j,i]=col-(i)  # x  eastward movement is positive
                    
                # avoid low corelation
                if winR[row,col]<=0:
                    T1[j,i]=0
                    T2[j,i]=0
            
    return T1,T2


def Heidke_Skill(realP,estiP):
    
    a=np.sum((realP>0) & (estiP>0))
    c=np.sum((realP>0) & (estiP==0))
    b=np.sum((realP==0) & (estiP>0))
    d=np.sum((realP==0) & (estiP==0))
    HS= 2*(a*d-b*c)/[(a+c)*(c+d)+(a+b)*(b+d)]
    
    return HS

def NRMSE(realP,estiP):
    # I ignore correct non-detect here
    realP1=realP[(realP>0) | (estiP>0)]
    estiP1=estiP[(realP>0) | (estiP>0)]
    NRMSEP=np.sqrt(np.nanmean((realP1-estiP1)**2))/np.nanmean(realP1)
    return NRMSEP