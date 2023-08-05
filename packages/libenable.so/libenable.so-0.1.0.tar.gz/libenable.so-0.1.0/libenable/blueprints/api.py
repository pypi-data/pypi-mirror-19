'''
RESTful API

This module defines the Flask blueprint for the RESTful API. See the
documentation for each object and their respective unit tests for more
information.
'''

from flask import Blueprint, render_template
from flask_restful import Api, Resource
import json
import libenable
import sys
import time

blueprint = Blueprint('api', __name__, template_folder = '../templates')
api = Api(blueprint)

class Version(Resource):
	'''
	Returns the version of the application
	'''

	def get(self):
		return {'version': libenable.__version__}

class Statistics(Resource):
	'''
	Returns statistics about the application and the Python interpreter
	'''

	def get(self):
		return {
			'libenable': {
				'status': libenable.__status__.name,
				'running_tasks': libenable.__running_tasks__,
				'total_tasks': libenable.__total_tasks__,
				'status_code': libenable.__status__.value,
				'version': libenable.__version__
			},
			'python': {
				'platform': sys.platform,
				'version': '%i.%i.%i' % sys.version_info[:3]
			},
			'time': {
				'current': int(time.time()),
				'running': int(time.time()) - libenable.__start_time__,
				'start': libenable.__start_time__
			}
		}

@blueprint.route('/')
def show():
	'''
	The documentation for the API
	'''

	return render_template(
		'api.html',
		host = libenable.__host__,
		port = libenable.__port__,
		version = json.dumps(
			Version().get(),
			sort_keys = False,
			indent = 2
		),
		stats = json.dumps(
			Statistics().get(),
			sort_keys = False,
			indent = 2
		)
	)

api.add_resource(Version, '/version')
api.add_resource(Statistics, '/statistics')
