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
import warnings

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
model = []                                                                                              #model object that represents our neural network

with open("C:/Users/sabry/Documents/310/Project/updateA3/data/intents.json") as file:                   #open the JSON file and load the data into "data"
    data = json.load(file)