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

unique_words = []

# Add all unique words to an array to be used as a column for the output dataset.
for x in range(0, len(data)):
    for y in range(0, len(data['dict'].iloc[x])):
        if list(data['dict'].iloc[x].keys())[y] not in unique_words:
            unique_words.append(list(data['dict'].iloc[x].keys())[y])

output = pd.DataFrame(columns=['word', 'count'])

# For each unique word, search for it in the dictionary of words for each website, and create a dictionary of websites and
# the frequency with which the word appears in each one, if at all.
for x in range(0, len(unique_words)):
    hol_dict = {}
    for y in range(0, len(data)):
        if unique_words[x] in data.dict.iloc[y]:
            hol_dict.update({data.links.iloc[y]: data.dict.iloc[y][unique_words[x]]})
    hol_dict = sorted(hol_dict.items(), key=lambda j: j[1], reverse=True)
    hol_dict = {k: v for k, v in hol_dict}
    output.loc[len(output)] = [unique_words[x], hol_dict]

output.to_csv("output.csv")
