import pandas as pd


df = pd.read_csv('data-sets/clean_pubg.csv')
df1 = pd.read_csv('data-sets/clean_pubg_text.csv')

# df= df.append(df1, ignore_index=False)

df = df.drop_duplicates()
df.to_csv("data-sets/cleaned-data-sets/clean_pubg_no_dupes.csv", index=False)