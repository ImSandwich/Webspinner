from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
import os 
import pickle 
import gensim 
import json 
import re

class Node:

    def __init__(self, word):
        self.word = word 
        self.ordinality = 0
        self.relations = {}

    def print_traversal(self, reference, upward, index):
        if index >= 5:
            return
        print("---" * index + self.word + "("+ str(self.ordinality)+")")
        input()
        for rel_string in self.relations:
            rel = reference[rel_string]
            if (upward and rel.ordinality > self.ordinality) or \
            (not upward and rel.ordinality < self.ordinality):
                rel.print_traversal(reference, upward, index+1)

def translate_pos(inp):
    if inp in ["JJ", "JJR", "JJS", "RB", "RBS"]:
        return "a"
    if inp in ["VB","VBD","VBG","VBN","VBP","VBZ"]:
        return "v"
    return "n"

def lemmatized_words(lemmatizer, sentence, criteria):
    tokens = word_tokenize(sentence)
    pos_tags = pos_tag(tokens)
    output = [] # May contain duplicates, such that more mentions lead to stronger correlation
    if len(pos_tags) != len(tokens):
        return False
    for i in range(len(pos_tags)):
        tag = pos_tags[i]
        if tag[1] in criteria:
            output.append(lemmatizer.lemmatize(tag[0], pos=translate_pos(pos_tag([tag[0]])[0][1])))

    return output

def simpler_sentence(model, reference, lemmatizer, sentence):
    tokens = word_tokenize(sentence)
    output = ""
    pos_tags = pos_tag(tokens)
    for tag in pos_tags:
        base = tag[0].lower()
        if tag[1] in ["NN", "NNS", "NNP", "NNPS", "JJ", "JJR", "JJS", "RB", "RBS","VB","VBD","VBG","VBN","VBP","VBZ" ]:
            base = lemmatizer.lemmatize(tag[0].lower(), pos = translate_pos(pos_tag[tag[0].lower()][0][1]))
            if base in reference:
                most_similar_relations = [(x, model.similarity(base,x) ) for x in reference[base].relations if reference[x].ordinality > reference[base].ordinality]
                most_similar_relations = sorted(most_similar_relations, key=lambda x: x[1], reverse=True)
                base = most_similar_relations[0][0] if len(most_similar_relations) > 0 else base
        output += base + " "
    return output



'''
word_node_vec = {}
word_node_vec["seed"] = Node("seed")
word_node_vec["seed"].relations["plant"]=True
word_node_vec["plant"] = Node("plant")
word_node_vec["plant"].ordinality = 1 

#word_node_dic["seed"].print_traversal(word_node_dic, True, 0)
'''
if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))


    wordnet_lemmatizer = WordNetLemmatizer()
    model = None
    word_node_dic = {} 
    definitions = None

    if os.path.isfile("pickle/dictionary_pickle.p"):
        print("File detected")
        definitions = pickle.load(open("pickle/dictionary_pickle.p","rb"))
    else:
        print("Reading file")
        with open("dict/dictionary.json", "r") as read_file:
            definitions = json.load(read_file)
    
        
        with open("dict/pg29765.txt", "r") as fileOpen:
            txt = ""
            line = fileOpen.read()
            matches = re.finditer('[A-Z]+(?=\n)', line)
            matches2 = re.finditer('(?<=Defn: )(.+(\n))*', line)
            while True:
                try:
                    word = next(matches).group(0)
                    definition = next(matches2).group(0)
                    if word not in definitions:
                        definitions[word] = definition
                    else:
                        definitions[word] += definition
                except StopIteration:
                    break
            

        pickle.dump(definitions, open("pickle/dictionary_pickle.p","wb"))
        

    if os.path.isfile("pickle/model_pickle.p"):
        print("Model detected")
        model = pickle.load(open("pickle/model_pickle.p","rb"))
    else:
        print("Reading model")
        model = gensim.models.KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True) 
        pickle.dump(model, open("pickle/model_pickle.p","wb"))
        

    progress = 0
    percentage = 0
    report_interval = int(len(definitions)/100)
    print("Start")
    for word in definitions:
        word = wordnet_lemmatizer.lemmatize(word.lower(),pos=translate_pos(pos_tag([word])[0][1]))
        word_node_dic[word] = Node(word)

    for word in definitions:
        progress+= 1
        if progress % report_interval == 0:
            progress = 0
            percentage+= 1
            print(percentage)
        if pos_tag(word)[0][1] in ["NN", "NNS", "NNP", "NNPS", "JJ", "JJR", "JJS", "RB", "RBS","VB","VBD","VBG","VBN","VBP","VBZ"]:
            if pos_tag(word)[0][1] in ["NN", "NNS", "NNP", "NNPS"]:
                related = lemmatized_words(wordnet_lemmatizer, definitions[word],["NN", "NNS", "NNP", "NNPS"])
            elif pos_tag(word)[0][1] in ["JJ", "JJR", "JJS", "RB", "RBS"]:
                related = lemmatized_words(wordnet_lemmatizer, definitions[word],["JJ", "JJR", "JJS", "RB", "RBS"])
            elif pos_tag(word)[0][1] in ["VB","VBD","VBG","VBN","VBP","VBZ"]:
                related = lemmatized_words(wordnet_lemmatizer, definitions[word],["VB","VBD","VBG","VBN","VBP","VBZ"])
            word = wordnet_lemmatizer.lemmatize(word.lower(), pos=translate_pos(pos_tag([word])[0][1]))
            for related_noun in related:
                if related_noun not in word_node_dic:
                    continue 
                try:  
                    word_node_dic[word].ordinality += model.similarity(word, related_noun)
                except:
                    pass
                word_node_dic[word].relations[related_noun]=True
                word_node_dic[related_noun].relations[word]=True

    #word_node_dic = pickle.load(open("dic.p","rb"))
    pickle.dump(word_node_dic, open("word_node_dic.p","wb"))
    word_rankings = [(word_node_dic[x].word, word_node_dic[x].ordinality) for x in word_node_dic]
    word_rankings = sorted(word_rankings, key=lambda x:x[1], reverse=True)
    print(word_rankings[:100])


    while (True):
        print(simpler_sentence(model, word_node_dic, wordnet_lemmatizer, input()))
        #word_node_dic[input()].print_traversal(word_node_dic, False, 0)
