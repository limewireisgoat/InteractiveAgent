from config import punc_table, stemmer, nltk, stop_words

#tokenize and clean a string. Lower case it, remove punctuation, remove non-alphanumeric tokens, and remove stop-words
def cleanWord(word):
    word = word.lower()                                                                                 #lowercase word
    word = word.translate(punc_table)                                                                   #remove punctuation
    word = stemmer.stem(word)                                                                           #stem the word

    return word

#function that gets the stemmed and pos tag for every word in a string
def getPOSList(tokenized_words):
    poslist = nltk.pos_tag(tokenized_words)                                                             #get the parts of speech of the pattern
    cleanPOSlist = []
    for tup in poslist:
        l = list(tup)
        word = l[0]
        cleanword = cleanWord(word)                                                                          #clean the word from punctuation, make it lower case, and stem it
        if (cleanword not in stop_words and word.isalpha()):                                                 #if it is not a stop word and is alphanumeric, only then use it
            l[0] = cleanword
            tup = tuple(l)
            cleanPOSlist.append(tup)
        else:
            tokenized_words.remove(word)
        if cleanword == '':
            tokenized_words.remove(word)
    
    return tokenized_words, cleanPOSlist