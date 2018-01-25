###########################
#Faisal Alnahhas          #
#Algorithms - Spring 2017 #
#Hendrix College          #
#HW5 - Percolation        #
###########################
#Note: I worked with Karthik, Jolli and Grace.
#this is the reference i used to make the the queue https://docs.python.org/3.5/library/heapq.html#module-heapq 

import numpy as np
from heapq import heappush, heappop
size = input("please type in an integer size of the grid to produce size x size grid: ")
size = int(size)

def make_grid():
    return np.zeros((size, size))
x = make_grid()

def find_neighbors(xc , yc , size):
    ns = []
    if xc > 0:
        ns.append(((xc-1), yc))
    if yc > 0:
        ns.append(((xc, (yc-1))))
    if yc < size - 1:
        ns.append(((xc + 1), yc))
    if xc < size - 1 :
        ns.append((xc, (yc + 1)))
    return ns
find_neighbors(5, 2, 10)


def is_neighbor(x1, y1, x2, y2):
    right_n = (x1+1, y1) == (x2, y2)
    left_n = (x1-1, y1) == (x2, y2)
    up_n = (x1, y1+1) == (x2, y2)
    down_n = (x1, y1-1) == (x2, y2)
    return right_n, left_n, up_n, down_n
    
    
final_path = {(x, y) : (x,y) for x in range(size) for y in range(size)}

class union_find:
    def __init__(self, size):
        self.sets = {(x, y) : (x,y) for x in range(size) for y in range(size)}
        self.sizes = {(x, y): 1 for x in range(size) for y in range(size)}
        
        #adding a point to the top of grid to check connectivity
        self.sets[(size-1, size)] = (size - 1, size)
        self.sizes[(size-1, size)] = 1
        
        #adding a poitn to the bottom of grid to check connectivity
        self.sets[(size-1, size + 1)] = (size - 1, size + 1)
        self.sizes[(size-1, size + 1)] = 1
        
        for i in range(size):
            self.sets[(i, 0)] = (size - 1, size)
            self.sizes[size-1, size] += 1
            
            self.sets[(i, size - 1)] = (size - 1, size+1)
            self.sizes[(size-1, size+1)] += 1
        
        
    def find(self, p):
        x = p
        if self.sets[x] == x:
            return p
        while self.sets[x] != x:
            x = self.sets[x]
        return x
    
    def union(self, p1, p2):
        r1 = self.find(p1)
        r2 = self.find(p2)
        
        if self.sizes[r1] > self.sizes[r2]:
            self.sets[r2] = self.sets[r1]
            self.sizes[r1] += self.sizes[r2]
            
        elif self.sizes[r2] > self.sizes[r1]:
            self.sets[r1] = self.sets[r2]
            self.sizes[r2] += self.sizes[r1]
        
        else:
            self.sets[r1] = self.sets[r2]
            self.sizes[r2] += self.sizes[r1]
            
open_set = set()
def percolate(x, size):
    data = union_find(size)
    while data.find((size-1, size)) != data.find((size-1,size+1)):
        xc = np.random.randint(0, size)
        yc = np.random.randint(0, size)
        if (xc, yc) not in open_set:
            open_set.add((xc, yc))
            x[xc][yc] = 1
            n = find_neighbors(xc,yc,size)
            for i in n:
                if i in open_set:
                    if data.find(i) != data.find((xc, yc)):
                        data.union(i, (xc, yc))
percolate(x, size)

def Dijkstras(x,open_set):
    visited_nodes = []
    tree = []
    p_heap = []
    path = False
    for i in range(len(x[0])):
        if x[0][i] == 1:
            visited_nodes.append((0,i))
        
    for n in visited_nodes:
        s = set()
        d = {(i,j) : (size*size) for i in range(size) for j in range(size)}
        d[n] = 0
        parents = {}
        parents[n] = n
        heappush(p_heap, (d[n], n))
        
    while not path and p_heap:
        (px,py) = heappop(p_heap)[1] #remove elements
        s.add((px,py)) #add removed elements to set

        neighbors = find_neighbors(px, py, size)
        for ns in neighbors:
            if ns in open_set:
                if ns not in s and (d[ns] > d[(px,py)] + 1):
                    if ns[1] == size - 1:
                        parents[ns] = (px,py)
                        d[ns] = d[(px,py)] + 1
                        path = True
                        break
                    parents[ns] = (px,py)
                    d[ns] = d[(px,py)] + 1
                    heappush(p_heap,(d[ns],ns))

    if path:
        tree.append((d[ns],ns, n, parents))

    
    return tree
trees = Dijkstras(x, open_set)
        
def write_file(size):
    fout = open("grid.txt", "w")
    for i in range(size):
        for j in range(size):
            #print(i,j)
            if x[i][j] == 1:
                fout.write("X ")
            elif x[i][j] == 2:
                fout.write("O")
            else:
                fout.write("? ")

        fout.write("\n")
    fout.close
write_file(size)