'''
Solve Media CAPTCHA Challenges

This module is an implementation of the Challenge specification and collects
data to solve Solve Media CAPTCHAs. To use these Challenges, create a new
instance of them and call the `get_data()` function. Then, process the data
using an Agent and submit it by calling the `submit_data()` function. See the
unit tests for this module for more information.
'''

from caboodle.challenges.spec import Challenge
import caboodle.challenges.util as util

class SolveMediaTextChallenge(Challenge):
	'''
	A Challenge for Solve Media Text CAPTCHAs

	A text CAPTCHA is the traditional type of CAPTCHA with obfuscated squiggly
	text. This Challenge will locate it if it exists and add a base64 encoded
	image of the CAPTCHA to the dictionary with the key 'image'. In addition to
	the CAPTCHA, the form to enter the result and the reload button to get a new
	CAPTCHA are added to the dictionary with the keys 'form' and 'reload'
	respectively.
	'''

	def __init__(self):
		super().__init__()

	def get_data(self, browser):
		'''
		Collects data needed to solve the Challenge

		Args:
			browser (Browser): The web browser to use

		Returns:
			A dictionary of collected data

		Raises:
			TypeError: The browser is not of type Browser
		'''

		super().get_data(browser)

		try:
			data = {}

			# Get elements
			data['image'] = browser.find_element_by_id('adcopy-puzzle-image-image')
			data['form'] = browser.find_element_by_id('adcopy_response')
			data['reload'] = browser.find_element_by_id('adcopy-link-refresh')

			# Preprocess elements
			data['image'] = util.get_element_image(data['image'], browser)

			return data
		except:
			return None

	def submit_data(self, data):
		'''
		Submits the processed data and solves the Challenge

		Args:
			data (dict): The Challenge to submit

		Raises:
			TypeError: The data is not a dictionary
		'''

		super().submit_data(data)

		data['form'].send_keys(data['result'])
