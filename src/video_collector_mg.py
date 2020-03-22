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


client = MongoClient("mongodb+srv://jrtedeschi:anaclaravpa10!@cluster0-ndlxt.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.scraper

videos = db.videos
db.drop_collection(name_or_collection= "videos_info")

df = pd.DataFrame(list(videos.find()))

url = "https://www.youtube.com{link}"

lista_de_links = df["link"].unique()
i = 0
for link in tqdm.tqdm(lista_de_links, leave=False):
    urll = url.format(link=link)
    print(urll)
    response = rq.get(urll)
    parsed = bs4.BeautifulSoup(response.text, 'html.parser')

    class_watch = parsed.find_all(attrs={"class":re.compile(r"watch")})
    id_watch = parsed.find_all(attrs={"id":re.compile(r"watch")})
    channel = parsed.find_all("a", attrs={"href":re.compile(r"channel")})
    meta = parsed.find_all("meta")

    data = dict()
    for e in class_watch:
        colname = "_".join(e['class'])
        if "clearfix" in colname:
            continue
        data[colname] = e.text.strip()
    for e in id_watch:
        colname = e['id']
        #if colname in output:
        #    print(colname)
        data[colname] = e.text.strip()
    for e in meta:
        colname = e.get('property')
        if colname is not None:
            data[colname] = e['content']
    for link_num, e in enumerate(channel):
        data["channel_link_{}".format(link_num)] = e['href']
        
    result = db.videos_info.insert_one(data)
    i += 1
    print('Created doc {0} as {1}'.format(i,result.inserted_id))

#     db.videos_info.insert_many(data)
print('finished creating {0} documents'.format(i))

pprint.pprint(db.videos_info.find_one().pretty())
# pprint.pprint(db.videos_info.find_one())