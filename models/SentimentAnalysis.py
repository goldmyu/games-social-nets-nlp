from textblob import TextBlob
import numpy as np
import pandas as pd

path = '../data-sets/'
name =''# 'clean_'
files = ['fortnite_clean', 'clean-full-fortnite-no-duplicates']


def calc(file_name):
    data = pd.read_csv(path+file_name)

    polarity_sum = 0
    subjectivity_sum = 0
    positive_polarity_sum = 0
    negative_polarity_sum = 0
    positive_polarity_num = 0
    negative_polarity_num = 0
    neutral_polarity_num = 0

    for row in data.values:
        if type(row[0]) is str:
            testimonial = TextBlob(row[0])
            polarity_sum += testimonial.sentiment.polarity
            subjectivity_sum += testimonial.sentiment.subjectivity
            # results.append([twite[0], testimonial.sentiment.polarity, testimonial.sentiment.subjectivity])
            # case polarity is positive
            if testimonial.sentiment.polarity > 0:
                positive_polarity_sum += testimonial.sentiment.polarity
                positive_polarity_num += 1
            # case polarity is negative
            elif testimonial.sentiment.polarity < 0:
                negative_polarity_sum += testimonial.sentiment.polarity
                negative_polarity_num += 1
            else:
                neutral_polarity_num += 1


    # df = pd.DataFrame(data=np.array(results), columns=['twite','polarity', 'subjectivity'])
    # df.to_csv(path+'Results/Sentiment/'+file_name)

    # average
    num_of_rows = positive_polarity_num + negative_polarity_num + neutral_polarity_num
    polarity_avg = polarity_sum / num_of_rows
    subjectivity_avg = subjectivity_sum / num_of_rows
    positive_polarity_avg = positive_polarity_sum / positive_polarity_num
    negative_polarity_avg = negative_polarity_sum / negative_polarity_num
    array = [[positive_polarity_avg, negative_polarity_avg, positive_polarity_num, negative_polarity_num, neutral_polarity_num, polarity_avg, subjectivity_avg, num_of_rows]]

    df_avg = pd.DataFrame(data=np.array(array), columns=['positive pol avg', 'negative pol avg', 'num of positive polarity', 'num of negative polarity','num of neutral polarity','polarity_avg', 'subjectivity_avg', 'num_of_rows'])
    df_avg.to_csv(path+'Results/Sentiment_Average/'+file_name)


for file in files:
    calc(name + file + '.csv')
