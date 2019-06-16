import nltk
from nltk.corpus import stopwords
from copy import copy
import math 
import re 

lemma =  nltk.WordNetLemmatizer()
stopWords = set(stopwords.words("english"))
D = [] # A pre-loaded list of different domains and their corpus

def extract_pattern(tokens, tags, pattern):
    extracted = []
    for i in range(len(tags) - len(pattern) + 1):
        match = True
        for j in range(len(pattern)):
            index = i + j
            if tags[index] not in pattern[j]:
                match = False
                break 
        if match:
            extracted += [tuple([tokens[x] for x in range(i, i+len(pattern))])]

    return extracted


def extract_terminologies(corpus, D):
    global lemma
    global stopWords
    word_tokens = nltk.word_tokenize(corpus)
    word_tokens = [lemma.lemmatize(x).lower() for x in word_tokens if x not in stopWords]
    corpus = ' '.join(word_tokens)
    word_tags = [x[1] for x in nltk.pos_tag(word_tokens)]
    word_pool = extract_pattern(word_tokens, word_tags, [["NN"], ["NN"]])
    word_pool += extract_pattern(word_tokens, word_tags, [["JJ"], ["NN"]])
    word_pool += extract_pattern(word_tokens, word_tags, [["NN"], ["IN"], ["NN"]])
    word_pool = list(set(word_pool))
    word_pool_str = [(' '.join(x)).strip() for x in word_pool]
    D = copy(D)
    
    D += [corpus]
    scores = [0] * len(word_pool)
    max_freq = [0] * len(word_pool)
    total_freq = [0] * len(word_pool)
    consensus = [0] * len(word_pool)

    for document in D:
        max_freq = [max(max_freq[i], len(list(re.finditer(word_pool_str[i], document)))) for i in range(len(word_pool))]
        total_freq = [a+b for a,b in 
        zip(total_freq, [len(list(re.finditer(word_pool_str[i], document)))
        for i in range(len(word_pool))])]
    print(list(zip(word_pool_str, total_freq)))
    for document in D:
        c_w = []
        for i in range(len(word_pool)):
            f_w = len(list(re.finditer(word_pool_str[i], document)))
            if f_w > 0:
                c_w += [(f_w/total_freq[i]) * -math.log((f_w/total_freq[i]))]
            else:
                c_w += [0]
        consensus = [a+b for a,b in 
        zip(consensus, c_w)]

    scores = [len(list(re.finditer(word_pool_str[i], corpus)))/max_freq[i] + consensus[i] for i in range(len(word_pool))] # Needs further work
    print(scores)
    return word_pool

print(extract_terminologies("""
As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. A quip in Tesler's Theorem says "AI is whatever hasn't been done yet." For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology. Modern machine capabilities generally classified as AI include successfully understanding human speech, competing at the highest level in strategic game systems (such as chess and Go),autonomously operating cars, intelligent routing in content delivery networks, and military simulations.
Artificial intelligence can be classified into three different types of systems: analytical, human-inspired, and humanized artificial intelligence. Analytical AI has only characteristics consistent with cognitive intelligence; generating cognitive representation of the world and using learning based on past experience to inform future decisions. Human-inspired AI has elements from cognitive and emotional intelligence; understanding human emotions, in addition to cognitive elements, and considering them in their decision making. Humanized AI shows characteristics of all types of competencies (i.e., cognitive, emotional, and social intelligence), is able to be self-conscious and is self-aware in interactions with others.
""",[("artificial intelligence artificial intelligence artificial intelligence")]))



