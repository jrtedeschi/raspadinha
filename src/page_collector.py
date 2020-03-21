import pandas as pd
import numpy as np
import re
import time
import bs4 as bs4 
import requests as rq
import io

queries = ["pydata"]
url = "https://www.youtube.com/results?search_query={query}&sp=CAI%253D&p={page}"

for query in queries:
    for page in range(1,100):
        urll = url.format(query=query, page=page)
        print(urll)
        response = rq.get(urll)

        with io.open("./data/{}_{}.html".format(query,page), "w",encoding="utf-8") as output:
            output.write(response.text)
        time.sleep(1)