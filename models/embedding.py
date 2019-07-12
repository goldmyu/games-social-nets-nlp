from gensim.test.utils import get_tmpfile
from gensim.models import Word2Vec
import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# ======================================================================================================================

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# ======================================================================================================================

path = get_tmpfile("word2vec.model")
game_name = 'pubg'
df = pd.read_csv("data-sets/cleaned-data-sets/clean_no_stop_words_" + game_name + ".csv")

# ======================================================================================================================

data_stream = []
for i in range(df.shape[0]):
    sentence = df.loc[i].loc['text']
    word_tokens = word_tokenize(sentence)
    data_stream.append(word_tokens)


w2v_model = Word2Vec(min_count=7,
                     window=5,
                     size=70,
                     negative=5,
                     sg=2,
                     workers=4)

w2v_model.build_vocab(data_stream, progress_per=100)
w2v_model.train(data_stream, total_examples=w2v_model.corpus_count, epochs=50, report_delay=1)
w2v_model.wv.most_similar(positive=['woman', 'king'], negative=['man'])
w2v_model.save("saved_embedding_models/" + game_name + ".model")

