from gensim.models import Word2Vec
from WordsSets.SexismRacismTrumpWords import *

# ======================================================================================================================

games_models_list = {
    'fortnite': Word2Vec.load("../saved_embedding_models/fortnite.model"),
    'pubg': Word2Vec.load("../saved_embedding_models/pubg.model"),
    'fifa': Word2Vec.load("../saved_embedding_models/fifa.model"),
    'minecraft': Word2Vec.load("../saved_embedding_models/minecraft.model"),
    'bloodstained': Word2Vec.load("../saved_embedding_models/bloodstained.model"),
    'lol': Word2Vec.load("../saved_embedding_models/lol.model"),
    'overwatch': Word2Vec.load("../saved_embedding_models/overwatch.model"),
    'sims': Word2Vec.load("../saved_embedding_models/sims.model"),
    'wow': Word2Vec.load("../saved_embedding_models/wow.model"),
    'dota2': Word2Vec.load("../saved_embedding_models/dota2.model"),
}

# ======================================================================================================================

word_triplets = [['man', 'woman', 'gamer'],  # gamergirl - man is to woman as gamer is to gamergirl
                 ['woman', 'bitch', 'man'],  # bitch, slut, crazy
                 ['man', 'bro', 'woman'],  # bitch
                 ['man', 'nigga', 'woman'],
                 ['man', 'winner', 'woman'],
                 ['man', 'woman', 'pro'],
                 ['man', 'pro', 'woman'],
                 ['gamer', 'pro', 'woman'],
                 ['man', 'asshole', 'woman'],
                 ['man', 'dude', 'woman'],
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


def run_triplet_examples(model, _word_triplets):
    for words_triples in _word_triplets:
        most_similar = [x[0] for x in model.wv.most_similar_cosmul(positive=[words_triples[1], words_triples[2]],
                                                                   negative=[words_triples[0]])]
        print("\n{} is to {} like {} is to: \n{}".format(
            words_triples[0], words_triples[1], words_triples[2], most_similar))


def run_similar_examples(model, words):
    for word in words:
        try:
            print("most similar words to '{}' are {}".format(word, model.wv.most_similar(positive=word, topn=10)))
        except:
            print("word {} is not in vocab".format(word))


def find_all_triplets():
    for game_name, game_w2v_model in games_models_list.items():
        try:
            print('Most intersting triplet examples for the game : ' + game_name)
            run_triplet_examples(game_w2v_model, word_triplets)
        except Exception as e:
            print("For game {}, got the following error:\n{}".format(game_name, str(e)))


def find_most_similar_words(lists_of_words):
    for game_name, game_w2v_model in games_models_list.items():
        for attribute, words in lists_of_words.items():
            try:
                print('Printing similar words to {} in the game : {}'.format(attribute, game_name))
                run_similar_examples(game_w2v_model, words)
            except Exception as e:
                print("For game {}, got the following error:\n{}".format(game_name, str(e)))


# ================================= run functions ================================================================
# find_all_triplets()
# find_most_similar_words(lists_of_negative_words)
find_most_similar_words(lists_of_neutral_words)
