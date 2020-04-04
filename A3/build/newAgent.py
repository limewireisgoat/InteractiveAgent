from setup import *
from pos import *

#method that reads the new data and stores it in our new variables
def readNewData():
    readData()
    cleanData
    prepareTrainingData()
    
    with open("data.pickle", "wb") as f:
        pickle.dump((dictionary, labels, training, output), f)

#function to read the intents.json file and store its elements into appropriate dictionaries 
def readData():
    global dictionary, labels, patterns
    for intent in data["intents"]:

        #hold the intent tag
        index = intent["tag"]

        for pattern in intent["patterns"]:
            
            pos_stemmed_words = getPOSList(pattern)                                                   #make and clean the pos list for this pattern
            dictionary.extend(pos_stemmed_words)                                                      #extend our dictionary with our stemmed words and their pos
            patterns.append(Pattern(pos_stemmed_words, index))                                        #append our list of patterns with this pattern object

        if intent["tag"] not in labels:                                                                 #if we have not studied this tag, add it to our list
            labels.append(intent["tag"])
       
#function to clean the data
def cleanData():
    global dictionary, labels
    dictionary = sorted(list(set(dictionary)))
    labels = sorted(labels)
    
    
#function to create the data that the neural network can use
def prepareTrainingData():
    global training, output
    
    out_empty = [0 for _ in range(len(labels))]

    for Pattern in patterns:
        bag = []

        pattern_pos_words = Pattern.pattern

        for dic_tup in dictionary:
            if dic_tup in pattern_pos_words:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(Pattern.tag)] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

#method to create a new model
def createNewModel():
    global model
    tensorflow.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(dictionary)])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(labels), activation='softmax')
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def create(): 
    readNewData()
    createNewModel()