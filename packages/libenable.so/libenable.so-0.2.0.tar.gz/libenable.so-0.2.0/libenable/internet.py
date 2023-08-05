'''
Internet

This module defines functions for enabling access to Internet domains. The
RESTful API uses these functions to generate a result. See the documentation for
each function and the unit tests for more information.
'''

from caboodle import web, solve
from caboodle.agents import *
from caboodle.challenges.recaptcha import RecaptchaV2Challenge
import libenable
import time

def access_reCAPTCHA(site_key, **agents):
	'''
	Enables access to reCAPTCHA protected domains

	Args:
		site_key (str): The site key of the domain
		**agents (str): Key word arguments describing which agents to use

	Returns:
		A tuple containing a dictionary and the cost of the action

	Agents must be declared using the name of the module from which they are
	located. The argument must be a dictionary containing the arguments you
	would normally pass to instantiate that Agent.

	Example:

		access_reCAPTCHA(
			'site key',
			d3cryp7 = {'url': 'localhost'},
			rucaptcha = {'key': 'api key'}
		)
	'''

	libenable.amWorking()

	browser = web.Browser()
	solver = solve.Solver(browser)

	# Dynamically add agents
	for agent in spec.Agent.__subclasses__():
		module = agent.__module__.split('.')[-1:][0]

		if module in tuple(agents.keys()):
			solver.add_agent(agent(**agents[module]))

	solver.add_challenge(RecaptchaV2Challenge())

	browser.get('https://www.google.com')
	browser.execute_script(
	'''
	document.getElementsByTagName('html')[0].remove();
	var html = document.createElement('html');
	var head = document.createElement('head');
	var scr = document.createElement('script');
	scr.type = 'text/javascript';
	scr.src = 'https://www.google.com/recaptcha/api.js';
	head.appendChild(scr);
	html.appendChild(head);
	var body = document.createElement('body');
	var div = document.createElement('div');
	div.setAttribute('id', 'g-recaptcha');
	div.setAttribute('class', 'g-recaptcha');
	div.setAttribute('data-sitekey', '%s');
	body.appendChild(div);
	html.appendChild(body);
	document.appendChild(html);
	''' % site_key
	)

	cost = 0.0
	result = {
		'result': None
	}

	id = None
	for _ in range(5):
		try:
			id = solver.solve()

			if id:
				cost = solver.data[id]['agent'].get_cost()

			break
		except:
			pass

		time.sleep(1)

	for _ in range(5):
		try:
			response = browser.find_element_by_id('g-recaptcha-response')
			response = response.get_attribute('value')
		except:
			time.sleep(1)
			continue

		if len(response) > 0:
			solver.set_success(id)
			result['result'] = response
			break

		time.sleep(1)
	else:
		solver.set_fail(id)
		result['error'] = 'Failed to receive a response'
		cost = 0.0

	browser.quit()

	libenable.amRunning()

	return (result, cost)
