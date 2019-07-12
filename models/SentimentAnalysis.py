from textblob import TextBlob
import numpy as np
import pandas as pd

path = 'data-sets/clean-full-fortnite-no-duplicates.csv'
data = pd.read_csv(path)
results = []

for twite in data.values:
    if type(twite[0]) is str:
        testimonial = TextBlob(twite[0])
        results.append([testimonial.sentiment.polarity, testimonial.sentiment.subjectivity])

df = pd.DataFrame(data=np.array(results), columns=['polarity', 'subjectivity'])
df.to_csv('data-sets/Results/Sentiment/fortnite.csv')

