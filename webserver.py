#!/usr/bin/python

import os, os.path
import glob
import random
import string
import json

import cherrypy
from lapps import Lapps
import blockly_runner

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return file('index.html')

class Control(object):

    @cherrypy.expose
    def status(self):
	cmd = """{
	  "hash": -7985492147856592190, 
	  "status": "running"
	}"""
	return cmd

    @cherrypy.expose
    def run(self):
	cmd = """{
	  "hash": -7985492147856592190, 
	  "status": "running"
	}"""
	return 'done'

    @cherrypy.expose
    def stop(self):
	cmd = """{
	  "hash": -7985492147856592190, 
	  "status": "running"
	}"""
	return cmd

class RunAPI(object):

    exposed = True

    def GET(self, name):	
	blockly_runner.run("apps/" + name + ".py")
	return 'done'

class LappsAPI(object):

    exposed = True

    def PUT(self, name=None):
	params = json.loads(cherrypy.request.body.read())
	app_type = name.split('-')

	if params['state'] == 'partial':
		app = open("apps/" + name + '.py', 'w+')
		if app_type[1] == 'blockly':
		    app = open("apps/" + name + '.xml', 'w+')
	else:
		app = open("apps/" + name + '.py', 'w+')

		if params['from_blockly'] == True:
		    app.write(params['by_code'])
		    pyfile = open("apps/" + name + ".xml", 'w+')
		    pyfile.write(params['py_code'])
		else:
		    app.write(params['py_code'])

	app.close()

#    def GET(self, app_name=None):
#	if cherrypy.request.method == 'GET':
#	    lapps = []
#
#	    lapp = {}
#
#	    for filename in os.listdir("/home/frazer/Downloads/DiscoveryServer/apps/"):
#		output = {}
#
#		if os.path.splitext(filename)[1] == ".xml":
#	    	    output['from_blockly'] = True
#		elif os.path.splitext(filename)[1] == ".py":
#	            output['from_blockly'] = False
#		
#		output['id'] = filename
#
#		output['name'] = filename
#
#		output['comment'] = 'Hello World'
#
#		output['author'] = 'Frazer'
#
#		app = open("/home/frazer/Downloads/DiscoveryServer/apps/" + filename)
#		app.seek(0)
#		output['py_code'] = app.read()
#
#	        lapps.append(output)
#		
#		out = {}
#		out["lapps"] = lapps
#
#            return json.dumps(out)

    def GET(self, app_name=None):
	lapps = []

	for filename in os.listdir("apps/"):
		if filename.endswith(".py"):
			output = {}

			name = os.path.splitext(filename)[0]

			if os.path.exists("apps/" + name + ".xml"):
			    output['from_blockly'] = True
			    xml_app = open("apps/" + name + ".xml")
			    output['by_code'] = xml_app.read()
			else:
			    output['from_blockly'] = False

			output['id'] = name

			output['name'] = name

			output['comment'] = 'Hello World'

			output['author'] = 'Frazer'

			app = open("apps/" + filename)
			output['py_code'] = app.read()

			lapps.append(output)

	out = {}
	out["lapps"] = lapps

	return json.dumps(out)

class NewLappAPI(object):

    exposed = True

    def GET(self, app):
	app = open("apps/" + app + ".py", "w+")	
	app.close()

if __name__ == '__main__':
     conf = {
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
         },
         '/generator': {
             'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
             'tools.response_headers.on': True,
             'tools.response_headers.headers': [('Content-Type', 'text/plain')],
         },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './static'
         }
     }

     cherrypy.tree.mount(StringGenerator(), '/', conf)
     #cherrypy.tree.mount(Control(), '/v1/ctrl')

     cherrypy.tree.mount(LappsAPI(), '/v1/lapps',
    {'/':
        {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    })

     cherrypy.tree.mount(NewLappAPI(), '/v1/lapps/new',
    {'/':
        {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    })

     cherrypy.tree.mount(RunAPI(), '/v1/ctrl/run',
    {'/':
        {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    })

     cherrypy.server.socket_host = '0.0.0.0'
     cherrypy.engine.start()
     cherrypy.engine.block()
