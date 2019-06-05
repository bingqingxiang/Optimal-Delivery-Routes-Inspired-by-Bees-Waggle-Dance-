import random
import copy    # array-copying convenience
import sys     # max float
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import math
from  beesAlgorithm import * 

def TrailBeesAlgo(x,y,nc, ns, max_epochs):
  # n = ne· nre + (nb - ne)· nrb + ns (elite sites foragers + remaining best sites foragers + scouts)
  # Initialisation------------------------------------------------------
  # create ns random bees
  hive = [Bee(nc,x,y) for i in range(ns)] 
  best_length = sys.float_info.max 

  result_array=np.zeros(max_epochs)
    
  epoch = 0
  while epoch < max_epochs:  #Stopping Condition

    #Waggle dance-------------------------------------------------------
    hive = Waggle_dance(hive)
    if hive[0].pathLength<best_length:
      best_length = hive[0].pathLength
      best_path = copy.copy(hive[0].path)
    
    ne=int(ns * 0.2)# number of elite sites
    nre=2 # recruited bees for elite sites
    nb=int(ns * 0.5)# number of best sites
    nrb=1 # recruited bees for remaining best sites
    
    for i in range(ns):# assign bees
      if i < ne:#elite sites bees
        hive[i].status = 1
      elif i < nb:
        hive[i].status = 2
      elif i < nb + (nb-ne)*(nrb-1):
        hive[i].status = 2 
        for j in range(1,nrb):#group assign to best
          #i-((nb-ne)*j)
          hive[i].path=copy.copy(hive[i-((nb-ne)*j)].path)
          hive[i].pathLength=hive[i-((nb-ne)*j)].pathLength 
      elif i <  ne*nre + (nb-ne)*nrb:# assign to the elite sites
        hive[i].status = 1
        for j in range(1,nre):#rest group assign to elite
          #(i-(ne+(nb-ne)*nrb))%ne
          hive[i].path=copy.copy(hive[(i-(ne+(nb-ne)*nrb))%ne].path)
          hive[i].pathLength=hive[(i-(ne+(nb-ne)*nrb))%ne].pathLength
            
      else:
        hive[i].status = 0 
        
    for i in range(ns):  
      #Local search-------------------------------------------------------
      if (hive[i].status == 1) or (hive[i].status == 2):    # bees around elite sites or best sites bees
        neighbor_path = copy.copy(hive[i].path)
        random.seed(time())
        ri = random.randint(0, nc-1)  # random index
        ai = 0  # adjacent index. assume last->first
        if ri < nc-1: ai = ri + 1
        tmp = neighbor_path[ri]
        neighbor_path[ri] = neighbor_path[ai]
        neighbor_path[ai] = tmp
        neighbor_length = pathLength(x,y,neighbor_path)

        # check if neighbor path is better
        random.seed(time())
        p = random.random()  
        if (neighbor_length < hive[i].pathLength) or (neighbor_length >= hive[i].pathLength and p < 0.05):
          hive[i].path = copy.copy(neighbor_path)
          hive[i].pathLength = neighbor_length

          
          if neighbor_length < best_length:
            best_path = copy.copy(neighbor_path)
            best_length = neighbor_length
            
        

      elif hive[i].status == 0:  
        #Global search-------------------------------------------------------
        Global_path = [0 for j in range(nc)]
        for j in range(nc):
          Global_path[j] = j
        random.seed(time())
        random.shuffle(Global_path)
        Global_length = pathLength(x,y,Global_path)
        
        if Global_length < hive[i].pathLength:
          hive[i].path = copy.copy(Global_path)        
          hive[i].pathLength = Global_length
            
       
          if Global_length < best_length:
            best_path =copy.copy( Global_path)
            best_length = Global_length
           
          

      else:
        pass
        
    result_array[epoch]=best_length
    epoch += 1
   

  return result_array
 