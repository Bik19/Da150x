# import pygame
import heapq
import time
from collections import defaultdict
import heapq
import math
from collections import defaultdict
import queue
import heapq
import math
import time

class Lpa:
    def __init__(self, matrix, S_start, S_goal):
        self.S_start = S_start
        self.S_goal = S_goal 
        self.g = {}
        self.rhs = {}
        self.U = []
        self.S_last = self.S_start
        self.path = []
        self.compute_cost = {}
        self.neighbors = defaultdict(list)
        self.blockSize = 0
        self.prev = S_start
        self.stepCounterMulti = 0

    def h(self, s1, s2):
        return abs(s1[0] - s2[0]) + abs(s1[1] - s2[1])

    def calculateKey(self, s):
        return (min(self.g[s], self.rhs[s] + self.h(s, self.S_goal)), min(self.g[s], self.rhs[s]))

    def initialize(self):
        self.U = []
        for s in self.neighbors:
            self.rhs[s] = float('inf')
            self.g[s] = float('inf')
        self.rhs[self.S_start] = 0
        heapq.heappush(self.U, (self.calculateKey(self.S_start), self.S_start))


    def pickMin(self, u):
        minimum = float('inf')
        s = u
        for successor in self.neighbors[u]:
            if(self.compute_cost[u, successor] + self.g[successor] < minimum):
                minimum = self.compute_cost[u, successor] + self.g[successor]
                s = successor
        return minimum, s
    
    def updateVertex(self, u):
        if u != self.S_start:
            self.rhs[u] = self.pickMin(u)[0]
        if any(u == item[1] for item in self.U):
            self.U = [item for item in self.U if item[1] != u]
            heapq.heapify(self.U)
        if self.g[u] != self.rhs[u]:
            heapq.heappush(self.U, (self.calculateKey(u), u))
  

    def computeShortestPath(self):
        while self.U and (self.U[0][0] < self.calculateKey(self.S_goal) or self.rhs[self.S_goal] != self.g[self.S_goal]):  # self.U and
            _, u = heapq.heappop(self.U)
            if self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for s in self.neighbors.get(u, []):
                    self.updateVertex(s)
            else:
                self.g[u] = float('inf')
                mlist = []
                if u not in self.U:
                    mlist = list(self.neighbors.keys()) + [u]
                for s in mlist:
                    self.updateVertex(s)
        self.createPath()


    def createPath(self):
        start = time.time()
        path = []
        current = self.S_goal 

        if self.g[current] == float('inf'):
            return []  

        path.append(current)
        while current != self.S_start:
            _, next_node = self.pickMin(current)
            if self.g[next_node] == float('inf'):
                return []  
            path.append(next_node)
            current = next_node
        path.reverse()
        self.path = path
            
    def startFinding(self, matrix):
        self.initializeGrid(matrix)
        self.initialize()
    
    def initializeGrid(self, matrix):
        size = len(matrix[0])
        for j in range(size):
            for i in range(size):
                if(matrix[j][i] == 0):
                    if(i+1 < size and matrix[j][i+1] == 0):
                        self.neighbors[(i, j)].append((i+1, j))   
                        self.compute_cost[((i, j), (i+1, j))] = 1 
                    if(j+1 < size and matrix[j+1][i] == 0):
                        self.neighbors[(i, j)].append((i, j+1))  
                        self.compute_cost[((i, j), (i, j+1))] = 1 
                    if(i-1 >= 0 and matrix[j][i-1] == 0):
                        self.neighbors[(i, j)].append((i-1, j) ) 
                        self.compute_cost[((i, j), (i-1, j))] = 1 
                    if(j-1 >= 0 and matrix[j-1][i] == 0):
                        self.neighbors[(i, j)].append((i, j-1) )
                        self.compute_cost[((i, j), (i, j-1))] = 1 
    
