import setup as s

#method to know if administrator wants to make changes to the agent
def getAdministratorInfo():
    new = False                                             #boolean to allow for using new/load old data

    adminIn = input("Would you like to train the agent on new data/create a new agent? (y/n)")
    #adminIn = 'y'
    
    if adminIn == 'y':
        new = True

    if new:
        from newAgent import create
        create()
    else:
        from existingAgent import load
        load()