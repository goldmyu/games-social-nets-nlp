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

game_name = 'fortnite'

# ======================================================================================================================

w2v_model = Word2Vec.load("../saved_embedding_models/" + game_name + ".model")
print(w2v_model.wv.most_similar(positive=['woman','gamer'], negative=['men']))


vocab = []
for word in list(w2v_model.wv.vocab):
    if word not in stop_words:
        vocab.append(word)

X = w2v_model[vocab]
tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)
df_tsne = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])
df_tsne.to_csv("tsne_" + game_name + ".csv", index= False)

plt.figure(figsize=(40, 30))
plt.scatter(df_tsne['x'], df_tsne['y'])
for word, pos in df_tsne.iterrows():
    plt.annotate(word, pos)
plt.show()
plt.savefig(game_name + "tsne_plot")