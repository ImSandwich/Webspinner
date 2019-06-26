import pickle 
import time 
from copy import copy 
class WCL :
    def __init__(self):
        self.vertices = []
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
        startIndex = self.vertices.index("START", 0, len(self.vertices))
        stopIndex = self.vertices.index("END", 0, len(self.vertices))
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

    def update(self, s):
        s = ["<s>"] + s + ["<e>"]
        M = []
        s = [(x, s[x]) for x in range(len(s))]
        max_score = -1
        
        
        for p in self.last_possible_paths:
            now = time.time()
            
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
                correlated[i] = len(self.vertices)-1

        for i in range(len(s)-1):
            edge = (correlated[i], correlated[i+1])
            if edge not in self.edges:
                self.edges += [edge]

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
    

if __name__ == "__main__":
    '''
    clusters = pickle.load(open("dict/clusters.pickle", "rb"))
    most_common = sorted([(key, len(clusters[key])) for key in clusters], key=lambda x: x[1], reverse=True) 
    analyze_cluster(clusters[most_common[9][0]])
    
    
    



    s1 = ["In", "NN", "a", "@", "is", "a", "NN"]
    s1 = [(x, s1[x]) for x in range(len(s1))]
    s2 = ["In", "NN", "a", "@", "is", "a", "JJ", "NN"]
    s2 = [(x, s2[x]) for x in range(len(s2))]
    '''
    class1 = WCL()
    class1.update(["In", "NN", "a", "@", "is", "a", "NN"])
    class1.update(["In", "NN", "a", "@", "is", "a", "JJ", "NN"])
    class1.update(["In", "NN", "NN", "a", "@", "is", "a", "NN"]) 

    print(str(class1))

