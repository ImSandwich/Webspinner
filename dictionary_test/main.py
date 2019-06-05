import gensim
from nltk.stem.snowball import SnowballStemmer
import queue
from nltk import word_tokenize
import operator
import json
import pickle
import string
# Dictionary = Wikipedia

def fundamental(A, B):
  A = stemmer.stem(A)
  B = stemmer.stem(B)

  loop_iterations = 5
  looked_at = {}

  Q = queue.Queue()
  for word in word_tokenize(definitions[A]):
    word = word.translate(str.maketrans('', '', string.punctuation)).lower()
    Q.put((0, word))  

  for word in word_tokenize(definitions[B]):
    word = word.translate(str.maketrans('', '', string.punctuation)).lower()
    Q.put((0, word))

  while(not Q.empty()):
    if(scores[word] > 0.5):
      print(word, scores[word]) 

    cur_level, word = Q.get()
    if(word not in looked_at):
      looked_at[word] = 1
      if(word in definitions):
        for def_word in word_tokenize(definitions[word]):
          def_word = stemmer.stem(def_word.translate(str.maketrans('', '', string.punctuation)).lower())
          if(cur_level + 1 < loop_iterations):
            Q.put((cur_level + 1, def_word))
    else:
      looked_at[word] += 1

  print()
  print(looked_at[A])
  print(looked_at[B])

# import dictionary
stemmer = SnowballStemmer("english")
graph = {}
graph = pickle.load(open("dictionary_graph.p", "rb"))
lower_definitions = {}
with open("dictionary.json", "r") as read_file:
  definitions = json.load(read_file)

for key in definitions.keys():
  lower_definitions[stemmer.stem(key.lower())] = definitions[key]
definitions = lower_definitions

# for key in definitions.keys():
#   graph[key] = 0
#   for word in definitions[key].split():
#     word = word.translate(str.maketrans('', '', string.punctuation)).lower()
#     graph[word] = graph.get(word, 0) + 1

# pickle.dump(graph, open("dictionary_graph.p", "wb"))

# i = 0
# for (key, value) in sorted(graph.items(), key=operator.itemgetter(1), reverse = True):
#   # if(graph[key] > 10000):
#     # print(key)
#   print(key, value)
#   i += 1
#   if(i > 100):
#     break

model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

scores = {}
for key in definitions.keys():
  for def_word in word_tokenize(definitions[key]):
    def_word = stemmer.stem(def_word.translate(str.maketrans('', '', string.punctuation)).lower())
    try:
      scores[def_word] = scores.get(def_word, 0) + model.similarity(key, def_word)
    except:
      pass

# for (key, value) in sorted(scores.items(), key=operator.itemgetter(1), reverse = True):
#   # if(graph[key] > 10000):
#     # print(key)
#   print(key, value)
#   i += 1
#   if(i > 100):
#     break

fundamental("fruit", "plant")

# a = "mills, "
# print(a.translate(str.maketrans('', '', string.punctuation)))
# get all nodes
# go through definitions
# add edges



# import queue
# import requests
# from bs4 import BeautifulSoup, Comment

# url = "https://en.wikipedia.org/wiki/Credit_derivative"
# max_depth = 2

# urls_to_visit = queue.LifoQueue()
# urls_to_visit.put((url, 0))

# while(not urls_to_visit.empty()):
# 	cur_url, cur_depth = urls_to_visit.get()

# 	if(cur_depth > max_depth):
# 		continue

# 	page = requests.get(cur_url)
# 	soup = BeautifulSoup(page.text, 'lxml')
# 	current_topic = soup.find('h1', {'class':'firstHeading'}).get_text().lstrip().rstrip()

# 	if(page.ok == True):
# 		first_paragraph = soup.find('div', {'class':'mw-parser-output'}).find('p')
# 		all_simpler = first_paragraph.find_all('a')

# 		print("\n\n\n" + current_topic + " depends on ", end='')
# 		for simpler in all_simpler:
# 			# ignore citations
# 			if(simpler['href'][0] != "#"):
# 				urls_to_visit.put(("https://en.wikipedia.org" + simpler['href'], cur_depth + 1))
# 				print(simpler['title'] + ", ", end='')
# 		print()