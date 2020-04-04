import setup as s
from setup import numpy as np
from setup import random as r

#method to get the tag that corresponds to the user input
def fitInput(user_input):
    bag = [0 for _ in range(len(s.dictionary))]

    s_dictionary = s.nltk.word_tokenize(user_input)
    s_dictionary = [s.stemmer.stem(word.lower()) for word in s_dictionary]

    for se in s_dictionary:
        for i, word in enumerate(s.dictionary):
            if word == se:
                bag[i] = 1
            
    return np.array(bag)


#chatting method
def chatWithAgent():
    print("Start talking with the bot (type goodbye to stop)!")
    while True:
        user = input("You: ")

        try:
            results = s.model.predict([fitInput(user)])                                         #fit the user input into the format that the model can read and predict the result
            results_index = np.argmax(results)                                                  #index the tag with the highest probability
            result_tag = s.labels[results_index]                                                #return that tag

            for intent in s.data["intents"]:
                if intent['tag'] == result_tag:
                    responses = intent['responses']

            print("Mahmoud: " + r.choice(responses))

            if result_tag == "goodbye":
                break
        except:
            print("Error in Model Prediction")
