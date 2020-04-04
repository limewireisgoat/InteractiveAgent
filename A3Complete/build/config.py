from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import nltk
import json
import string
import neuralnet
from nltk.corpus import stopwords as sw

#define the list of stopwords
stop_words = set(sw.words('english'))

#define a punctuation table
punc_table = str.maketrans('','', string.punctuation)

dictionary = []                                                                                         #array that holds all the words in the JSON file
labels = []                                                                                             #array that holds all of our tags
patterns = []                                                                                           #array to hold the pattern objects
training = []                                                                                           #training data for neural network
output = []                                                                                             #output data of neural network
agent = []

with open("C:/Users/sabry/Documents/310/Project/updateA3/data/intents.json") as file:                   #open the JSON file and load the data into "data"
    information = json.load(file)

def createModel():
    global agent
    agent = neuralnet.initialize(dictionary, labels)