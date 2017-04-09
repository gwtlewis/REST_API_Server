# -*- coding: utf-8 -*-
import commands
import web
import logging
import json

# Server running log
logFormat = "%(asctime)s [%(levelname)s] %(filename)s => %(message)s"
logging.basicConfig(filename="./logs/REST_API_Server.log", level=logging.DEBUG, format=logFormat)

# Server templates path and routers
render = web.template.render('templates')

urls = (
    '/', 'index',
    '/exe', 'RunDocker',
    '/test', 'Test'
)

app = web.application(urls, globals())


# Router handlers
class index:
    def GET(self):
        logging.info('Client is visiting index page.')
        return render.index()


class RunDocker:
    def GET(self):
        logging.info('Client is trying to run docker.')
        web.header('Content-Type', 'text/json')
        logging.info("RunDocker: going to docker's directory")
        r1 = commands.getstatusoutput('cd /opt/apps/Docker_tomcat_8')
        r = commands.getoutput('pwd')
        if r1[0] == 0:
            logging.info("RunDocker: "+r[0])
            logging.info("RunDocker: running docker")
            r2 = commands.getstatusoutput('./startTomcatDocker.sh')
            if r2[0] == 0:
                logging.info("RunDocker: docker successfully running, enjoy the service")
                return results.success()
            else:
                logging.error("RunDocker: fail to run docker"+r2[1])
                return results.fail()
        else:
            logging.error("RunDocker: fail to go to docker's directory" + r1[1])
            return results.fail()


class Test:
    def GET(self):
        logging.info('Client is using the test method')
        web.header('Content-Type', 'text/json')
        r = commands.getstatusoutput('pwd')
        if r[0] == 0:
            return results.success()
        else:
            return results.fail()


# Results handler
class results:
    @staticmethod
    def success():
        s = '{"result":"OK"}'
        return json.loads(s, encoding='utf-8')

    @staticmethod
    def fail():
        s = '{"result":"BAD"}'
        return json.loads(s, encoding='utf-8')


# Main - run Server
if __name__ == '__main__':
    logging.info('Initializing REST API Server...')
    app.run()
    logging.info('REST API Server stopped.')
