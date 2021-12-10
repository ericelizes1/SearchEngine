import pandas as pd
from ast import literal_eval

data = pd.read_csv("inv_freq2.csv", delimiter="~")
data.columns = ['word', 'links']

data2 = pd.read_csv("nspiderdata.csv", delimiter="~")
data2.columns = ['title', 'link', 'desc']

word = input("What are you looking for?" + "\n").lower()

searched = data.loc[data.word == word]
searched = searched.dropna()

if len(searched) == 0:
    print("No results")
else:
    links = searched.links.astype(str).apply(eval).values[0]
    if len(links) > 10:
        links = links[:10]
    links = [x[0] for x in links]
    for link in links:
        print(link)
        print(data2.loc[data2['link'] == link, 'title'].iloc[0])
        print(str(data2.loc[data2['link'] == link, 'desc'].iloc[0][:100]) + "\n")
