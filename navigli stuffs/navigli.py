def getPaths(N, u, v):
    
    paths = []
    if u == v:
        return [[v]]
    if u not in N:
        return None 
    for c in N[u]:
        P = getPaths(N, c, v)
        if P is not None:
            for p in P:
                paths += [[u]+p]

    
    return paths

'''
PRECONDITION:
1. Graph is fully connected
2. Has roots
Complexity:
'''
def getWeight(E, U, L):
    # Get all vertices from edges
    V = sorted(list(set([v for p in E for v in p])))
    N = {}
    for v in V:
        N[v] = [x[1] for x in E if x[0]==v]

    # Ensure that the given upper nodes exist in the graph
    assert(all([x in V for x in U]))

    # Remove false roots 
    non_roots = set([x[1] for x in E])
    false_roots = set(V) - set (non_roots) - set(U)
    for f in false_roots:
        V.remove(f)

    # Assign weight to all nodes
    V_weight = {}
    for v in V:
        q = [v]
        visited = [v]
        while len(q) > 0:
            first = q[0]
            q = q[1:]
            for c in N[first]:
                if c not in visited:
                    q = q + [c]
                    visited = visited + [c]

        V_weight[v] = len(set(visited) & set(L))


    # Assign edge_weight to all nodes
    V_weight2 = {}
    for v in V:
        root_to_node = []
        for u in U:
            P = getPaths(N, u, v)
            if v == 1:
                pass
            cost = 0
            if len(P) > 0:
                for p in P:
                    cost = max(cost, sum(V_weight[x] for x in p))
            root_to_node += [cost]
        V_weight2[v] = max(root_to_node)
    
    output = []
    for e in edges:
        if e[0] in V_weight2:
            output += [V_weight2[e[0]]]
        else:
            output += [-1]

    return output



edges = [(0,1),(0,2),(0,3), (1,5), (1,6), (1,7), (2,3), (2,4), (3,4), (5,7),(8,1)]
root = [0]
leaf = [3,4,5,6,7]
E_weight = getWeight(edges, root, leaf)
for i in range(len(E_weight)):
    print(str(edges[i]) + ": " + str(E_weight[i]))
