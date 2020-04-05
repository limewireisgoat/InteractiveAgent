import numpy
import random
import config
from pos import getPOSList
from synonyms import getSynonyms
import gui
import time

isDone = False

#method to fit the user's input into a format that the neural network can understand
def fitInput(userString):
    bag = [0 for _ in range(len(config.dictionary))]                                                           #create a bag of 0s that is the size of the neural network's input 

    user_dictionary = getPOSList(userString)                                                          #make a stemmed pos list from the user's input

    #loop over all our words
    for i, word_postag in enumerate(config.dictionary):                                                               #traverse through our dictionary of words
        if (len(user_dictionary) == 0 ):                                                                #if there are no more words left to study, end
            break

        else:
            for j, userword_postag in enumerate(user_dictionary):                                                    #look through every word in the list of words that the user provided
                if word_postag == userword_postag:                                                                          #if the word that the user provides is in our dictionary,
                    bag[i] = 1                                                                          #then put 1 to show that the word is present
                    user_dictionary.pop(j)                                                              #no need to check for this word ever again
                    break                                                                               #no need to check for the other words

    #account for synonyms now
    for i, word_postag in enumerate(config.dictionary):
        if (len(user_dictionary) == 0 ):                                                                #if there are no more words left to study, end
            break
        
        elif bag[i] == 1:                                                                               #if a word has been accounted for, skip it
            continue

        else:
            for j, userword_postag in enumerate(user_dictionary):                                                    #account for synonyms
                synonyms = getSynonyms(userword_postag[0])
                for synm in synonyms:
                    if synm == word_postag[0]:
                        bag[i] = 1
                        user_dictionary.pop(j)
                        break
                if bag[i] == 1:
                    break
            
    return numpy.array(bag)


#get the reponse
def getResponses(results):
    global isDone
    
    if numpy.amax(results) < 0.70:                                                                      #if the maximum probability that a tag has is 70%, we will asusme that the user entered something that is off topic
        result_tag = 'irrelevant'   
    else:
        results_index = numpy.argmax(results)                                                           #index the tag with the highest probability
        result_tag = config.labels[results_index]                                                              #return that tag
    
    #find the intent with the specified tag and get the responses
    for intent in config.information["intents"]:
        if intent['tag'] == result_tag:
            responses = intent['responses']
    
    if result_tag == "goodbye":
        isDone = True
    
    return responses

#chatting method
def chat():
    graphicalUI = gui.create_gui()
    #print("Start talking with the bot (type goodbye to stop)!")
    while True:
        if isDone:
            break
        else:
            #while the user has not inputted anything, display the gui

            while(not graphicalUI.valid_message):
                graphicalUI.root.update_idletasks()
                graphicalUI.root.update()
            
            #do the algorithm and return result to user
            user = graphicalUI.last_received_message

            results = config.agent.predict([fitInput(user)])                                         #fit the user input into the format that the model can read and predict the result
            responses = getResponses(results)                                                   #get the response tag that the model predicts

            graphicalUI.show_response(random.choice(responses))
