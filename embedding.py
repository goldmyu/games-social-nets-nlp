from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec
import pandas as pd
import pickle

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# nltk.download('punkt')
# nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

path = get_tmpfile("word2vec.model")
#
# df = pd.read_csv('data-sets/clean_fortnite.csv')
# df2 = pd.read_csv('data-sets/clean_subreddit-fortnite.csv')
# df3 = pd.read_csv('data-sets/clean-fortnite-no-duplicates.csv')
# df= df.append(df2, ignore_index=False)
# df= df.append(df3, ignore_index=False)
#
# df = df.drop_duplicates()
# df.to_csv("clean-fortnite-no-duplicates2.csv", index=False)
df = pd.read_csv("clean-fortnite-no-duplicates-no-stopwords.csv")

clean_data = []
for i in range(df.shape[0]):
    sentence = df.loc[i].loc['text']
    if isinstance(sentence, str):
        sentence = sentence.lower()
        word_tokens = word_tokenize(sentence)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]

        filtered_sentence = []

        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        clean_data.append(filtered_sentence)
        # print(word_tokens)
        # print(filtered_sentence)
# with open('fortnite-lowered', 'wb') as fp:
#     pickle.dump(clean_data, fp)
#
# with open ('fortnite-lowered', 'rb') as fp:
#     itemlist = pickle.load(fp)


#
w2v_model = Word2Vec(min_count=7,
                     window=5,
                     size=70,
                     negative=5,
                     sg=1,
                     workers=4)

w2v_model.build_vocab(clean_data, progress_per=10000)
w2v_model.train(clean_data, total_examples=w2v_model.corpus_count, epochs=50, report_delay=1)

# model = Word2Vec(common_texts, size=100, window=5, min_count=1, workers=4)

# model = Word2Vec(clean_data, size=300, window=5, min_count=4, workers=4)
# model.train(clean_data, total_examples=len(clean_data), epochs=10)

w2v_model.wv.most_similar(positive=['woman', 'king'], negative=['man'])
w2v_model.save("fortnite.model")
# with open ('fortnite-lowered', 'rb') as fp:
#     itemlist = pickle.load(fp)


#
# w2v_model = Word2Vec(min_count=2,
#                      window=5,
#                      size=300,
#                      sample=6e-5,
#                      alpha=0.03,
#                      min_alpha=0.0007,
#                      negative=0,
#                      workers=4)
#
# w2v_model.build_vocab(clean_data, progress_per=10000)
# w2v_model.train(clean_data, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)

# model = Word2Vec(common_texts, size=100, window=5, min_count=1, workers=4)
#
# model = Word2Vec(clean_data, size=200, window=4, min_count=4, workers=4)
# # model.train(clean_data, total_examples=len(clean_data), epochs=100)
#
# model.wv.most_similar(positive=['woman', 'king'], negative=['man'])
