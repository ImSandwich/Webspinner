import nltk 
from spacy.en import English
from nltk.corpus import gutenberg

sentences = []
for fileid in gutenberg.fileids():
    txt = gutenberg.sents(fileid)
    for sent_array in txt:
        sentences.append(' '.join(sent_array))
    break

doc = ' '.join(sentences)
nlp = English()
doc_processed = nlp(doc)
for sent in doc:
    for token in sent:
        if token.is_alpha:
            print(token.orth +","+ token.tag_ + ","+ token.head.lemma_)