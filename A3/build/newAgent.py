import setup as s
from setup import numpy as np
from setup import tflearn as tfl
from setup import tensorflow as tf
from setup import pickle as p

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
            tokenized_words = s.nltk.word_tokenize(pattern)
            tokenized_words = [s.stemmer.stem(word.lower()) for word in tokenized_words if word != "?"]
            s.dictionary.extend(tokenized_words)
            s.patterns.append(s.Pattern(tokenized_words, index))

        if intent["tag"] not in s.labels:
            s.labels.append(intent["tag"])
       
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

        pattern_words = str(Pattern.pattern)

        for word in s.dictionary:
            if word in pattern_words:
                bag.append(1)
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