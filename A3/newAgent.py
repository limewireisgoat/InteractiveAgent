import setup as s
from setup import numpy as np
from setup import tflearn as tfl
from setup import tensorflow as tf
from setup import pickle as p
from setup import Pattern as pat

#get the STEMMED synonyms of a word and store them in an array
def getSynonyms(word):
    synonyms = []                                                                                       #create an array to hold the synonyms

    for syn in wn.synsets(word):                                                                        #get all the synonym sets of a word
        for l in syn.lemmas():                                                                          #get the lemmas of every synonym set
            synonyms.append(l.name())                                                                   #append the lemma to the synonym array
    
    synonyms = [stemmer.stem(syn.lower()) for syn in synonyms]                                          #normalize them

    return synonyms

#tokenize and clean a string. Lower case it, remove punctuation, remove non-alphanumeric tokens, and remove stop-words
def cleanWord(word):
    word = word.lower()                                                                                 #lowercase word
    word = word.translate(punc_table)                                                                   #remove punctuation
    word = stemmer.stem(word)                                                                           #stem the word

    return word

def cleanPOSList(string):
    tokenized_words = nltk.word_tokenize(string)                                                        #tokenize the string
    poslist = nltk.pos_tag(tokenized_words)                                                             #get the parts of speech of the pattern
    cleanPOS = []
    for i,tup in enumerate(poslist):
        l = list(tup)
        word = l[0]
        word = cleanWord(word)                                                                          #clean the word from punctuation, make it lower case, and stem it
        if (word not in stop_words and word.isalpha()):                                                  #if it is not a stop word and is alphanumeric, only then use it
            l[0] = word
            tup = tuple(l)
            cleanPOS.append(tup)

    return pos_tokenized_words

#method that reads the new data and stores it in our new variables
def readNewData():

    readData()
    cleanData
    prepareTrainingData()
    
    with open("data.pickle", "wb") as f:
        p.dump((s.dictionary, s.labels, s.training, s.output), f)

#function to read the intents.json file and store its elements into appropriate dictionaries 
def readData():

    for intent in s.data["intents"]:

        #hold the intent tag
        index = intent["tag"]

        for pattern in intent["patterns"]:
            
            pos_stemmed_words = cleanPOSList(pattern)                                                   #make and clean the pos list for this pattern
            dictionary.extend(pos_stemmed_words)                                                        #extend our dictionary with our stemmed words and their pos
            patterns.append(Pattern(pos_stemmed_words, index))                                          #append our list of patterns with this pattern object

        if intent["tag"] not in labels:                                                                 #if we have not studied this tag, add it to our list
            labels.append(intent["tag"])
    
    return dictionary, labels, patterns
       
#function to clean the data
def cleanData():
    s.dictionary = sorted(list(set(s.dictionary)))
    s.labels = sorted(s.labels)
    
    
#function to create the data that the neural network can use
def prepareTrainingData():
    training = []
    output = []
    
    out_empty = [0 for _ in range(len(s.labels))]

    for Pattern in s.patterns:
        bag = []

        pattern_pos_words = pat.pattern

        for dic_tup in s.dictionary:
            if dic_tup in pattern_pos_words:
                bag.apped(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[s.labels.index(Pattern.tag)] = 1

        training.append(bag)
        output.append(output_row)

    s.training = np.array(training)
    s.output = np.array(output)

#method to create a new model
def createNewModel():
    
    tf.reset_default_graph()


    net = tfl.input_data(shape=[None, len(s.dictionary)])
    net = tfl.fully_connected(net, 8)
    net = tfl.fully_connected(net, 8)
    net = tfl.fully_connected(net, len(s.labels), activation='softmax')
    net = tfl.regression(net)

    s.model = tfl.DNN(net)
    s.model.fit(s.training, s.output, n_epoch=1000, batch_size=8, show_metric=True)
    s.model.save("model.tflearn")

def create():
    
    readNewData()
    createNewModel()