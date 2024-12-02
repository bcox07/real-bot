# This program takes user input and matches it to a list of terms used in CS2 maps and strategies
# NOTE: in order for the user input for 'A' and 'B' to be recognized as 'a-site' and 'b-site', the user must input 'A' and 'B' in uppercase

import nltk 
from nltk.metrics.distance import edit_distance

# set a threshold for edit distance to correct misspellings
threshold = 2

# list of common terms used in CS2 maps and strategies
terms = ['mirage', 'anubis', 'ancient', 'vertigo', 'dust 2', 'inferno', 'nuke', 'overpass',
         'train' , 'smoke' , 'flash' , 'molotov' , 'lineup' , 'execute' , 'default' , 'middle',
         'b-site', 'a-site', 'catwalk', 'long', 'short', 'tunnel', 'window', 'door', 'connector', 'ramp',
         'stairs', 'banana', 'apartments', 'pit', 'truck', 'car', 'barrels', 'boost',
         'heaven', 'hell', 'sandwich', 'underpass', 'palace', 'tetris', 'jungle', 
         'firebox', 'bench', 'market', 'balcony', 'dark', 'chair'
         ]

# common slang terms/shortentings used in cs2
slang={'apps': 'apartments', 'mid': 'middle', 'B': 'b-site', 'A': 'a-site',
       'cat': 'catwalk', 'ct': 'counter-terrorist', 't': 'terrorist', 'conn': 'connector',
       'exec': 'execute', 'molly': 'molotov'
       }

# example user input of terms, slang, terms, etc
user_input= "i a need molly lineup exec for A long on dust"

# split the user input into individual words
user_words = user_input.split()

# loop to match user input to cs2 maps/terms, even if it's misspelled
for word in user_words:
    # Check if the word is in the slang dictionary
    if word in slang:
        word = slang[word]
    temp = [(edit_distance(word, w), w) for w in terms if w[0] == word[0]]
    # Filter out words that are not close matches
    close_matches = [w for d, w in temp if d <= threshold]
    if close_matches:
        print(sorted(close_matches, key=lambda w: edit_distance(word, w))[0])


# Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.