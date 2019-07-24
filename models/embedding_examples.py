from gensim.models import Word2Vec
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# ======================================================================================================================

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

game_name = 'fifa'

# ======================================================================================================================

fortnite_model = Word2Vec.load("../saved_embedding_models/" + game_name + ".model")
# fortnite_model = Word2Vec.load("../saved_embedding_models/" + game_name + ".model")
# print(w2v_model.wv.most_similar(positive=['woman', 'gamer'], negative=['man']))
# w2v_model.similarity(w1='fornite', w2='pubg')
# w2v_model.similarity(w1='fornite', w2='game')
# w2v_model.wv.similarity(w1='fornite', w2='sucks')

# ======================================================================================================================

word_triplets_general = [['man', 'woman', 'gamer'],  # gamergirl - man is to woman as gamer is to gamergirl
                         ['woman', 'bitch', 'man'],  # bitch, slut, crazy
                         ['man', 'bro', 'woman'],  # bitch
                         ['man', 'nigga', 'woman'],
                         ['man', 'winner', 'woman'],
                         ['man', 'woman', 'pro'],
                        ['man','pro','woman'],
                         ['gamer', 'pro', 'woman'],
                         ['man', 'asshole', 'woman'],
                         [ 'man','dude', 'woman'],
                         ['bro', 'dude', 'sister'],
                         ['gamer', 'game', 'woman'],
                         ['man', 'streamer', 'girl'],
                         ['trump', 'president', 'clinton'],
                         ['trump', 'usa', 'clinton'],
                         ['trump', 'clinton', 'man'],
                         ['trump', 'islamophobic', 'clinton'],
                         ['trump', 'muslim', 'man'],
                         ['fortnie', 'pubg', 'trump'],
                          ['trump', 'mexico', 'fortnite'],
                          ['fortnite', 'battleroyale', 'trump'],
                          ['man', 'fortnite', 'woman'],
                          ['gamer', 'fortnite', 'trump']
                          ]

trump_hate =['trump','boldfinger', 'bratman', 'bumbledore', 'chickenhawk', 'taxevader', 'drumpf', 'meathead', 'tictacdough', 'trumpofdoom', 'trumpelthinskin', 'trumpenstein', 'trumpinator', 'trumpocalypse', 'trumptastrophe',
             'trumpkopf', 'groepenfuehrer', 'orangutan', 'trumpamaniac', 'trumpster', 'adolftwitler']



def run_triplet_examples(word_triplets_list):
    print('These are interesting embedding examples from the game : ' + game_name)
    for words_triples in word_triplets_list:
        most_similar = [x[0] for x in fortnite_model.wv.most_similar_cosmul(positive=[words_triples[1], words_triples[2]],
                                                                            negative=[words_triples[0]])]
        print("\n{} is to {} like {} is to: \n{}".format(
            words_triples[0], words_triples[1], words_triples[2], most_similar))


def run_similar_examples(words):
    for word in words:
        try:
            print(fortnite_model.wv.most_similar(positive=word, topn=10))
        except:
            print("word {} is not in vocab".format(word))

# run_triplet_examples(word_triplets_general)
run_similar_examples(trump_hate)


