import web
from gothonweb import map

urls = (
    '/game', 'GameEngine',
    '/', 'Index',
)

app = web.application(urls, globals())

# little hack so that debug mode works with sessions
if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store,
                                  initializer={'room': None})
    web.config._session = session
else:
    session = web.config._session
    
render = web.template.render('templates/', base="layout")


class Index(object):
    def GET(self): 
        # this is used to "setup" the session with starting values
        if session.room == None or session.room.name == 'The End' or session.room.name == 'death':           
            session.room = map.START
        else:
            session.room
            
        web.seeother("/game")
        
        
class GameEngine(object):

    def GET(self):
        try:
            web.debug(session.room.name)
        except AttributeError:
            web.debug(session.room)
            print "'NoneType' object has no attribute 'name'"
        if session.room:
            return render.show_room(room=session.room)
        else:
            session.room = map.generic_death
            return render.you_died(room = session.room)
            
    def POST(self):
        form = web.input(action=None)
        
        # there is a bug here, can you fix it?
        if session.room and form.action:
            session.room = session.room.go(form.action)
            
        web.seeother("/game")
        
if __name__ == "__main__":
    app.run()
