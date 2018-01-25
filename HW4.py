#Faisal Alnahhas
#Algorithms HW4
#Hendrix College - Spring 2017

import sys
import numpy as np

#name = sys.argv[1]  #input("Type the full path for the file without the .in extension: ")
#out_name = sys.argv[2]
name = input("Make sure the files is saved in the same directory as the file\
you wish to parse. Type in the full name of the desired file: ")

f = open(name , "r")
fin = f.readlines()
n = int(fin[0])
m = int(fin[1])
DAG = False

edges=[]
num_incoming_edges = {i:0 for i in range(n)}
num_outgoing_edges = {i:0 for i in range(n)}
#print(num_incoming_edges)
incoming_edges = {i:[] for i in range(n)}
outgoing_edges = {i:[] for i in range(n)}
top_order = []
no_incoming = set()
zero_degrees = set()
non_zero_degrees = set()
cycle = []
flag = False
cycle_flag = False

def stripping():
    for i in range(2, len(fin)):
        split = fin[i].split(" ")
        edges.append((int(split[0]), int(split[1])))
    #print "edges are: " + str(edges)
    #print str(m), str(n) + "\n"

stripping()

#make dictionary of edges:[list of vertices it connects to] for in_coming
# do same for outgoing 


def num_incoming():
    # if e[1] in dictionary, then increment, else add it to the dict with 1
    for e in edges:
        if e[1] in num_incoming_edges:
            num_incoming_edges[e[1]] += 1
        else:
            num_incoming_edges[e[1]] = 1
    #print "number of incoming edges" + str(num_incoming_edges) + "\n"

num_incoming()

def num_outgoing():
    for e in edges:
        if e[0] in num_outgoing_edges:
            num_outgoing_edges[e[0]] += 1
        else:
            num_outgoing_edges[e[0]] = 1
   # print "number of outgoing edges" + str(num_outgoing_edges) + "\n"

num_outgoing()

def incoming():
    for e in edges:
        if e[1] not in incoming_edges:
            incoming_edges[e[1]] = [e[0]]
        else:
            incoming_edges[e[1]].append(e[0])

 #   print "incoming edges list: " + str(incoming_edges) +"\n"
incoming()

def outgoing():
    for e in edges:
        if e[0] not in outgoing_edges:
            outgoing_edges[e[0]] = [e[1]]
        else:
            outgoing_edges[e[0]].append(e[1])
   # print "outgoing edges list: " + str(outgoing_edges) + "\n"

outgoing()

def set_of_no_incoming():
    for k, v in num_incoming_edges.items():
        if v == 0:
            no_incoming.add(k)
   # print "the set of edges with no incoming edges: " + str(no_incoming) + "\n"

set_of_no_incoming()


def top_order_fncn():
    while len(no_incoming) > 0:
        p = no_incoming.pop()
 #       print p
        top_order.append(p)
        neighbors = outgoing_edges[p]
        for n in neighbors:
            num_incoming_edges[n] -= 1
            if num_incoming_edges[n] == 0:
                no_incoming.add(n)
    if len(top_order) == 0:
        cycle_flag = True
        print "this is not a DAG" + "\n"
    else:
        cycle_flag = False
        #print "the DAG is: " + str(top_order)
    
top_order_fncn()

def find_cycle():
##    for k in num_incoming_edges.items():
##        all_edges.append(k)
##    print all_edges      
    for k, v in num_incoming_edges.items() and num_outgoing_edges.items():
        if v == 0:
            zero_degrees.add(k)
        else:
            non_zero_degrees.add(k)
 #   print "vertices with zero in/out degrees are: " + str(zero_degrees) + "\n"
 #   print "vertices without zero degrees are: " + str(non_zero_degrees) + "\n"

    for k, v in incoming_edges.items() and outgoing_edges.items():
        for e in zero_degrees:
            if e in v:
                flag = True
                v.remove(e)
                if len(v) > 0:
                    cycle.append(k)
                    cycle_flag = True
    if cycle_flag:
        print "there is a cycle produced"
   
find_cycle()


def file_write():
    if cycle_flag:
        finale = open(name[:-3] + ".out", "w")
        finale.write("Cycle:\n")
        for c in cycle:
            finale.write(str(c) + "\n")
        finale.close()
        print cycle
    else:       
        finale = open(name[:-3] + ".out" , 'w')
        finale.write("DAG:\n")
        for t in top_order:
            finale.write(str(t) + "\n")
        finale.close()

file_write()

