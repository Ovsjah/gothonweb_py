import web
from web import form
from gothonweb import map, lexicon, parser

import random
from hashlib import sha1


# A simple user object that doesn't store passwords in plain text
# see http://en.wikipedia.org/wiki/Salt-(cryptography)
class PasswordHash(object):
    def __init__(self, password_):
        self.salt = "".join(chr(random.randint(33,127)) for x in xrange(64))
        self.saltedpw = sha1(password_ + self.salt).hexdigest()
    def check_password(self, password_):
        """checks if the password is correct"""
        return self.saltedpw == sha1(password_ + self.salt).hexdigest()
        
        
# Note: a secure application would never store passwords in plaintext in the source code
users = {
    'Kermit': PasswordHash('frog'),
    'ET': PasswordHash('eetee'),
    'falken': PasswordHash('joshua')
}


urls = (
    '/', 'Hello',
    '/logout', 'Logout',
    '/register', 'Register',
    '/index', 'Index',
    '/game', 'GameEngine'
)

app = web.application(urls, globals())

# little hack so that debug mode works with sessions
if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store,
                                  initializer={'room': None, 'user': 'anonymous', 'pw': None})
    web.config._session = session
else:
    session = web.config._session
    
render = web.template.render('templates/', base="layout")


signin_form = form.Form(
    form.Textbox('username',
                 form.Validator('Unknown username.',
                                lambda x: x in users.keys()),
                 description='Username:'),
    form.Password('password',
                  description='Password:'),
    validators = [form.Validator("Username and password didn't match.",
                  lambda x: users[x.username].check_password(x.password))])
                  
                  
signup_form = form.Form(
    form.Textbox('username',
                 form.Validator('Username already exists.',
                                lambda x: x not in users.keys()),
                 description='Username:'),
    form.Password('password',
                  description='Password:'),
    form.Password('password_again',
                  description='Repeat your password:'),
    validators = [form.Validator("Passwords didn't match.",
                  lambda i: i.password == i.password_again)])


class Hello(object):
    def GET(self):
        my_signin = signin_form()
        return render.hello(session.user, my_signin)
        
    def POST(self):
        my_signin = signin_form()
        if not my_signin.validates():
            return render.hello(session.user, my_signin)
        else:
            session.user = my_signin['username'].value
            session.pw = my_signin['password'].value
            web.seeother('/index')

class Logout(object):
    def GET(self):
        session.kill()
        raise web.seeother('/')
        
        
class Register(object):
    def GET(self):
        my_signup = signup_form()
        return render.signup(my_signup)
    
    def POST(self):
        my_signup = signup_form()
        if not my_signup.validates():
            return render.signup(my_signup)
        else:
            username = my_signup['username'].value
            password = my_signup['password'].value
            users[username] = PasswordHash(password)
            raise web.seeother('/')


class Index(object):
    
    def GET(self): 
        # this is used to "setup" the session with starting values
        if session.room == None or session.room.name == 'The End' or session.room.name == 'death':
            reload(map)         
            session.room = map.START
        else:
            session.room    # this is used to load saved session object
            
        web.seeother("/game")
        
        
class GameEngine(object):

    def GET(self):
        
        try:
            web.debug(session.room.name), web.debug(session.room.code), web.debug(session.room.guesses), web.debug(session.room.right_one)
        except AttributeError:
            web.debug(session.room)
            print "'NoneType' object has no attribute 'name'"
            
        if session.room:
            return render.show_room(room=session.room, user=session.user)
        else:           
            session.room = map.generic_death
            return render.you_died(room = session.room)
            
    def POST(self):
        form = web.input(action=None)
        web.debug(form)
        web.debug(form.action)
        
        try:
            int(form.action)
            form.action = form.action
        except ValueError:
            try:
                scaned = lexicon.Scanner().scan(form.action)
                edited = parser.Stuff().parse_sentence(scaned).edit()
                form.action = edited
            except parser.ParserError:
                form = web.input(action=None)
        
        if session.room.name == "Laser Weapon Armory" and form.action != session.room.code and session.room.guesses > 1 and form.action != '*':
            session.room.open_lock(form.action)
        elif session.room.guesses == 1 and form.action != session.room.code:            
            form.action = session.room.open_lock(form.action)            
            session.room = session.room.go(form.action)
        elif session.room.name == "Escape Pod" and form.action != session.room.right_one:
            web.debug(session.room.right_one)
            form.action = session.room.take_one(form.action)
            session.room = session.room.go(form.action)                     
        else:
            session.room = session.room.go(form.action)
                    
        web.seeother("/game")
        
        
if __name__ == "__main__":
    app.run()
