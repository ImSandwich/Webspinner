from copy import copy 
import random 

def getAccessible(E, r, L):
    for edge in E:
        if edge[0] == r:
            if edge[1] not in L:
                L += [edge[1]]
                getAccessible(E, edge[1], L)
    return L

def getPairs(E):
    return [x[:2] for x in E]

def getWeights(E):
    return [x[2] for x in E]

def getArborescence(E, r, w):
    # Combine weights and edges
    Ew = [a + (b,None) for a,b in zip(E,w)]
    
    # Remove all incoming edges to r
    Ew = list(filter(lambda x: x[1] != r, Ew))
    # Choose among parallel edges for one with lowest weight
    Ew = [(edgePair[0],edgePair[1],\
        min(weightedPair[2] for weightedPair in Ew if weightedPair[:2] == edgePair)) \
            for edgePair in set(getPairs(Ew))]

    vertices, trimmed_Ew = recurArborescence(Ew, r)

    return vertices, getPairs(trimmed_Ew), r, getWeights(trimmed_Ew)

def recurArborescence(Ew, r): # each edge contains inc, out, weight, id
    # Precondition : ensure that r can reach all other vertices 
    V = list(set([x for pair in getPairs(Ew) for x in pair]))
    V_nor = copy(V)
    V_nor.remove(r)
    assert(len(getAccessible(getPairs(Ew), r, [r])) == len(V))

    
    # Get incoming edges of lowest weight
    trimmed_Ew = [min([edgePair for edgePair in Ew if edgePair[1]==vertex], key=lambda x: x[2]) \
            for vertex in V_nor]
    trimmed_pairs = getPairs(trimmed_Ew)
    trimmed_weights = getWeights(trimmed_Ew)
    # Check for cycles
    candidates = copy(V)
    for a in getAccessible(trimmed_pairs, r, [r]):
        candidates.remove(a)
    if len(candidates) == 0:
        return (V, trimmed_Ew)
    else:
        node = random.choice(candidates)
        cycle = [node]
        pi_cycle = {}
        error = False
        while len(cycle) == 1 or cycle[0] != cycle[-1]:
            error = True
            for pair in trimmed_Ew:
                if pair[1] == node:
                    node = pair[0]
                    cycle += [pair[0]]
                    error = False
                    pi_cycle[node] = pair[2]
                    break 
            assert(not error)
        del cycle[-1]
            
        edges_prime = []
        new_vertex = max(V) + 1
        edge_dict = {}
        C_edges = []
        for edge in Ew:
            edge_dict[(edge[0],edge[1])] = edge
            if edge[0] in cycle and edge[1] not in cycle:
                edges_prime += [(new_vertex, edge[1], edge[2], edge[0])]
            elif edge[0] not in cycle and edge[1] in cycle:
                edges_prime += [(edge[0], new_vertex, edge[2]-pi_cycle[edge[1]], edge[1])]
            elif edge[0] not in cycle and edge[1] not in cycle:
                edges_prime += [(edge[0], edge[1], edge[2], None)]
            else:
                C_edges += [edge]
        vertices_prime, edges_prime = recurArborescence(edges_prime, r)
        incoming_edge = [x for x in edges_prime if x[1] == new_vertex][0]
        incoming_edge = (incoming_edge[0], incoming_edge[3])
        output_edges = []

        for edge in edges_prime:
            edge0 = edge[3] if edge[0] == new_vertex else edge[0]
            edge1 = edge[3] if edge[1] == new_vertex else edge[1]
            output_edges += [edge_dict[(edge0,edge1)]]
        for edge in C_edges:
            if edge[1] == incoming_edge[1]:
                pass 
            else:
                output_edges += [edge]
        return (V, output_edges)





edges = [(1,2),(1,3),(3,4),(4,5),(5,3)]
root = 1
weights = [1,3,1,1,1]

vertices, edges, root, weights = getArborescence(edges, root, weights)
print(edges)

