import os 
import pickle
import random
import math
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

def read_lewis(dir):
    key_corpus = {}
    tokenizer = RegexpTokenizer(r"\w+")
    for file in os.listdir(dir):
        with open(os.path.join(dir, file), "r") as file_read:
            text = file_read.read()
            parsed_text = BeautifulSoup(text, "lxml")
            articles = parsed_text.html.body.find_all("reuters")
            for a in articles:
                topic = a.topics
                topic = "nondescript" if topic == None else topic.text
                if topic not in key_corpus:
                    key_corpus[topic] = []
                key_corpus[topic] += [tokenizer.tokenize(a.find("text").text)]

    pickle.dump(key_corpus, open("dict/reuters_corpus.pickle", "wb"))

def gather_frequency(corpus, terminology):
    output = {}
    N_gram = 0
    for t in terminology:
        N_gram = max(N_gram, len(t.split(' ')))
        output[t] = 0
    for l in range(len(corpus)):
        # print(float(l)/len(corpus))
        for i in range(1, N_gram+1):
            if l + i > len(corpus):
                break 
            term = ' '.join([x.lower() for x in corpus[l:l+i]])
            if term in output:
                output[term] += 1

    return output
            
    
def extract_terminology(corpus, control_corpuses):
    N_gram = 2 
    common_words = set(stopwords.words('english'))
    chunks = []
    print(len(corpus))
    flattened_corpus = [y for x in corpus for y in x]
    flattened_control_corpus = [y for corp in control_corpuses for x in corp for y in x]
    # Perform preliminary filtering
    flattened_corpus = [x.lower() for x in flattened_corpus if not x.isnumeric()]

    for l in range(1, N_gram+1):
        for i in range(len(corpus)-l+1):
            chunk = ""
            contains_common = False
            for k in flattened_corpus[i:i+l]:
                if k not in common_words:
                    chunk += k + " "
                else:
                    contains_common = True
                    break 
            if contains_common:
                continue
            # print(chunk)
            chunks += [chunk[:-1]]

    candidates = list(set(chunks))
    
    domain_frequency = gather_frequency(flattened_corpus, candidates)
    domain_pertinence = {}
    control_domain_frequency = []
    for corp in flattened_control_corpus+[flattened_corpus]:
        control_domain_frequency += [gather_frequency(corp, candidates)]
    for key in domain_frequency:
        # print("k: " + key + " d: " + str(domain_pertinence[key]) + " m: " + str(max(control_domain_frequency[x][key] for x in range(len(control_domain_frequency)))))
        domain_pertinence[key] = float(domain_frequency[key]) / max(control_domain_frequency[x][key] for x in range(len(control_domain_frequency)))

    lexical_cohesion = {}
    for key in candidates:
        components = key.split(' ')
        if len(components) == 1:
            lexical_cohesion[key] = 1 
        else:
            lexical_cohesion[key] = domain_frequency[key] / sum([domain_frequency[c] for c in components]) * math.log(domain_frequency[key]) * len(components)

    domain_consensus = {}
    for key in candidates:
        domain_consensus[key] = []
    for corp in corpus:
        corpus_occurence = gather_frequency(corp, candidates)
        for key in candidates:
            domain_consensus[key] += [corpus_occurence[key]]
    for key in candidates:
        key_sum = sum(domain_consensus[key])
        key_entropy = -sum([(x/key_sum) * math.log(x/key_sum) for x in domain_consensus[key] if x > 0])
        # The higher the value, the less per-article bias for this keyword 
        domain_consensus[key] = key_entropy 

    term_score = {}
    for key in candidates:
        term_score[key] = 2 * domain_pertinence[key] + lexical_cohesion[key] + domain_consensus[key] * 0.3

    prevalent_pairs = sorted([(key, term_score[key]) for key in term_score], key=lambda x:x[1], reverse = True)[:50]
    return [x[0] for x in prevalent_pairs]

    



    
    




if __name__ == "__main__":  
    os.chdir(os.path.dirname(__file__))
    #read_lewis("reuters")
    key_corpus = pickle.load(open("dict/reuters_corpus.pickle", "rb"))
    
    # trim corpus
    corpus = {}
    for key in key_corpus:
        corpus[key] = []
        for article in key_corpus[key]:
            corpus[key] += [article[:30000]]
    control_corpus = [corpus[key] for key in [random.choice(list(corpus.keys())) for x in range(50)]]
    print(extract_terminology(corpus['interest'], control_corpus))