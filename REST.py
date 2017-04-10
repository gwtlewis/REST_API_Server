# -*- coding: utf-8 -*-
# !/usr/bin/env python
import commands
import web
import logging
import json
import pymongo
import datetime

# Server running log
logFormat = "%(asctime)s [%(levelname)s] %(filename)s => %(message)s"
logging.basicConfig(filename="./logs/REST_API_Server.log", level=logging.DEBUG, format=logFormat)

# Server templates path and routers
render = web.template.render('templates')

urls = (
    '/', 'index',
    '/docker', 'RunDocker',
    '/mongo', 'Mongo',
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
        web.header('Content-Type', 'text/json;charset=utf-8')
        callback = web.input(callback='callback')['callback']
        logging.info("RunDocker: starting container-tomcat")
        r = commands.getstatusoutput('/opt/apps/Docker_tomcat_8/startTomcatDocker.sh')
        logging.info("RunDocker: running results: " + r[1])
        if r[0] == 0:
            logging.info("RunDocker: run docker successfully. Please enjoy the service")
            return "%s(%s)" % (callback, results.success())
        else:
            logging.error("RunDocker: run docker failed.")
            return "%s(%s)" % (callback, results.fail())


class Mongo:
    def GET(self):
        logging.info('Client is trying to duplicate Mongo collection.')
        web.header('Content-Type', 'application/javascript;charset=utf-8')
        callback = web.input(callback='callback')['callback']
        try:
            names = ['gm', 'jd']
            oneday = datetime.timedelta(days=1)
            now = datetime.datetime.now()
            today = now.strftime("%Y%m%d")
            yst = (now - oneday).strftime("%Y%m%d")
            tmr = (now + oneday).strftime("%Y%m%d")
            logging.info('Mongo: initializing Mongo Client...')
            client = pymongo.MongoClient(host="118.89.48.117", port=27027)
            logging.info('Mongo: trying to connect to Mongo database...')
            db = client['Douban']
            logging.info('Mongo: trying to authenticate with  Mongo user...')
            db.authenticate(name="dbOwner", password="Db1419")
            logging.info('Mongo: connect to Mongo successfully.')
            for name in names:
                today_collection = db[name + '_computers_' + today]
                yst_collection = db[name + '_computers_' + yst]
                tmr_collection = db[name + '_computers_' + tmr]
                if today_collection.count() != 0 and tmr_collection.count() == 0:
                    logging.info('Mongo: trying to duplicate today collection for tomorrow.')
                    tmr_collection.insert_many(today_collection.find())
                elif today_collection.count() == 0 and yst_collection.count() != 0:
                    logging.info('Mongo: trying to duplicate from yesterday collection.')
                    today_collection.insert_many(yst_collection.find())
                else:
                    logging.warning('Mongo: '+name+' collection already exists.')
            logging.info('Mongo: job done or skipped, please enjoy the service.')
            return "%s(%s)" % (callback, results.success())
        except Exception as e:
            logging.error('Mongo: unexpected error occurred.' + e.message)
            return "%s(%s)" % (callback, results.fail())


class Test:
    def GET(self):
        logging.info('Client is using the test method')
        web.header('Content-Type', 'application/javascript;charset=utf-8')
        callback = web.input(callback='callback')['callback']
        print callback
        r = commands.getstatusoutput('pwd')
        if r[0] == 0:
            return "%s(%s)" % (callback, results.success())
        else:
            return "%s(%s)" % (callback, results.fail())


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
    web.webapi.config.debug = False
    app.run()
    logging.info('REST API Server stopped.')
