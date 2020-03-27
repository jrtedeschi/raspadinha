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
clean_date[0] = clean_date[0].map(lambda x: "0"+str(x[0]) if len(str(x)) == 1 else str(x))
#clean_date[1] = clean_date[1].map(lambda x: x[0].upper()+x[1:])
clean_date[2] = clean_date[2].astype('str')


mapa_meses = {"jan": "Jan",
              "fev": "Feb",
              "mar": "Mar", 
              "abr": "Apr", 
              "mai": "May", 
              "jun": "Jun",
              "jul": "Jul",
              "ago": "Aug", 
              "set": "Sep", 
              "out": "Oct", 
              "nov": "Nov",
              "dez": "Dec"}

clean_date[1] = clean_date[1].map(mapa_meses)
clean_date = clean_date.dropna()




clean_date = clean_date.apply(lambda x: " ".join(x.dropna()), axis=1)

print("xura",clean_date)

df_limpo['date'] = pd.to_datetime(clean_date.dropna(), format="%d %b %Y")

views = df['watch-view-count'].str.extract(r"(\d+\.?\d*)", expand=False).str.replace(".", "").fillna(0).astype(int)
df_limpo['views'] = views

features = pd.DataFrame(index=df_limpo.index)
y = df['Y'].copy()

features['tempo_desde_pub'] = (pd.to_datetime("2019-12-03") - df_limpo['date']) / np.timedelta64(1, 'D')
features['views'] = df_limpo['views']
features['views_por_dia'] = features['views'] / features['tempo_desde_pub']
features = features.drop(['tempo_desde_pub'], axis=1)

print(features)