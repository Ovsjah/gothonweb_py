class ParserError(Exception):
    pass
    
    
class Sentence(object):

    def __init__(self, subject, verb, obj):
        self.subject = subject[1]
        self.verb = verb[1]
        self.object = obj[1]
        
    def edit(self):
        return "%s %s %s" % (self.subject,
                                 self.verb, self.object)
                                          
            
class Subject(object):

    def parse_subject(self, data):
        self.data = data
        Stuff().skip(data, 'stop word')
        Stuff().skip(data, 'error')
        next_word = Stuff().peek(data)
        
        if next_word == 'noun':
            return Stuff().match(data, 'noun')
        elif next_word == 'verb':
            return ('noun', 'player')
        else:
            raise ParserError("Expected a verb next.")
            

class Verb(object):
    
    def parse_verb(self, data):
        self.data = data
        Stuff().skip(data, 'stop word')
        Stuff().skip(data, 'error')
        next_word = Stuff().peek(data)
        
        if next_word == 'verb':
            return Stuff().match(data, 'verb')
        else:
            raise ParserError("Expected a verb next.")


class Object(object):
        
    def parse_object(self, data):
        self.data = data
        Stuff().skip(data, 'stop word')
        Stuff().skip(data, 'error')
        next_word = Stuff().peek(data)
        
        if next_word == 'noun':
            return Stuff().match(data, 'noun')
        elif next_word == 'direction':
            return Stuff().match(data, 'direction')
        else:
            raise ParserError("Expected a noun or direction next.")


class Stuff(Subject, Verb, Object):
    
    def __init__(self):
        pass
        
     
    def parse_sentence(self, data):
        self.data = data
        subj = Subject().parse_subject(data)
        verb = Verb().parse_verb(data)
        obj = Object().parse_object(data)
        
        return Sentence(subj, verb, obj)
        
    def peek(self, data):
        self.data = data
        if data:
            word = data[0]
            return word[0]
        else:
            return None
            
    def match(self, data, exp):
        self.data = data
        self.exp = exp
        if data:
            word = data.pop(0)
            
            if word[0] == exp:
                return word
            else:
                return None
        else:
            return None
            
    def skip(self, data, word_type):
        self.data = data
        self.word_type = word_type
        while self.peek(data) == word_type:
            self.match(data, word_type)
