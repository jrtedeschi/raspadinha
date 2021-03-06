import pandas as pd
import numpy as np
import re
import time
import bs4 as bs4 
import requests as rq
import pprint
from pymongo import MongoClient
import json
import tqdm

time1 = time.time()

client = MongoClient("mongodb+srv://jrtedeschi:anaclaravpa10!@cluster0-ndlxt.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.scraper


colunas_selecionadas = ['watch-title', 'watch-view-count', 'watch-time-text', 'content_watch-info-tag-list', 'watch7-headline',
                    'watch7-user-header', 'watch8-sentiment-actions', "og:image", 'og:image:width', 'og:image:height',
                    "og:description", "og:video:width", 'og:video:height', "og:video:tag", 'channel_link_0']

query = { _ : 1 for _ in colunas_selecionadas }

videos_info = db.videos_info 

df = pd.DataFrame(list(videos_info.find()))

base = df[colunas_selecionadas]

base.to_csv('C:/Users/joaor/Documents/Projetos/data/raspadinha/videos_to_label.csv', 
                                        sep=";",
                                        encoding= "utf-8-sig"
                                        )

time2 = time.time() - time1
print("Feito em: {} minutos".format(np.round(time2/60, decimals=2)))