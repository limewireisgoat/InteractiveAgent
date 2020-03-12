import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import importlib
import numpy
import tflearn
import tensorflow
import random
import json
import pickle

class Pattern:
    def __init__(self, pattern, tag):
        self.pattern = pattern
        self.tag = tag

#importlib.import_module(Pattern)                            #imports Pattern.py



dictionary = []                                             #array that holds all the words in the JSON file
labels = []                                                 #array that holds all of our tags
patterns = []                                               #array to hold the pattern objects
training = []                                               #training data for neural network
output = []                                                 #output data of neural network

def loadExistingData():
    with open("data.pickle", "rb") as f:
        dictionary, labels, training, output = pickle.load(f)

def readNewData():
    with open("intentscopy.json") as file:
        data = json.load(file)

    readData()
    cleanData()
    prepareTrainingData()

    with open("data.pickle", "wb") as f:
        pickle.dump((dictionary, labels, training, output), f)
    
    #function to read the intents.json file and store its elements into appropriate dictionaries
    def readData():
        for intent in data["intents"]:
        
            #hold the intent tag
            index = intent["tag"]

            for pattern in intent["patterns"]:
                tokenized_words = nltk.word_tokenize(pattern)
                tokenized_words = [stemmer.stem(word.lower()) for word in tokenized_words if word != "?"]
                dictionary.extend(tokenized_words)
                patterns.append(Pattern(tokenized_words, index))

            if intent["tag"] not in labels:
                labels.append(intent["tag"])
    
    #function to clean the data
    def cleanData():
        dictionary = sorted(list(set(dictionary)))
        labels = sorted(labels)
    
    #function to create the data that the neural network can use
    def prepareTrainingData():
        out_empty = [0 for _ in range(len(labels))]

        for Pattern in patterns:
            bag = []

            pattern_words = Pattern.pattern

            for word in dictionary:
                if word in pattern_words:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[labels.index(Pattern.tag)] = 1

            training.append(bag)
            output.append(output_row)

        training = numpy.array(training)
        output = numpy.array(output)

#method to load the existing model
def loadExistingModel():
    model.load('model.tflearn')

#method to create a new model
def createNewModel():
    tensorflow.reset_default_graph()


    net = tflearn.input_data(shape=[None, len(dictionary)])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(patterns), activation='softmax')
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    print('hi')
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    print('hi')
    model.save("model.tflearn")
    print('hi')
#method to get the tag that corresponds to the user input
def fitInput(s):
    bag = [0 for _ in range(len(dictionary))]

    s_dictionary = nltk.word_tokenize(s)
    s_dictionary = [stemmer.stem(word.lower()) for word in s_dictionary]

    for se in s_dictionary:
        for i, word in enumerate(dictionary):
            if word == se:
                bag[i] = 1
            
    return numpy.array(bag)

#chatting method
def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        user = input("You: ")
        if inp.lower() == "quit":
            break

        results = model.predict([fitInput(user)])                #fit the user input into the format that the model can read and predict the result
        results_index = numpy.argmax(results)                   #index the tag with the highest probability
        result_tag = labels[results_index]                      #return that tag

        for intent in data["intents"]:
            if intent['tag'] == result_tag:
                responses = intent['responses']

        print("Mahmoud: " + random.choice(responses))

#        if tag == "Goodbye":
#            break

#method to know if you want to make changes
def InputAndModel():
    newData = True                                              #boolean to allow us to use new /load old data
    newModel = True                                            #boolean to allow to create new/ use existing models
    print("Use existing data?")
    wantNewData = input()

    if wantNewData == 'yes':
        newData = False

    print("Make new Model?")
    wantNewModel = input()

    if wantNewModel == 'no':
        newModel = False

    if newData:        
        loadNewData()
        createNewModel()
    else:
        loadExistingData()
        if newModel:
            createNewModel()
        else:
            loadExistingModel()

#main method
def main():
    InputAndModel()
    chat()

if __name__ == '__main__':
    main()
