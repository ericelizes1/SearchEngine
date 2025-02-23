import pandas as pd
from collections import Counter
import re
import numpy as np

'''
File to create a frequency table data structure from the resultant
dataframe from myspider.py.
'''

# Read the data file produced by myspider.py
data = pd.read_csv("data.csv", delimiter="~")

new_data = pd.DataFrame(columns=['Title', 'Link', 'Dict'])

# Use regex to split the website description up by word and make a dictionary from it. If the word appears
# multiple times, increase its value by 1 for each repeat.
for i in range(0, len(data)):
    holder = dict(Counter(list(filter(None, re.split(r"[ 1234567890,.!?|<>~`@#$%^&*()_+={}:;\\\"\'\[\]/]", str(data.Desc.iloc[i]).lower())))))
    new_data.loc[len(new_data)] = [data.Title.iloc[i], data.Link.iloc[i], holder]

# Save this data to csv
np.savetxt("new_data.csv", new_data, delimiter="~", fmt="%s", encoding="utf-8")
