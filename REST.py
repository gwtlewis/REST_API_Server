# -*- coding: utf-8 -*-
import commands
import web
import logging

render = web.template.render('templates')

urls = (
    '/', 'index',
    '/exe', 'RunDocker',
    '/test', 'Test'
)


class index:
    def GET(self):
        return render.index()

class RunDocker:
    def GET(self):
        r = commands.getstatusoutput('cd /opt/apps/Docker_tomcat_8')
        return str(r)


class Test:
    def GET(self):
        r = commands.getstatusoutput('pwd')
        return str(r)

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
