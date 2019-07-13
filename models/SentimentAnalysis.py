from textblob import TextBlob
import numpy as np
import pandas as pd

path = 'data-sets/'
file_name = 'clean-full-fortnite-no-duplicates.csv'
data = pd.read_csv(path+file_name)
results = []

polarity_sum = 0
subjectivity_sum = 0

for twite in data.values:
    if type(twite[0]) is str:
        testimonial = TextBlob(twite[0])
        polarity_sum += testimonial.sentiment.polarity
        subjectivity_sum += testimonial.sentiment.subjectivity
        results.append([twite[0], testimonial.sentiment.polarity, testimonial.sentiment.subjectivity])

df = pd.DataFrame(data=np.array(results), columns=['twite','polarity', 'subjectivity'])
df.to_csv(path+'Results/Sentiment/'+file_name)

# average
polarity_avg = polarity_sum / len(results)
subjectivity_avg = subjectivity_sum / len(results)
array = [[polarity_avg, subjectivity_avg, len(results)]]

df_avg = pd.DataFrame(data=np.array(array), columns=['polarity_avg', 'subjectivity_avg', 'num_of_twites'])
df_avg.to_csv(path+'Results/Sentiment_Average/'+file_name)
