import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw

import importlib
import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import string

#define the list of stopwords
stop_words = set(sw.words('english'))

#define a punctuation table
punc_table = str.maketrans('','',string.punctuation)

#A Pattern class
class Pattern:
    def __init__(self, pattern, tag):
        self.pattern = pattern
        self.tag = tag


dictionary = []                                                                                         #array that holds all the words in the JSON file
labels = []                                                                                             #array that holds all of our tags
patterns = []                                                                                           #array to hold the pattern objects
training = []                                                                                           #training data for neural network
output = []                                                                                             #output data of neural network
model = 1

with open("intents.json") as file:                                                                      #open the JSON file and load the data into "data"
    data = json.load(file)

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

    return twClean

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

#load the existing data into the workspace instead of training the model all over again
def loadExistingData():
    global dictionary
    global labels
    global training
    global output
    with open("data.pickle", "rb") as f:                                                                #load the data back into the variables
        dictionary, labels, training, output = pickle.load(f)

#read the new data inside the modified json file
def readNewData():
    global dictionary
    global labels
    global patterns
    global training
    global output
    
    dictionary, labels, patterns = readData()
    dictionary, labels = cleanData(dictionary, labels)
    training, output = prepareTrainingData()
    
    with open("data.pickle", "wb") as f:
        pickle.dump((dictionary, labels, training, output), f)

#function to read the intents.json file and store its elements into appropriate dictionaries 
def readData():
    global data

    for intent in data["intents"]:

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
def cleanData(dictionary, labels):
    dictionary = sorted(list(set(dictionary)))
    labels = sorted(labels)
    return dictionary, labels
    
    
#function to create the data that the neural network can use
def prepareTrainingData():
    training = []
    output = []
    
    out_empty = [0 for _ in range(len(labels))]

    for Pattern in patterns:
        bag = []

        pattern_pos_words = Pattern.pattern

        for dic_tup in dictionary:
            if dic_tup in pattern_pos_words:
                bag.apped(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(Pattern.tag)] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)
    
    return training, output    

#method to load the existing model
def loadExistingModel():
    global model
    model = model.load('model.tflearn')


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


#method to fit the user's input into a format that the neural network can understand
def fitInput(userString):
    bag = [0 for _ in range(len(dictionary))]                                                           #create a bag of 0s that is the size of the neural network's input 

    user_dictionary = cleanPOSList(userString)                                                          #make a stemmed pos list from the user's input

    #loop over all our words
    for i, word in enumerate(dictionary):                                                               #traverse through our dictionary of words
        if (len(user_dictionary) == 0 ):                                                                #if there are no more words left to study, end
            break

        else:
            for j, se in enumerate(user_dictionary):                                                    #look through every word in the list of words that the user provided
                if word == se:                                                                          #if the word that the user provides is in our dictionary,
                    bag[i] = 1                                                                          #then put 1 to show that the word is present
                    user_dictionary.pop(j)                                                              #no need to check for this word ever again
                    break                                                                               #no need to check for the other words

    #account for synonyms now
    for i, word in enumerate(dictionary):
        if (len(user_dictionary) == 0 ):                                                                #if there are no more words left to study, end
            break
        
        elif bag[i] == 1:                                                                               #if a word has been accounted for, skip it
            continue

        else:
            for j, se in enumerate(user_dictionary):                                                    #account for synonyms
                synonyms = getSynonyms(se)
                for synm in synonyms:
                    if synm == word
                        bag[i] = 1
                        user_dictionary.pop(j)
                        break
                if bag[i] == 1:
                    break
            
    return numpy.array(bag)


#get the reponse
def getResponse(results):
    if max(results) < 0.70:                                                                             #if the maximum probability that a tag has is 70%, we will asusme that the user entered something that is off-topic
        result_tag = 'irrelevant'
        
    else:
        results_index = numpy.argmax(results)                                                           #index the tag with the highest probability
        result_tag = labels[results_index]                                                              #return that tag
    
    return result_tag


#chatting method
def chat():
    print("Start talking with the bot (type goodbye to stop)!")
    while True:
        user = input("You: ")

        results = model.predict([fitInput(user)])                                                       #fit the user input into the format that the model can read and predict the result
        result_tag = getResponse(results)                                                               #get the response tag that the model predicts
        
        #find the intent with the specified tag and get the responses
        for intent in data["intents"]:
            if intent['tag'] == result_tag:
                responses = intent['responses']

        print("Mahmoud: " + random.choice(responses))

        if result_tag == "goodbye":
            break


#method to know if you want to make changes
def InputAndModel():
    newData = False                                                                                     #boolean to allow us to use new /load old data
    newModel = True                                                                                     #boolean to allow to create new/ use existing models
    print("Input new data?")
    haveNewData = input()

    if haveNewData == 'yes':
        newData = True

    if newData:        
        readNewData()
        createNewModel()
    else:
        print("Make new Model?")
        wantNewModel = input()

        if wantNewModel == 'no':
            newModel = False
        
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
