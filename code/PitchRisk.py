import numpy as np
import math
import Metrica_Viz as mviz

w=68
h=106

#Convert from coordinates to distance
def DISTANCE(x,y):
    return np.sqrt(x**2+abs(y)**2)

#Convert from coordinates to angle
def ANGLE(x,y):
    angle=np.arctan(7.32*x / (x**2 + abs(y)**2 - (7.32/2)**2))
    if angle<0:
        angle+=np.pi
    return angle

#calculate xG
#input:coordinates
def xG(x,y):
    distance=DISTANCE(x,y)
    angle=ANGLE(x,y)
    if (distance<7.32/2) & (angle==0):
        angle+=np.pi
    z=4.03-2.53*angle-0.12*distance-0.11*distance*angle+0.0069*distance**2
    #x=3.9-3.54*angle #角度のみ反映
    return 1/(1+np.exp(z))

#Creating an xG array
def make_xG():
    xG_array=np.zeros((w,h))

    for i in range(w):
        for j in range(h):
            k=abs(i-w/2)
            xG_array[i,j]=xG(j,k)
            
    return xG_array

#calculate SxA
#input:coordinates
def SxA(x,y):
    G=xG(x,y)
    x=x/106*100
    y=y/68*100
    
    x=(x-51.7902432)/math.sqrt(560.359953)
    y=(y-25.2317529)/math.sqrt(194.295050)
    G=(G-0.00675608983)/math.sqrt(0.0014388397)
    
    z=-8.67108158-1.85487057*x-0.43115795*y-0.25692468*G+0.19006112*x*y+0.25620965*x**2-0.1446175*y**2
    return 1/(1+np.exp(-z))

#Creating an SxA array
def make_SxA():
    SxA_array=np.zeros((w,h))

    for i in range(w):
        for j in range(h):
            k=abs(i-w/2)
            SxA_array[i,j]=SxA(j,k)
            
    return SxA_array


#Pitch Risk
def Pitch_Risk(at,PPCF):
    xG_array=make_xG()
    SxA_array=make_SxA()
    
    if at=='Away':
        #右側のゴールに向かうとき
        xG_array=np.rot90(xG_array,2)
        SxA_array=np.rot90(SxA_array,2)
        
    PR=PPCF*xG_array+PPCF*SxA_array*10
    
    return PR
