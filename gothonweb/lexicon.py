import parser

class WordSep(object):

    def __init__(self, stuff):
        self.stuff = stuff
        
    def cutter(self):
        words = self.stuff.split()
        return words 


class Grammar(object):

    direction_words = [
    'direction','north', 'south', 
    'east','west', 'down', 
    'up', 'left',
    'right', 'back'
    ]
    verbs = ['verb', 'go', 'stop', 'kill', 'eat', 'place', 'throw', 'shoot', 'dodge', 'tell']
    stop_words = ['stop word', 'a', 'the', 'in', 'of', 'from', 'at', 'it']
    nouns = ['noun', 'door', 'bear', 'princess', 'cabinet', 'joke', 'bomb', 'them']
    lexicon = [direction_words, verbs, stop_words, nouns]
    
    def edit(self, sentence):
        self.sentence = sentence
        for word in sentence:
            if type(word) != tuple:
                pos = sentence.index(word)
                sentence[pos] = ('error', word)
        return sentence


class Scanner(Grammar):
    
    def __init__(self):
        pass
        
    def scan(self, stuff):
        self.stuff = stuff    
        words = WordSep(stuff).cutter()
        sentence = []
        for word in words:
            lower = word.lower()
            try:
                word = ('number', int(word))
            except ValueError:
                for self.data in self.lexicon:
                    if lower in self.data:
                        word = (self.data[0], word)
            sentence.append(word)
        Grammar().edit(sentence)
        return sentence
