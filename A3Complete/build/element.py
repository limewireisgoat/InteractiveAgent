def createElements(pattern, pos_stemmed_words, nerlist):
    nerlist = shrinkNERList(pattern, nerlist)
    pos_ner_stemmed_words = combineLists(pos_stemmed_words, nerlist)
    return pos_ner_stemmed_words

def shrinkNERList(pattern, nerlist):
    shrunkNERlist = []
    for i,element in enumerate(pattern):
        while(getelements(nerlist[i])[0] != element):
            nerlist.pop(i)
        shrunkNERlist.append(nerlist[i])

    return shrunkNERlist

def getelements(element):
    nerlist = list(element)
    word = nerlist[0]
    iob = nerlist[1]
    typ = nerlist[2]
    return word, iob, typ

def combineLists(pos_stemmed_words, nerlist):
    pos_ner_stemmed_words = []
    for i,element in enumerate(pos_stemmed_words):
        word, iob, typ = getelements(nerlist[i])
        POS_stemmed_list = list(element)
        POS_stemmed_list.append(iob)
        POS_stemmed_list.append(typ)
        POS_stemmed_tup = tuple(POS_stemmed_list)
        pos_ner_stemmed_words.append(POS_stemmed_tup)
    return pos_ner_stemmed_words
