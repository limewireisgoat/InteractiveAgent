import setup as s
from setup import numpy as np
from setup import random as r

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
def chatWithAgent():
    print("Start talking with the bot (type goodbye to stop)!")
    while True:
        user = input("You: ")

        try:
            results = s.model.predict([fitInput(user)])                                         #fit the user input into the format that the model can read and predict the result
            results_index = np.argmax(results)                                                  #index the tag with the highest probability
            result_tag = s.labels[results_index]                                                #return that tag

            results = s.model.predict([fitInput(user)])                                         #fit the user input into the format that the model can read and predict the result
            result_tag = getResponse(results)                                                   #get the response tag that the model predicts

            #find the intent with the specified tag and get the responses
            for intent in s.data["intents"]:
                if intent['tag'] == result_tag:
                    responses = intent['responses']

            print("Mahmoud: " + r.choice(responses))

            if result_tag == "goodbye":
                break
        except:
            print("Error in Model Prediction")