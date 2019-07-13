import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# nltk.download('punkt')
# nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


game_name = 'pubg_text'
data_set_folder = "../data-sets/cleaned-data-sets/"
df = pd.read_csv(data_set_folder + "/clean_" + game_name + ".csv")

sentences = []
for i in range(df.shape[0]):
    sentence = df.loc[i].loc['text']
    if isinstance(sentence, str):
        sentence = sentence.lower()
        word_tokens = word_tokenize(sentence)

        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        sentence = ' '.join(word for word in filtered_sentence)
        sentences.append(sentence)

df_no_stop_words = pd.DataFrame(sentences, columns=['text'])
df_no_stop_words.to_csv(data_set_folder + "clean_no_stop_words_" + game_name + ".csv", index=False)
