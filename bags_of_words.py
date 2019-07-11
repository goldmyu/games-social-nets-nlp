# import nltk
# nltk.download()
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd
from pandas import DataFrame
from nltk.corpus import stopwords

DATA_SETS_PATH = "data-sets/fortnite_clean.csv"
data = pd.read_csv(DATA_SETS_PATH)
df = DataFrame(data)
row_list = df.values.tolist()
words_list = []

for row in (row_list):
    if type(row[0]) is str:
        list = row[0].split()
        words_list.extend(list)

# stop_words_set = set(stopwords.words("english"))
# words_list = [w for w in words_list if w not in stop_words_set]
c = Counter(words_list)
print(c.most_common(1000))
print("f")
