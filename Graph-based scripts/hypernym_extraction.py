from google_define_scraper import definitions_of as google_definitions_of
from nltk.corpus import wordnet

T = set(["Depth-first search", "Cryptography", "Beam search", "Dijkstra’s algorithm", "best-first search", "Search algorithm ", "Numerical algorithm", "Heuristic search algorithm", "Optimal greedy algorithm", "Greedy algorithm", "String matching", "Approximate algorithm", "Breadth first search", "Conquer search algorithm", "Binary search", "Polynomial-time algorithm", "First-order optimization algorithm", "Hash function", "Data mining", "Gradient descent", "Probability inference algorithm", "Public-key encryption algorithm", "Tree search", "Graph mining", "Belief propagation", "Link analysis algorithm", "Bottom-up dynamic programming", "Iterative dynamic programming", "Dynamic programming", "Top-down dynamic programming", "Recursive dynamic programming", "Space-efficient dynamic programming"])
T = set([t.lower() for t in T])
U = set(["object", "abstraction", "algorithm"])
nouns = {x.name().split('.', 1)[0] for x in wordnet.all_synsets('n')}
D = set()

domain_constant = 0.38

def main():
  global D
  D = T.union(get_nouns(T))

  for t in T:
    if(t not in U):
      # Get all definition sentences from WCL
      wcl_defs = []

      # Get all definition sentences from Google
      g_defs = google_definitions_of(t)

      definition_candidates = g_defs + wcl_defs
      
      print(len(definition_candidates), end = '\t')
      new_definition_candidates = []
      for definition in definition_candidates:
        if(domain_weight(definition) > domain_constant):
          new_definition_candidates.append(definition)

      definition_candidates = new_definition_candidates
      print(len(definition_candidates))

def get_nouns(terms):
  ans = set()

  for term in terms:
    ind_words = term.split()

    for word in ind_words:
      if(isNoun(word)):
        ans.add(word)

  return ans

def isNoun(word):
  return word in nouns

def domain_weight(sentence):
  bag = set(sentence.split())
  return len(bag.intersection(D)) / len(bag)


if __name__ == '__main__':
  main()      