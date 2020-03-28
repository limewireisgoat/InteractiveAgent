import setup as s

def loadExistingData():

    with open("data.pickle", "rb") as f:
        s.dictionary, s.labels, s.training, s.output = s.pickle.load(f)

#method to load the existing model
def loadExistingModel():
    s.model = s.model.load('model.tflearn')

def load():
    loadExistingData()
    loadExistingModel()
