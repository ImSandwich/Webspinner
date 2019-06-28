import pickle 
import time 
from copy import copy 
class WCL :
    def __init__(self):
        self.vertices = []
        self.vertices_weight = [] 
        self.edges = []
        self.last_possible_paths = []
        self.call = 0

    def possible_paths(self):
        N = {}
        for i in range(len(self.vertices)):
            N[i] = []
            for source, dest in self.edges:
                if source == i:
                    N[i] += [dest]
        # print(N)
        startIndex = self.vertices.index("<s>", 0, len(self.vertices))
        stopIndex = self.vertices.index("<e>", 0, len(self.vertices))
        P = self.getPaths(N, startIndex, stopIndex)
        # print(P)
        if P is None:
            P = []
        out = []
        for p in P:
            out += [[]]
            for v in p:
                out[-1] += [(v,self.vertices[v])] 
        return out

    def max_match(self, s1, s2, a, b, mult):
        if a == -1 or b == -1:
            return (0, [])
        if mult[a][b] == -1:  
            C0, P0 = self.max_match(s1,s2,a-1,b-1,mult)
            C1, P1 = self.max_match(s1,s2,a-1,b,mult)
            C2, P2 = self.max_match(s1,s2,a,b-1,mult)
            P0 = copy(P0)
            if s1[a][1] == s2[b][1]:
                C0 += 1
                P0 += [(s1[a][0], s2[b][0])]
            CMax = max(C0, C1, C2)
            if CMax == C0:
                mult[a][b] = (C0, P0) 
            elif CMax == C1:
                mult[a][b] = (C1, P1) 
            else:
                mult[a][b] = (C2, P2)
        
        return mult[a][b]

    def test(self,mult, c):
        if c == -1:
            return
        mult[c][0]=c
        c -= 1
        self.test(mult, c)
    '''
    def max_match2(self, s1, s2, a, b, mult):
        if a == -1 or b == -1:
            return 0
        if mult[a][b] == -1:   
            C0 = self.max_match2(s1,s2,a-1,b-1, mult) + int(s1[a][1]==s2[b][1])
            C1 = self.max_match2(s1,s2,a-1,b, mult)
            C2 = self.max_match2(s1,s2,a,b-1, mult)
            return max(C0, C1, C2)
        else:
            return mult[a][b]
    '''
    def word_match(self, s1, s2):
        mult = []
        for i in range(len(s1)):
            mult += [[]]
            for j in range(len(s2)):
                mult[-1] += [-1]

        r, l = self.max_match(s1, s2, len(s1)-1, len(s2)-1, mult)
        return r, l



    def __repr__(self):
        out = ""
        for p in self.last_possible_paths:
            out += str([x[1] for x in p]) + "\n"
        return out

    def prune(self):
        top = sorted([(self.vertices[x], self.vertices_weight[x]) for x in range(len(self.vertices))], key=lambda x: x[1], reverse=True)[:6]
        top = [x[0] for x in top]
        for i in range(len(self.vertices)-1,-1,-1):
            if self.vertices[i] not in top:

                for e in range(len(self.edges)-1,-1,-1):
                    if self.vertices[i] in self.edges[e]:
                        del self.edges[e]
                del self.vertices[i]
                del self.vertices_weight[i]
        self.last_possible_paths = self.possible_paths()


    def update(self, s, occ):
        s = ["<s>"] + s + ["<e>"]
        M = []
        s = [(x, s[x]) for x in range(len(s))]
        max_score = -1
        

        for p in self.last_possible_paths:
            if s == p:
                
                for i, label in p:
                    self.vertices_weight[i] += occ 
                
                return
            score, matches = self.word_match(s, p)
            if score > max_score:
                max_score = score 
                M = matches 
        
        if max_score == len(s):
            return 
        correlated = {}
        for X, Y in M:
            correlated[X] = Y 

        for i, label in s:
            if i not in correlated:
                self.vertices += [label]
                self.vertices_weight += [0]
                correlated[i] = len(self.vertices)-1

        for i in range(len(s)-1):
            edge = (correlated[i], correlated[i+1])
            if edge not in self.edges:
                self.edges += [edge]
        
        for i in range(len(s)):
            self.vertices_weight[correlated[i]] += occ
        
        self.last_possible_paths = self.possible_paths()
        

        

    def getPaths(self, N, u, v):
        paths = []
        if u == v:
            return [[v]]
        if u not in N:
            return None 
        for c in N[u]:
            P = self.getPaths(N, c, v)
            if P is not None:
                for p in P:
                    paths += [[u]+p]

        
        return paths


def analyze_cluster(cluster):
    vertices = []
    edges = []
    class1 = WCL()
    generalized_freq = {}
    for s in cluster:
        s = tuple(s)
        if s in generalized_freq:
            generalized_freq[s] += 1
        else:
            generalized_freq[s] = 1 
    cluster = sorted([(list(key), generalized_freq[key]) for key in generalized_freq], key = lambda x: x[1], reverse=True)
    cluster = cluster[:50]
    for s in range(len(cluster)):
        print(float(s)/len(cluster))
        class1.update(cluster[s][0], cluster[s][1])
    return class1
    

if __name__ == "__main__":
    '''
    
    
    
    
    class1.update(["In", "NN", "a", "@", "is", "a", "NN"])
    class1.update(["In", "NN", "a", "@", "is", "a", "JJ", "NN"])
    class1.update(["In", "NN", "NN", "a", "@", "is", "a", "NN"]) 



    s1 = ["In", "NN", "a", "@", "is", "a", "NN"]
    s1 = [(x, s1[x]) for x in range(len(s1))]
    s2 = ["In", "NN", "a", "@", "is", "a", "JJ", "NN"]
    s2 = [(x, s2[x]) for x in range(len(s2))]
    '''
    clusters = pickle.load(open("dict/clusters.pickle", "rb"))
    most_common = sorted([(key, len(clusters[key])) for key in clusters], key=lambda x: x[1], reverse=True) 
    for k in range(len(most_common)-1, -1, -1):
        if '@' not in most_common[k][0]:
            del most_common[k]

    lattice = analyze_cluster(clusters[most_common[6][0]])
    lattice.prune()
    

    print(str(lattice))

