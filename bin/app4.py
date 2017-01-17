import web

urls = (
  '/hello', 'Index',
  '/upload', 'Upload'
)


app = web.application(urls, globals())

render = web.template.render('templates/', base="layout1")

class Index(object):
    def GET(self):
        return render.hello_form()
        
    def POST(self):
        form = web.input(name="Nobody", greet="Hail")
        print form
        print form.name
        print form.greet
        hello = "%s, %s" % (form.greet, form.name)
        return render.index(greeting = hello)


class Upload(object):
    def GET(self):
        return render.upload()
        
    def POST(self):
        form = web.input(myfile={})
        #print "THIS IS JUST form!"
        #print form
        print "THIS IS form.myfile!"
        print form.myfile
        web.debug(form['myfile'].filename) # This is the filename
        #web.debug(form['myfile'].value) # This is the file contents
        #web.debug(form['myfile'].file.read()) # Or use a file(-like) object
        with open('static/' + form['myfile'].filename, 'w') as f:
            f.write(form['myfile'].file.read())
        return render.after_upload(myfile=form['myfile'].filename)
if __name__ == "__main__":
    app.run()
