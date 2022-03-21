import pandas as pd
import os

from pyparsing import col

def filter_rows_by_values(df, col, values):
    return df[~df[col].isin(values)]

directory = 'datasets/csv/'

df1 = pd.read_csv(directory + 'xeno-canto_europe.csv', usecols=[1, 4, 6])
df1['file_code'] = 'XC' + df1['file_code'].astype(str) + '.mp3'
df1 = df1.rename(columns={'file_code': 'filename'})

df2 = pd.read_csv(directory + 'train_extended.csv', usecols=[6, 7, 22])
df2 = df2.rename(columns={'species': 'english_name'})

df3 = pd.read_csv(directory + 'metadata.csv', usecols=[0, 4, 6])
df3 = df3.rename(columns={'Recording_ID': 'filename', 'English_name': 'english_name', 'Country': 'country'})
df3 = df3['Recording_ID'] = 'XC' + df3['Recording_ID'].astype(str) + '.mp3'

df = pd.concat([df1, df2, df3], ignore_index=True)
df = filter_rows_by_values(df, 'country', ['Japan', 'El Salvador', 'Guatemala', 'Chile', 'Peru', 'United States', 'Canada', 'Colombia', 'Costa Rica', 'Mexico', 'Honduras', 'Puerto Rico', 'Cuba', 'Panama', 'Ecuador', 'Algeria', 'Argentina', 'Australia', 'Azerbaijan', 'Bahamas', 'Barbados', 'Belize', 'Bhutan', 'Bolivia', 'Brazil', 'Burundi', 'Vietnam', 'Venezuela', 'Uzbekistan', 'Uruguay'])

print(df.head())

df.to_csv(directory + 'train.csv', index=False)
