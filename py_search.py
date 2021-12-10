import pandas as pd

'''
File to create a search engine entirely using the Python command line.
'''

# Read in the inverse frequency table -- this will be queried when
# the user searches for a word.
data = pd.read_csv("inv_freq2.csv", delimiter="~")
data.columns = ['word', 'links']

# Read in the data associated with each link from the data scraped
# by the spider. This is used to print out this associated data to
# the command line following a query.
data2 = pd.read_csv("nspiderdata.csv", delimiter="~")
data2.columns = ['title', 'link', 'desc']

flag = True

# Continue while the user wants to keep searching.
while flag:
    word = input("What are you looking for?" + "\n").lower()

    # Create a subset of the data that is only containing the word that is queried.
    searched = data.loc[data.word == word]
    searched = searched.dropna()

    # If the word doesn't exist, show nothing.
    if len(searched) == 0:
        print("No results")
        
        # See if the user would like to continue searching.
        resp = input("Would you like to search again? (y/n)").lower()
        if resp == 'y' or resp == 'yes':
            continue
        else:
            flag = False
    else:
        # Get the first 10 links and their corresponding data from the dataset.
        links = searched.links.astype(str).apply(eval).values[0]
        if len(links) > 10:
            links = links[:10]
        links = [x[0] for x in links]
        
        # Print out the information from each link to the command line.
        for link in links:
            print(link)
            print(data2.loc[data2['link'] == link, 'title'].iloc[0])
            print(str(data2.loc[data2['link'] == link, 'desc'].iloc[0][:100]) + "\n")
            
        # See if the user would like to continue searching.
        resp = input("Would you like to search again? (y/n)").lower()
        if resp == 'y' or resp == 'yes':
            continue
        else:
            flag = False
