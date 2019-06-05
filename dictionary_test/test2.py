import pickle
from test import Node

if __name__ == "__main__":
    word_node_dic = pickle.load(open("pickle/word_node_dic.p","rb"))
    fundamentals = [] 
    for word in word_node_dic:
        iRelations = word_node_dic[word].relations
        iOrdinality = word_node_dic[word].ordinality 
        fundamental =  True
        for relation in iRelations:
            if word_node_dic[relation].ordinality >= iOrdinality:
                fundamental = False
                break
        if fundamental and iOrdinality > 0:
            fundamentals += [(word, iOrdinality)]
    print([x[0] for x in sorted(fundamentals, key=lambda x: x[1], reverse=True)][:250])
