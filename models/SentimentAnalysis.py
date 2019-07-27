from textblob import TextBlob
import numpy as np
import pandas as pd

# ==================================================================================================================

datasets_path = '../data-sets/'
no_stop_words_prefix = 'clean_no_stop_words_'
clean_prefix = 'clean_'

games_df = {
    'fortnite': pd.read_csv(datasets_path + clean_prefix + 'fortnite.csv'),
    'pubg': pd.read_csv(datasets_path + clean_prefix + 'pubg.csv'),
    'fifa': pd.read_csv(datasets_path + clean_prefix + 'fifa.csv'),
    'minecraft': pd.read_csv(datasets_path + clean_prefix + 'minecraft.csv'),
    'bloodstained': pd.read_csv(datasets_path + clean_prefix + 'bloodstained.csv'),
    'lol': pd.read_csv(datasets_path + clean_prefix + 'lol.csv'),
    'overwatch': pd.read_csv(datasets_path + clean_prefix + 'overwatch.csv'),
    'sims': pd.read_csv(datasets_path + clean_prefix + 'sims.csv'),
    'wow': pd.read_csv(datasets_path + clean_prefix + 'wow.csv'),
    'dota2': pd.read_csv(datasets_path + clean_prefix + 'dota2.csv'),
}


# ==================================================================================================================


def perform_sentiment_analysis(game_name, _game_df, _results_df):
    polarity_sum = 0
    subjectivity_sum = 0
    positive_polarity_sum = 0
    negative_polarity_sum = 0
    num_pos_pol = 0
    num_neg_pol = 0
    num_neu_pol = 0

    for row in _game_df.values:
        if type(row[0]) is str:
            testimonial = TextBlob(row[0])
            polarity_sum += testimonial.sentiment.polarity
            subjectivity_sum += testimonial.sentiment.subjectivity
            # results.append([twite[0], testimonial.sentiment.polarity, testimonial.sentiment.subjectivity])
            # case polarity is positive
            if testimonial.sentiment.polarity > 0:
                positive_polarity_sum += testimonial.sentiment.polarity
                num_pos_pol += 1
            # case polarity is negative
            elif testimonial.sentiment.polarity < 0:
                negative_polarity_sum += testimonial.sentiment.polarity
                num_neg_pol += 1
            else:
                num_neu_pol += 1

    # average
    num_of_rows = num_pos_pol + num_neg_pol + num_neu_pol

    polarity_avg = polarity_sum / num_of_rows
    subjectivity_avg = subjectivity_sum / num_of_rows
    positive_polarity_avg = positive_polarity_sum / num_pos_pol
    negative_polarity_avg = negative_polarity_sum / num_neg_pol

    _results_df = _results_df.append({'game_name': game_name, 'num_pos_pol': num_pos_pol, 'num_neg_pol': num_neg_pol,
                                      'num_neu_pol': num_neu_pol, 'avg_positive_pol': positive_polarity_avg,
                                      'avg_neg_pol': negative_polarity_avg, 'polarity_avg': polarity_avg,
                                      'subjectivity_avg': subjectivity_avg, 'num_of_rows': num_of_rows},
                                     ignore_index=True)

    print({'game_name': game_name, 'num_pos_pol': num_pos_pol, 'num_neg_pol': num_neg_pol,
           'num_neu_pol': num_neu_pol, 'avg_positive_pol': positive_polarity_avg,
           'avg_neg_pol': negative_polarity_avg, 'polarity_avg': polarity_avg,
           'subjectivity_avg': subjectivity_avg, 'num_of_rows': num_of_rows})
    return _results_df


def main():
    results_df = pd.DataFrame(columns=['game_name', 'num_pos_pol', 'num_neg_pol', 'num_neu_pol'
                                        'avg_positive_pol', 'avg_neg_pol',
                                       'polarity_avg', 'subjectivity_avg', 'num_of_rows'])
    for game_name, game_df in games_df.items():
        results_df = perform_sentiment_analysis(game_name, game_df, results_df)
    results_df.to_csv(datasets_path + 'games_sentiment_analysis.csv', index=False)


if __name__ == '__main__':
    main()
