import pandas as pd

df = pd.read_csv("audio/metadata.csv", usecols=[3])
df.drop_duplicates(subset=None, inplace=True)

df.to_csv("audio/new_metadata.csv", index=False)