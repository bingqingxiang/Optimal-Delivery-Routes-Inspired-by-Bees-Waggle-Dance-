import numpy as np
import matplotlib.pyplot as plt
result=np.load("result.npy")
plt.plot(result)
plt.title("Bees Algorithm")
plt.xlabel("n Iterations")
plt.ylabel("Distance")
plt.savefig("full.png", format="PNG", dpi=400)
plt.close()

plt.plot(result[0:50])
#plt.title("Bees Algorithm")
#plt.xlabel("n Iterations")
#plt.ylabel("Distance")
plt.savefig("part.png", format="PNG", dpi=400)
plt.close()

print(result[0])
print(result[20])
print(result[5000-1])
'''
Length of best path = 572.9015456641082
number of local update 25
number of global update 1
'''