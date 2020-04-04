import nltk

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()


import numpy
import tensorflow
import tflearn
import random
import json
import pickle

import warnings

class Pattern:
    def __init__(self, pattern, tag):
        self.pattern = pattern
        self.tag = tag

dictionary = []                                             #array that holds all the words in the JSON file
labels = []                                                 #array that holds all of our tags
patterns = []                                               #array to hold the pattern objects
training = []                                               #training data for neural network
output = []                                                 #output data of neural network
model = []

with open("C:/Users/sabry/Documents/310/Project/A3/data/intents.json") as file:
    data = json.load(file)