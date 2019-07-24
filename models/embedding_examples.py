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

word_triplets = [
    # Sexist
    ['man', 'woman', 'gamer'],  # gamergirl - man is to woman as gamer is to gamergirl
    ['woman', 'bitch', 'man'],  # bitch, slut, crazy
    ['man', 'bro', 'woman'],  # bitch
    ['man', 'winner', 'woman'],
    ['man', 'woman', 'pro'],
    ['gamer', 'pro', 'gamergirl'],
    ['man', 'pro', 'woman'],
    ['man', 'asshole', 'woman'],
    ['man', 'dude', 'woman'],
    ['bro', 'dude', 'sister'],
    ['gamer', 'game', 'gamergirl'],
    ['man', 'streamer', 'girl'],

    # Racist
    ['man', 'nigga', 'woman'],
    ['hitler', 'jews', 'trump'],
    ['jews', 'nazis', 'mexicans'],
    ['jews', 'nazis', 'arabs'],
    ['arabs', 'jews', 'mexicans'],
    ['arabs', 'islam', 'jews'],
    ['arabs', 'islam', 'americans'],
    ['jew', 'nazi', 'mexican'],

    # Trump
    ['trump', 'president', 'clinton'],
    ['trump', 'usa', 'clinton'],
    ['trump', 'clinton', 'man'],
    ['trump', 'islamophobic', 'clinton'],
    ['trump', 'muslim', 'man'],

    # Games related
    ['fortnie', 'pubg', 'trump'],
    ['trump', 'mexico', 'fortnite'],
    ['fortnite', 'battleroyale', 'trump'],
    ['man', 'fortnite', 'woman'],
    ['gamer', 'fortnite', 'trump']
]


def run_triplet_examples(model, _word_triplets, game_name):
    for words_triples in _word_triplets:
        try:
            most_similar = [x[0] for x in model.wv.most_similar_cosmul(positive=[words_triples[1], words_triples[2]],
                                                                       negative=[words_triples[0]])]
            print("{} is to {} like {} is to: {}".format(
                words_triples[0], words_triples[1], words_triples[2], most_similar))
        except Exception as e:
            print("For game {}, got the following error: {}".format(game_name, str(e)))


def run_similar_examples(model, words, game_name):
    for word in words:
        try:
            sim_words = []
            simimlar_words = model.wv.most_similar(positive=word, topn=10)
            for item in simimlar_words:
                sim_words.append(item[0])
            print("most similar words to '{}' are {}".format(word, sim_words))
        except:
            print("word {} is not in the gmae {} vocab".format(word, game_name))


def find_all_triplets():
    for game_name, game_w2v_model in games_models_list.items():
        print('Most interesting triplet examples for the game : ' + game_name)
        run_triplet_examples(game_w2v_model, word_triplets, game_name)
        print("\n\n")


def find_most_similar_words(lists_of_words):
    for game_name, game_w2v_model in games_models_list.items():
        for attribute, words in lists_of_words.items():
            print("Printing similar words to '{}' in the game : {}".format(attribute, game_name))
            run_similar_examples(game_w2v_model, words, game_name)
            print("\n\n")


# ================================= run functions ================================================================
# find_all_triplets()
# find_most_similar_words(lists_of_negative_words)
find_most_similar_words(lists_of_neutral_words)
