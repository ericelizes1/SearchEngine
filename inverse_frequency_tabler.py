import pandas as pd
from ast import literal_eval
import numpy as np

# Read the data file produced by frequency_tabler.py
data = pd.read_csv("new_data.csv", delimiter="~", error_bad_lines=False)
data.columns = ['title', 'links', 'dict']

# If a website has no description, remove it, as this is incompatible with our search engine.
data = data.dropna()

# Make column a dictionary again (pandas does not recognize dictionaries as a type when reading)
data.dict = data.dict.apply(literal_eval)

unique_words = {}

# Create a nested dictionary within unique_words with the key being a word and the value being
# a dictionary of key-value pairs of url-frequency.
for x in range(0, len(data)):
    for y in range(0, len(data['dict'].iloc[x])):
        if list(data['dict'].iloc[x].keys())[y] not in unique_words.keys():
            unique_words.update({list(data['dict'].iloc[x].keys())[y]:
                                     {data['links'].iloc[x]: list(data['dict'].iloc[x].values())[y]}})
        else:
            unique_words[list(data['dict'].iloc[x].keys())[y]].update({data['links'].iloc[x]:
                                                                 list(data['dict'].iloc[x].values())[y]})

# Sort the nested dictionaries wihtin unique_words in descending order by count
for key, value in unique_words.items():
    unique_words.update({key: sorted(value.items(), key=lambda j: j[1], reverse=True)})

# Write the dictionary to csv, with the keys all mapping to a column consisting
# of unique words, and the values mapping to another column.
ifreq = pd.DataFrame(list(unique_words.items()))
ifreq.columns = ['word', 'dict']
np.savetxt("inv_freq.csv", ifreq, delimiter="~", fmt="%s", encoding="utf-8")
