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

importlib.import_module(Pattern)
newData = True                                              #boolean to allow us to load/create models

dictionary = []                                             #array that holds all the words in the JSON file
labels = []                                                 #array that holds all of our tags
patterns = []                                               #array to hold the pattern objects
training = []                                               #training data for neural network
output = []                                                 #output data of neural network

def useExistingData():
    with open("data.pickle", "rb") as f:
        dictionary, labels, training, output = pickle.load(f)

def readNewData():
    with open("intents.json") as file:
        data = json.load(file)

    readData()
    cleanData()
    prepareTrainingData()

    with open("data.pickle", "wb") as f:
        pickle.dump((dictionary, labels, training, output), f)
    
    #function to read the intents.json file and store its elements into appropriate dictionaries
    def readData():
    for intent in data["intents"]:
        
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


def loadExistingModel():
    model.load('model.tflearn')

def createNewModel():
    tensorflow.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(dictionary)])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(patterns), activation='softmax')
    net = tflearn.regression(net)

    model = tflearn.DNN(net)

    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def bag_of_dictionary(s, dictionary):
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
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_dictionary(inp, dictionary)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        print(random.choice(responses))

#main method
def main():
    if newData:
        loadNewData()
        createNewModel()
    else:
        loadExistingData()
        loadExistingModel()
    
    chat()
    print("Goodbye!!!")

if __name__ == '__main__':
    main()
