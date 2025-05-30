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


class Dstar:
    
    def __init__(self, matrix, S_start, S_goal):
        self.matrix = matrix
        self.S_start = S_start
        self.S_goal = S_goal
        self.g = {}
        self.rhs = {}
        self.U = []
        self.S_last = self.S_start
        self.km = 0
        self.path = []
        self.changed_edges = {}
        self.compute_cost = {}
        self.neighbors = defaultdict(list)
        self.blockSize = 0
        self.pos = S_start

    def h(self, s1, s2):
        return abs(s1[0] - s2[0]) + abs(s1[1] - s2[1])

    def calculateKey(self, s):
        return (min(self.g[s], self.rhs[s] + self.h(self.S_start, s) + self.km), min(self.g[s], self.rhs[s]))

    def initialize(self):
        self.U = []
        for s in self.neighbors:
            self.rhs[s] = float('inf')
            self.g[s] = float('inf')
        self.rhs[self.S_goal] = 0
        heapq.heappush(self.U, (self.calculateKey(self.S_goal), self.S_goal)) 
        
    def pickMin(self, u):
        minimum = float('inf')
        s = u
        for successor in self.neighbors[u]:
            if(self.compute_cost[u, successor] + self.g[successor] <= minimum):
                minimum = self.compute_cost[u, successor] + self.g[successor]
                s = successor
        return minimum, s
    
    def updateVertex(self, u):
        if u != self.S_goal:
            self.rhs[u] = self.pickMin(u)[0]

        in_U = any(u == item[1] for item in self.U)

        if self.g[u] != self.rhs[u] and in_U:
            self.U = [item for item in self.U if item[1] != u] 
            heapq.heapify(self.U)
            heapq.heappush(self.U, (self.calculateKey(u), u))  

        elif self.g[u] != self.rhs[u] and not in_U:
            heapq.heappush(self.U, (self.calculateKey(u), u))

        elif self.g[u] == self.rhs[u] and in_U:
            self.U = [item for item in self.U if item[1] != u]
            heapq.heapify(self.U)


    def computeShortestPath(self):
        while self.U and (self.U[0][0] < self.calculateKey(self.S_start) or self.rhs[self.S_start] > self.g[self.S_start]):
            k_old, u = heapq.heappop(self.U)
            k_new = self.calculateKey(u)

            if k_old < k_new:
                heapq.heappush(self.U, (k_new, u))

            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for s in self.neighbors.get(u, []):
                    if s != self.S_goal:
                        self.rhs[s] = min(self.rhs[s], self.compute_cost[s, u] + self.g[u])
                    self.updateVertex(s)

            else:
                g_old = self.g[u]
                self.g[u] = float('inf')
                for s in self.neighbors.get(u, []) + [u]:
                    if s!= u and self.rhs[s] == self.compute_cost[s, u] + g_old:
                        if s != self.S_goal:
                            self.rhs[s] = min(self.compute_cost[s, sp] + self.g[sp] for sp in self.neighbors.get(s, []))
                    self.updateVertex(s)

    
    def startFinding(self):
        self.S_last = self.S_start
        self.initializeGrid(self.matrix)
        self.initialize()
        self.computeShortestPath()
    
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
    
