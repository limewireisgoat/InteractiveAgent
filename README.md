# Mahmoud the Interactive Conversational Agent

## Purpose
Mahmoud is your friend who, conveniently, can hold a conversation of at least 30 turns. 

## Class Organization
### Folder breakdown: 

Files are divided into 2 folders: build and data 

build folder: This folder contains all of the code needed to build and run the agent.  
data folder: This folder contains the data that the agent is trained on. 

We decided to split the structure in this format for 2 main reasons:  
1) To separate the data from the code. If more code is needed, then we only need to modify the contents of build, and likewise with data.  
2) data contains the information that the agent is trained on, which means that if you change the data, you create a new agent. It is much cleaner to have both of these aspects separate in this way.  

### Class breakdown: 
build/project.py: The main method of the project.  

build/admin.py: This code asks the administrator (The person running the code) if they would like to build a new agent or use existing agent that has been previously generated. It also asks the administrator if they would like to see a conversation between Mahmoud and , another chatbot that has been created by another group in the COSC 310 class.  

build/agent.py: This code uses the agent that was created to have a conversation with the user/x.  

build/config.py: This file contains the necessary configuration elements to link the files. It contains all the global variables that are modified or used frequently throughout the execution of the program.  

build/data.py: This file contains the methods that can read new data from the intents.json file or load existing data that has been saved in "data.pickle".  

build/model: This file contains methods that can create a new agent or load an existing agent from "model.tflearn".  

build/neuralnet.py: Code that contains a method to initialize a neural net using input and output arrays to determine the number of neurons on either side.  

build/pattern.py: A simple class that models a response that is read as training data into the agent.  

build/pos.py: code that generates the filtered and stemmed parts of speech of a string.  

build/synonyms: code that generates the stemmed synonyms of a word.  

data/intents.json: This is a file that holds all of the data that the agent is trained on and the data that is used for responses.  
  

## How to Compile the code
To generate this interactive agent, make sure that you have Python 3.6.x installed (Any Python 3.6 version). No other Python version will allow you to compile the code because the libraries used in this project only work with Python 3.6.  

You will then need to install the required libraries for this project. These are the libraries that you will need:  
1) tensorflow  
2) tflearn  
3) nltk  
4) json  
5) string  
6) numpy  
7) random  
8) pickle  

Ensure that you have all of these libraries installed first. If you do not have any of the libraies mentioned above, make sure to use this instruction to install the library:  
  
   pip install <package_name>

You may also be ased to install wordnet as well. For this issue, run Python and type the following instructions:  
1) import nltk  
2) nltk.download('wordnet') or just nltk.download()  

Everything should workout from here.  

## How to Run the code

Run the project.py file and enjoy your chatbot!


## Built With
Python - Programming language  
JSON - File Format  
