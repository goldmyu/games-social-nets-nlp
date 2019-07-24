import sys
import pandas as pd
from pandas import DataFrame
from textblob import TextBlob

property = "Sexism" #"Racism" or "Trump-hate"
community = "sims"
path = "../WordsSets/" + property
sys.path.append(path)
import Words

alpha = 1/3
beta = 1/3
gama = 1/3

negative_words = Words.negative_words
neutral_words = Words.neutral_words
DATA_SETS_PATH = '../data-sets/'
name_file = 'clean_no_stop_words_'+community+'.csv'
name_file_withStopWords = 'clean_'+community+'.csv'


def term_freq():
    num_negative_posts = 0
    data = pd.read_csv(DATA_SETS_PATH+name_file)
    df = DataFrame(data)
    row_list = df.values.tolist()

    for row in (row_list):
        if type(row[0]) is str:
            post = row[0].split()
            for word in post:
                if word in negative_words:
                    num_negative_posts += 1
                    break

    ans = num_negative_posts / len(row_list)
    return ans


def sentiment():
    sum_polarity = 0
    num_of_posts = 0
    data = pd.read_csv(DATA_SETS_PATH+name_file_withStopWords)

    for row in data.values:
        if type(row[0]) is str:
            testimonial = TextBlob(row[0])
            post = row[0].split()
            for word in post:
                if word in neutral_words:
                    num_of_posts += 1
                    sum_polarity += testimonial.sentiment.polarity
                    break

    ans = sum_polarity / num_of_posts
    return ans


def embedding():
    return



nem_property = alpha * term_freq() + beta * sentiment() + gama * embedding()

