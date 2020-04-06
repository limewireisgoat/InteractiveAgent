import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

#this function returns a  list of tuples.
#The tuples come in the form of entity, its iob code, and its type
def getNER(string):
    nerList = nlp(string)
    nerList = [(X.text, X.ent_iob_, X.ent_type_) for X in nerList]
    return nerList