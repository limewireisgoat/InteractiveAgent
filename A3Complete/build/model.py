
import config

#method to create a new model
def create(training, output):
    config.agent.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    config.agent.save("model.tflearn")

#method to load the existing model
def load():
    try:
        config.agent.load('model.tflearn')
    except:
        print("Error loading Model")