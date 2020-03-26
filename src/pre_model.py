import pandas as pd
import numpy as np
import re
import time
import bs4 as bs4


#​pd.set_option('max.columns', 131)

path = 'C:/Users/joaor/Documents/Projetos/data/raspadinha/videos_labeled.csv'

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


df = pd.read_csv('C:/Users/joaor/Documents/Projetos/data/raspadinha/videos_labeled.csv', index_col=0, sep=';')
df = df[df['Y'].notnull()]

print(df.shape)

df_limpo = pd.DataFrame(index=df.index)

clean_date = df['watch-time-text'].str.extract(r"(\d+) de ([a-z]+)\. de (\d+)")
clean_date[0] = clean_date[0].map(lambda x: "0"+x[0] if len(x) == 1 else x)
#clean_date[1] = clean_date[1].map(lambda x: x[0].upper()+x[1:])

mapa_meses = {"jan": "Jan",
              "fev": "Feb",
              "mar": "Mar", 
              "abr": "Apr", 
              "mai": "May", 
              "jun": "Jun",
              "jul": "Jul",
              "ago": "Aug", 
              "set": "Sep", 
              "nov": "Nov",
              "out": "Oct", 
              "dez": "Dec"}

clean_date[1] = clean_date[1].map(mapa_meses)

clean_date = clean_date.apply(lambda x: " ".join(x), axis=1)

df_limpo['date'] = pd.to_datetime(clean_date, format="%d %b %Y")

views = df['watch-view-count'].str.extract(r"(\d+\.?\d*)", expand=False).str.replace(".", "").fillna(0).astype(int)
df_limpo['views'] = views
