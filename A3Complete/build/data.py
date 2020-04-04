import json
import pickle
import numpy
import config

from pos import getPOSList
from Pattern import Pattern as pat

#method that reads the new data and stores it in our new variables
def read():    
    dictionary, labels, patterns = readData()
    training, output = train(dictionary, labels, patterns)
    
    with open("data.pickle", "wb") as f:
        pickle.dump((dictionary, labels, training, output), f)
    
    config.dictionary, config.labels, config.patterns, config.training, config.output = dictionary, labels, patterns, training, output

#function to read the intents.json file and store its elements into appropriate dictionaries 
def readData():
    dictionary = []
    labels = []
    patterns = []
    for intent in config.information["intents"]:

        #hold the intent tag
        index = intent["tag"]

        for pattern in intent["patterns"]:
            
            pos_stemmed_words = getPOSList(pattern)                                                 #make and clean the pos list for this pattern
            dictionary.extend(pos_stemmed_words)                                                    #extend our dictionary with our stemmed words and their pos
            patterns.append(pat(pos_stemmed_words, index))                                          #append our list of patterns with this pattern object

        if intent["tag"] not in labels:                                                             #if we have not studied this tag, add it to our list
            labels.append(intent["tag"])
        
        dictionary = sorted(list(set(dictionary)))                                                  #sort the data
        labels = sorted(labels)

    return dictionary, labels, patterns
    
#function to create the data that the neural network can understand
def train(dictionary, labels, patterns):
    training = []
    output = []
    
    out_empty = [0 for _ in range(len(labels))]

    for pattern_object in patterns:
        bag = []

        pattern_pos_words = pattern_object.pattern

        for dic_tup in dictionary:
            if dic_tup in pattern_pos_words:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(pattern_object.tag)] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)
    
    return training, output

def load():

    with open("data.pickle", "rb") as f:
        dictionary, labels, training, output = pickle.load(f)
    
    config.dictionary, config.labels, config.training, config.output = dictionary, labels, training, output
