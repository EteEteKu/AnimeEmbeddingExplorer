import pandas as pd


df = pd.read_csv(r'Animedataset\anime.csv')


print(df["Name"][0])
