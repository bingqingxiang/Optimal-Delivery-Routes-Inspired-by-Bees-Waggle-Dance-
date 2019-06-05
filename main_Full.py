
# coding: utf-8

# In[1]:


import random
import copy    # array-copying convenience
import sys     # max float
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import math
from  beesAlgorithm import * 
from  Trail import * 


# In[2]:


#input 
#number of nodes = number of cities       nc = 20
#number of scout bees                     ns = 100
#number of elite sites                    ne = int(ns * 0.1)
#recruited bees for elite sites          nre = 2
#number of best sites                     nb = int(ns * 0.15)
#recruited bees for remaining best sites nrb = 1
#The total artificial bee n = ne· nre + (nb - ne)· nrb + ns
#max_epochs =1000


# In[3]:


# Create Map
numberOfNode=20
random.seed(1)
xPosition=random.sample(range(0, 100),numberOfNode)
random.seed(2)
yPosition=random.sample(range(0, 100),numberOfNode)
CityMap=createMap(xPosition,yPosition,numberOfNode);


# In[4]:


#get distance of node i and j
#=distance2Node(0,1,xPosition,yPosition)
#print(d)

#test draw graph
#path=[j for j in range(20)]
#print(path)
#pathLength(xPosition,yPosition,path)
#createGraph(xPosition,yPosition,numberOfNode,path);
#plt.show()


# In[5]:


#one time 
num_cities = numberOfNode
ns = 40 #number of scout bees
max_epochs =100
print("num_cities : " , num_cities)
print("number of scout bees: " , ns)
print("max_epochs : " , max_epochs)
result=BeesAlgo(xPosition,yPosition,num_cities,ns, max_epochs)# save plot
#print(result.shape)
np.save("result.npy",result)


# print(result[0:30])
# plt.plot(range(0,max_epochs),result[0:max_epochs])
# plt.show()

# #Thousands time
# num_cities = numberOfNode
# ns = 100 #number of scout bees 20
# max_epochs =1000
# n_trail=1000
# l=np.zeros(max_epochs)
# for trail in range(n_trail):
#     l=l+TrailBeesAlgo(xPosition,yPosition,num_cities,ns, max_epochs)
#     #print(l.shape)
#     print(trail)
# trail_result=l/n_trail
# np.save("trail1000.npy",trail_result)

# In[6]:


plt.plot(result)
plt.show()


# ns=100
# ne=int(ns * 0.1)
# nre=3
# nb=int(ns * 0.2)
# nrb=2
# print(nb) 
# print(nb + (nb-ne)*(nrb-1))
# print(ne*nre + (nb-ne)*nrb)
# print("start")
# for i in range(ns):# assign bees
#   if i < nb:#elite sites bees
#     print("i",i)
# 
#   elif i < nb + (nb-ne)*(nrb-1):
#     print("second")
#     for j in range(1,nrb):
#       print(i,i-((nb-ne)*j))
# 
#   elif i < ne*nre + (nb-ne)*nrb:
#     print("third")
#     print(i,(i-(ne+(nb-ne)*nrb))%ne)
#     
#     
#   else:
#     print(i)
