
from setup import *

#get the STEMMED synonyms of a word and store them in an array
def getSynonyms(word):
    synonyms = []                                                                                       #create an array to hold the synonyms

    for syn in wn.synsets(word):                                                                        #get all the synonym sets of a word
        for l in syn.lemmas():                                                                          #get the lemmas of every synonym set
            synonyms.append(l.name())                                                                   #append the lemma to the synonym array
    
    synonyms = [stemmer.stem(syn.lower()) for syn in synonyms]                                          #normalize them

    return synonyms