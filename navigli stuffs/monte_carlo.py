import random
import copy
import math 
import matplotlib.pyplot as plt 

steps = 10000
vertices_label = ["living", "animal", "dog", "cat", "bear", "plant", "grass", "cauliflower", "mango"]
edges = [(0,1), (1,2), (1,3), (1,4), (0,5), (5,6), (5,7), (5,8), (4,7)]
direction = [0 for x in edges]
record = []
upper = [0]

class Node:
    def __init__(self, label):
        self.parent = []
        self.children = [] 
        self.label = label
        self.probability = 0

def getEntropy(vertices, edges, direction):
    nodes = {}
    for i in vertices:
        nodes[i] = Node(i)
    for edgeIndex in range(len(edges)):
        a = edges[edgeIndex][0]
        b = edges[edgeIndex][1]
        if direction[edgeIndex] == 0:
            nodes[a].children += [nodes[b]]
            nodes[b].parent += [nodes[a]]
        elif direction[edgeIndex] == 1:
            nodes[b].children += [nodes[a]]
            nodes[a].parent += [nodes[b]]
    current_layer = [nodes[x] for x in nodes if len(nodes[x].parent)==0]
    leaf_layer = [nodes[x] for x in nodes if len(nodes[x].children)==0]
    while len(current_layer) > 0:
        new_layer = []
        for n in current_layer:
            if len(n.parent) == 0:
                n.probability =  1.0/len(current_layer)
            else:
                for p in n.parent:
                    n.probability += p.probability/len(p.children)
            for c in n.children:
                incomplete = False
                for p in c.parent:
                    if p.probability == 0:
                        incomplete = True
                        break
                if not incomplete:
                    new_layer = new_layer + [c]

        current_layer = new_layer

    return -sum(x.probability * math.log(x.probability) for x in leaf_layer)

def validate(vertices, edges, direction, upper):
    nodes = {}
    for i in vertices:
        nodes[i] = Node(i)
    for edgeIndex in range(len(edges)):
        a = edges[edgeIndex][0]
        b = edges[edgeIndex][1]
        if direction[edgeIndex] == 0:
            nodes[a].children += [nodes[b]]
            nodes[b].parent += [nodes[a]]
        elif direction[edgeIndex] == 1:
            nodes[b].children += [nodes[a]]
            nodes[a].parent += [nodes[b]]
    current_layer = [nodes[x] for x in nodes if len(nodes[x].parent)==0]
    current_layer = sorted([x.label for x in current_layer])
    upper.sort()
    return len(current_layer) == len(upper) and current_layer == upper


for i in range(steps):
    
    original_entropy = getEntropy(range(len(vertices_label)), edges, direction)
    record += [original_entropy]
    flipIndex = -1
    while True:
        flipIndex = random.randint(0, len(direction) - 1)
        direction[flipIndex] = 1 - direction[flipIndex]
        if validate(range(len(vertices_label)), edges, direction, upper):
            break
        else:
            direction[flipIndex] = 1 - direction[flipIndex]

    after_entropy = getEntropy(range(len(vertices_label)), edges, direction)
    constant = 100
    alpha = 0 if after_entropy == 0 else math.exp(constant*after_entropy)
    beta = 0 if original_entropy == 0 else math.exp(constant*original_entropy)
    print(alpha/(alpha+beta))
    if random.uniform(0,1) <= alpha/(alpha+beta):
        pass
    else:
        # revert
        direction[flipIndex] = 1 - direction[flipIndex]

plt.plot(range(steps), record)
plt.show()

print(direction)