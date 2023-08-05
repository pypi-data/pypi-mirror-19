'''
Configuration

This module defines the Flask blueprint for the application's configuration. See
the documentation for each object and their respective unit tests for more
information.
'''

from flask import Blueprint, redirect, render_template, request
import libenable

blueprint = Blueprint('config', __name__, template_folder = '../templates')

@blueprint.route('/')
def show():
	'''
	The configuration interface
	'''

	return render_template('config.html', config = libenable.config)

@blueprint.route('/save', methods = ['POST'])
def save():
	'''
	Saves the configuration
	'''

	libenable.config['DEFAULT']['host'] = request.form['host']
	libenable.config['DEFAULT']['port'] = request.form['port']

	with open(libenable.__conf__, 'w') as configfile:
		libenable.config.write(configfile)

	return redirect('/')
