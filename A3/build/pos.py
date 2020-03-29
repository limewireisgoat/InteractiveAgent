from setup import *

#tokenize and clean a string. Lower case it, remove punctuation, remove non-alphanumeric tokens, and remove stop-words
def cleanWord(word):
    word = word.lower()                                                                                 #lowercase word
    word = word.translate(punc_table)                                                                   #remove punctuation
    word = stemmer.stem(word)                                                                           #stem the word

    return word

#function that gets the stemmed and pos tag for every word in a string
def getPOSList(string):
    tokenized_words = nltk.word_tokenize(string)                                                        #tokenize the string
    poslist = nltk.pos_tag(tokenized_words)                                                             #get the parts of speech of the pattern
    cleanPOS = []
    for tup in poslist:
        l = list(tup)
        word = l[0]
        word = cleanWord(word)                                                                          #clean the word from punctuation, make it lower case, and stem it
        if (word not in stop_words and word.isalpha()):                                                 #if it is not a stop word and is alphanumeric, only then use it
            l[0] = word
            tup = tuple(l)
            cleanPOS.append(tup)
    return cleanPOS