import pandas as pd
import numpy as np
import re
import time
import bs4 as bs4 
import requests as rq
import io

path_videos = "C:/Users/joaor/Documents/Projetos/data/raspadinha/videos/"

df = pd.read_json(path_videos+"parsed_videos.json", lines= True, encoding= "utf-8")

lista_links = df["link"].unique()

url = "https://www.youtube.com{link}"

for link in lista_links:
    urll = url.format(link= link)
    print(urll)
    response = rq.get(urll)
    nome_link = re.search("v=(.*)",link).group(1)


    with io.open(path_videos+"video_{}.html".format(nome_link), "w",encoding="utf-8") as output:
        output.write(response.text)
    time.sleep(1)