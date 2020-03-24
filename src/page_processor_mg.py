import pandas as pd
import numpy as np
import re
import time
import bs4 as bs4 
import requests as rq
import io
import json
import pprint
from pymongo import MongoClient

client = MongoClient("mongodb+srv://jrtedeschi:anaclaravpa10!@cluster0-ndlxt.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.scraper
db.drop_collection(name_or_collection= "videos")

path_pages = "C:/Users/joaor/Documents/Projetos/data/raspadinha/pages/"

queries = ["pydata","NLP","machine+learning","docker","scrapy","mongodb","markov","active+learning","jenkins","tensorflow","kubernetes"]

i = 0
for query in queries:
    for page in range(1,10):
        with io.open(path_pages+"{}_{}.html".format(query,page), "r", encoding= "utf-8") as inp:
            page_html = inp.read()

            parsed = bs4.BeautifulSoup(page_html)

            tags = parsed.findAll("a")

            for e in tags:
                if e.has_attr("aria-describedby"):
                    link = e['href']
                    title = e['title']
                    data = {"link": link, "title": title, "query": query}
                    result = db.videos.insert_one(data)
                    print('Created doc {0} as {1}'.format(i,result.inserted_id))
                    i += 1

print('finished creating {0} documents'.format(i))

pprint.pprint(db.videos.find_one())



