import config
import data
import model

#method to know if administrator wants to make changes to the agent
def getAdministratorInfo():
    new = False                                             #boolean to allow for using new/load old data

    adminIn = input("Would you like to train the agent on new data/create a new agent? (y/n) ")
    #adminIn = 'y'
    
    if adminIn == 'y':
        new = True

    if new:
        data.read()
        config.createModel()
        model.create(config.training, config.output)
    else:
        data.load()
        config.createModel()
        model.load()