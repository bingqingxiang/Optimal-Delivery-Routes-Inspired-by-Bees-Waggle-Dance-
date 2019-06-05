import random
from time import time
import copy    # array-copying convenience
import sys     # max float
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import math

# In[ ]:
#-----------------------------------------------------------------------
class Bee:
  def __init__(self, nc,x,y):
    self.status = 0  # 0 = inactive, 1 = ne number of elite sites, 2 = nb number of best sites
    self.path = np.zeros(nc)#[0 for i in range(nc)]  # potential solution
    for i in range(nc):
      self.path[i] = i  # [0,1,2, ...]
    random.seed(time())
    random.shuffle(self.path)
    self.pathLength = pathLength(x,y,self.path) # bee's current error
    
# In[ ]:
#-----------------------------------------------------------------------
def result_path(path):
  for i in range(len(path)-1):
    print(str(path[i]) + " -> ", end="")
  print(path[len(path)-1])
# In[ ]:
#-----------------------------------------------------------------------
def createMap(x,y,numberOfNode):
    G=nx.Graph()
    for i in range (numberOfNode):
        G.add_node(i,pos=(x[i],y[i]))
    pos=nx.get_node_attributes(G,'pos')
    nx.draw(G,pos, with_labels=True,node_color='r')
    plt.savefig("map.png", format="PNG", dpi=400)
    #plt.show()
    return G
    
def createGraph(x,y,numberOfNode,path):
    G=nx.DiGraph()
    for i in range (numberOfNode):
        G.add_node(i,pos=(x[i],y[i]))
        
    for i in range (numberOfNode-1):
        G.add_edge(path[i],path[i+1])
        
    G.add_edge(path[-1],path[0])
    pos=nx.get_node_attributes(G,'pos')
    nx.draw(G,pos, with_labels=True,node_color='r',arrowsize=10,arrowstyle='fancy')
    #plt.show()

# In[ ]:
#-----------------------------------------------------------------------
def distance2Node(i,j,x,y):
    d=math.sqrt(pow(x[i]-x[j],2)+pow(y[i]-y[j],2))
    return d

def pathLength(x,y,path):#total distance of a path(fo back to original)
    l=0
    for i in range(len(path)-1):
        l+=distance2Node(int(path[i]),int(path[i+1]),x,y)
    l+=distance2Node(0,len(path)-1,x,y)

    return l

# In[ ]:
#-----------------------------------------------------------------------
def Waggle_dance(hive):# rank scouts in decreasing order of visited site fitness
    #len(hive)=number of bees in the hive
    pl=[0 for i in range(len(hive))]# path length array before sort
    pl_copy=[0 for i in range(len(hive))]
    hiveSort=[0 for i in range(len(hive))]
    
    for i in range (len(hive)):
        pl[i] = copy.copy(hive[i].pathLength)
        pl_copy[i]=copy.copy(hive[i].pathLength)
        
    pl.sort()
    #print(pl)
    #print(pl_copy)
    # pl_copy.index(pl[i]) find the index in the non sort version
    for i in range (len(hive)):
        #print(pl[i])
        #print(pl_copy.index(pl[i]))
        hiveSort[i]=copy.copy(hive[pl_copy.index(pl[i])])
        #print(hiveSort[i].pathLength)
    return hiveSort
# In[ ]:
#-----------------------------------------------------------------------
def BeesAlgo(x,y,nc, ns, max_epochs):
  # n = ne· nre + (nb - ne)· nrb + ns (elite sites foragers + remaining best sites foragers + scouts)
  # Initialisation------------------------------------------------------
  # create ns random bees
  hive = [Bee(nc,x,y) for i in range(ns)] 
  best_length = sys.float_info.max 

  result_array=np.zeros(max_epochs)
  localcounter=0
  globalcounter=0
  epoch = 0
  while epoch < max_epochs:  #Stopping Condition
    #Waggle dance-------------------------------------------------------
    hive = Waggle_dance(hive)
    if hive[0].pathLength<best_length:
      best_length = hive[0].pathLength
      best_path = copy.copy(hive[0].path)
    
    ne=int(ns * 0.25)# number of elite sites
    nre=3 # recruited bees for elite sites
    nb=int(ns * 0.3)# number of best sites
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
            #print("local",best_length)
            localcounter=localcounter+1
        

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
            best_path = copy.copy(Global_path)
            best_length = Global_length
            #print("global",best_length)
            globalcounter=globalcounter+1
        
      else:
        pass
    if (epoch% 20)==0 and epoch<100:
        createGraph(x,y,len(best_path),best_path)
        plt.savefig("plot\Epoch{}.png".format(epoch), format="PNG", dpi=400)
        plt.close()
        
    if (epoch% (max_epochs/10))==0:
        createGraph(x,y,len(best_path),best_path)
        plt.savefig("plot\Epoch{}.png".format(epoch), format="PNG", dpi=400)
        plt.close()
        
    result_array[epoch]=best_length
    epoch += 1
   

 
  createGraph(x,y,len(best_path),best_path)
  plt.savefig("plot\Epoch{}.png".format(epoch), format="PNG", dpi=400)
  plt.close()

  print("\nBest path found:")
  result_path(best_path)
  print("\nLength of best path = " + str(best_length))
  print("number of local update",localcounter)
  print("number of global update",globalcounter)
  return result_array
 