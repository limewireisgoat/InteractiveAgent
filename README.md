# Mahmoud the Interactive Conversational Agent

## Built by  

Ahmed Sabry  
Camila Jenkins  
Maya Tomoum  

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
  
## Features  

Since the previous iteration, there have been lots of new features that have been implemented. Each features that will be mentioned below will include a rationale as to why it has been chosen and a snippet of the feature in action.  

### Simple Gui  
The user needs a cleaner interface to communicate with the chatbot.  
![gui](https://user-images.githubusercontent.com/52863189/78506820-35ec4180-7731-11ea-97c0-7ec84e20d2bc.png)


### Extra topics  
The interactive agent models a friend. There should be a lot to talk about. More topics have been added to the agent's reportoire as presented in the intents.json file.  
![extra topics](https://user-images.githubusercontent.com/52863189/78506903-ccb8fe00-7731-11ea-9547-6774fbe0710f.png)

### Out-of-topic handler  
The agent is bound to come accross a topic that it has not been trained on. For this reason, an "irrelevant" tag has been added to the agent's reportoire to respond to such input.  
![out-of-topic](https://user-images.githubusercontent.com/52863189/78506968-333e1c00-7732-11ea-95b4-77d883e75990.png)
 

### Spelling Mistake Recognition  
The agent has been trained on data that has been stemmed using a Snowball stemmer. The Snowball stemmer has been chosen over the Porter and Lancaster stemmers because it has shown the best results in terms of training the agent and responding to the user. Reseach has also shown that it is regarded as the preferred algorithm as it is faster than Porter and less aggressive than Lancaster.  
https://stackoverflow.com/questions/10554052/what-are-the-major-differences-and-benefits-of-porter-and-lancaster-stemming-alg  
![spelling](https://user-images.githubusercontent.com/52863189/78507179-7baa0980-7733-11ea-8d09-336c778fa44f.png)
 

### Synonym Recognition  
The user may not use the exact words that the agent has been trained on. For this reason, synonym recognition has been added. If a word is not understood by the agent, then its synonym list will be generated, and if the word that the agent is trained on is found, then the agent can adjust the response accordingly.  
![synonym](https://user-images.githubusercontent.com/52863189/78508892-152ae880-773f-11ea-90a0-b2e51588b1a5.png)

### POS tagging  
The same word may be used in different contexts. The agent has been trained to understand the context of the word being inputted and accounting for that using POS tagging. So inputting the same word in a different context will generate a different response.  
![pos_tagging](https://user-images.githubusercontent.com/52863189/78508940-64711900-773f-11ea-95c5-8cd8d6aff635.png) 

### Sockets Conversation with External Chatbot  
Simulating a conversation with another agent can bring a good laugh to the spectator. What better way to do this, than to have 2 average chatbots talk to each other while you sit with your popcorn and watch the magic unfold.
<Snippet> 


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
9) spacy

Ensure that you have all of these libraries installed first. If you do not have any of the libraies mentioned above, make sure to use this instruction to install the library:  
  
   pip install <package_name>

You may also be asked to install wordnet and en_core_web_sm as well. For this issue, run Python and type the following instructions:  
1) import nltk  
2) nltk.download('wordnet') or just nltk.download()  

AND  

python -m spacy download en_core_web_sm

Everything should workout from here.  

## How to Run the code

Run the project.py file and enjoy your chatbot!


## Built With
Python - Programming language  
JSON - File Format  
