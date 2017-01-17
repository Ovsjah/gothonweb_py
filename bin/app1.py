import web

urls = ('/upload', 'Upload')

app = web.application(urls, globals())
render = web.template.render('templates/', base="layout")

class Upload(object):
    def GET(self):
        return render.upload()
        
    def POST(self):
        form = web.input(pic={})
        pic = form['pic'].filename
        return render.after_upload(pic=pic)
        
       
if __name__ == "__main__":
    app.run()        
