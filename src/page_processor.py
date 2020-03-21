import pandas as pd
import numpy as np
import re
import time
import bs4 as bs4 
import requests as rq
import io
import json

queries = ["pydata"]

for query in queries:
    for page in range(1,27):
        with io.open("./data/{}_{}.html".format(query,page), "r", encoding= "utf-8") as inp:
            page_html = inp.read()

            parsed = bs4.BeautifulSoup(page_html)

            tags = parsed.findAll("a")

            for e in tags:
                if e.has_attr("aria-describedby"):
                    link = e['href']
                    title = e['title']
                    with io.open("parsed_videos.json","a+",encoding= "utf-8") as output:
                        data = {"link": link, "title": title, "query": query}
                        output.write("{}\n".format(json.dumps(data,ensure_ascii=False)))

df = pd.read_json("parsed_videos.json", lines= True, encoding= "utf-8")

print(df.head())