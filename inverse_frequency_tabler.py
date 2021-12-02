import pandas as pd
from ast import literal_eval
import numpy as np

'''
To Do:
1. Use boolean array to apply operation once instead of for loop?
2. Instead of above, use np.vectorize to remove loops? (Hard to do with nested loops)
3. Use map() instead?
4. Is it faster to make a list of tuples and map these tuples to a dictionary afterwards?
'''

data = pd.read_csv("new_data.csv", delimiter="~", error_bad_lines=False)
data.columns = ['title', 'links', 'dict']
data = data.dropna()

# Make column a dictionary again (pandas does not recognize dictionaries as a type when reading)
data.dict = data.dict.apply(literal_eval)

unique_words = {}

# Create a nested dictionary within unique_word with the key being a word and the value being
# a dictionary of key-value pairs of url-frequency.
for x in range(0, len(data)):
    for y in range(0, len(data['dict'].iloc[x])):
        if list(data['dict'].iloc[x].keys())[y] not in unique_words.keys():
            unique_words.update({list(data['dict'].iloc[x].keys())[y]:
                                     {data['links'].iloc[y]: list(data['dict'].iloc[x].values())[y]}})
        else:
            unique_words[list(data['dict'].iloc[x].keys())[y]].update({data['links'].iloc[y]:
                                                                 list(data['dict'].iloc[x].values())[y]})

for key, value in unique_words.items():
    unique_words.update({key: sorted(value.items(), key=lambda j: j[1], reverse=True)})

ifreq = pd.DataFrame(list(unique_words.items()))
ifreq.columns = ['word', 'dict']
np.savetxt("inv_freq.csv", ifreq, delimiter="~", fmt="%s", encoding="utf-8")
