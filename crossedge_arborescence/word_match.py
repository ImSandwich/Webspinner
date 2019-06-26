import os 
import pickle
from nltk import word_tokenize, pos_tag 
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet
def max_match(s1, s2, a, b):
    if a == -1 or b == -1:
        return 0

    return max(max_match(s1,s2, a-1, b-1) + int(s1[a]==s2[b]), max_match(s1, s2,a-1, b), max_match(s1, s2, a, b-1))

def word_match(s1, s2):
    s1 = s1.split(' ')
    s2 = s2.split(' ')
    return max_match(s1, s2, len(s1)-1, len(s2)-1)

def is_hypernym(word, hyp):
    candidates = [str(y) for x in wordnet.synsets(word) for y in x.hypernyms()]
    return any([str(x) in candidates for x in wordnet.synsets(hyp)])

def generalize_sentence(tokens, d, f, wildcard=False):
    pos_tags = pos_tag(tokens)
    out = []
    wildcard_last = False
    contains_word = False
    contains_hypernym = False
    for p in pos_tags:
        word, pos = p
        if word == d:
            out += ["@"]
            contains_word = True
            wildcard_last = False
        elif word in f:
            out += [word]
            wildcard_last = False
        else:
            if wildcard:
                if not wildcard_last:
                    out += "*"
                    wildcard_last = True
            else:
                if is_hypernym(d, word):
                    contains_hypernym = True
                    out += [pos + "x"]
                else:
                    out += [pos]
    return out, contains_word and contains_hypernym

def extract_dictionary(file):
    f = open(file, "r")
    dic = {}
    line = f.readline()
    tokenizer = RegexpTokenizer(r"\w+")

    while line != "":
        if line == "\n":
            line = f.readline()
            continue
        sp = line.split(' ')
        definiendum = sp[3].lower()

        
        definition = [x.lower() for x in tokenizer.tokenize(' '.join(sp[5:]))]
        if definiendum in dic:
            dic[definiendum] += [definition]
        else:
            dic[definiendum] = [definition]
        line = f.readline()
        
    f.close()
    return dic
def generate_WCL(w, theta):
    word_freq = {}
    total = 0
    tokenizer = RegexpTokenizer(r"\w+")
    for s in w:
        tokens = [y for x in w[s] for y in x]
        for t in tokens:
            if t not in word_freq:
                word_freq[t] = 1 
            else:
                word_freq[t] = word_freq[t] + 1 
            total += 1

    for key in word_freq:
        word_freq[key] /= float(total)
    
    common_words = sorted([(key, word_freq[key]) for key in word_freq], key=lambda x:x[1], reverse = True)
    common_words = [x[0] for x in common_words[:theta]]
    clusters = {}
    T = len(w.keys())
    R = int(T/100)
    I = 0

    for key in w:
        I = I + 1
        if I % R == 0:
            print(float(I)/T)
        definitions = w[key]
        for d in definitions:
            cluster, contains_word = tuple(generalize_sentence(d, key, common_words, wildcard=True))
            if not contains_word:
                continue
            if cluster not in clusters:
                clusters[cluster] = []
            clusters[cluster] += [generalize_sentence(d, key, common_words, wildcard=False)]

    pickle.dump(clusters, open("dict/clusters.pickle","wb"))

    most_common_clusters = sorted([(key, len(clusters[key])) for key in clusters], key=lambda x: x[1], reverse=True)
    print(most_common_clusters[:50])
            

os.chdir(os.path.dirname(__file__))
if os.path.exists("dict/word_dic.pickle"):
    w = pickle.load(open("dict/word_dic.pickle","rb"))
else:
    w = extract_dictionary("dict/azdictionary.txt")
    pickle.dump(w, open("dict/word_dic.pickle","wb"))

generate_WCL(w, 100)


#print(word_match("a quick brown fox jumped over a lazy dog", "a quick fox jumped over a lazy dog"))