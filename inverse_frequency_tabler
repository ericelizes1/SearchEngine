import pandas as pd
from ast import literal_eval
import numpy as np
from datetime import datetime

data = pd.read_csv("new_data.csv", delimiter="~")

data.columns = ['title', 'links', 'dict']

data = data.dropna()

list_d = list(data.index.values)
list_d = list_d[:-1]

data.dict = data.dict.apply(literal_eval)

unique_words = []

for x in range(0, len(data)):
    for y in range(0, len(data['dict'].iloc[x])):
        if list(data['dict'].iloc[x].keys())[y] not in unique_words:
            unique_words.append(list(data['dict'].iloc[x].keys())[y])

output = pd.DataFrame(columns=['word', 'count'])

for x in range(0, len(unique_words)):
    hol_dict = {}
    for y in range(0, len(data)):
        if unique_words[x] in data.dict.iloc[y]:
            hol_dict.update({data.links.iloc[y]: data.dict.iloc[y][unique_words[x]]})
    output.loc[len(output)] = [unique_words[x], hol_dict]

output.to_csv("output.csv")
