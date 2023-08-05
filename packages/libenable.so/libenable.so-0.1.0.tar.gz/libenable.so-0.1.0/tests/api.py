from requests import get
import unittest

class ApiTest(unittest.TestCase):
	'''
	Tests the RESTful API to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Verifies that the application is running
		'''

		try:
			get('http://localhost')
		except:
			self.fail(
				'Could not connect, the application is not running on port 80'
			)

	def test_version(self):
		'''
		Tests that the API handles the version route correctly
		'''

		data = get('http://localhost/api/version').json()
		self.assertTrue('version' in data)

	def test_statistics(self):
		'''
		Tests that the API handles the statistics route correctly
		'''

		data = get('http://localhost/api/statistics').json()
		self.assertTrue('libenable' in data)
		self.assertTrue('status' in data['libenable'])
		self.assertTrue('running_tasks' in data['libenable'])
		self.assertTrue('total_tasks' in data['libenable'])
		self.assertTrue('status_code' in data['libenable'])
		self.assertTrue('version' in data['libenable'])
		self.assertTrue('python' in data)
		self.assertTrue('platform' in data['python'])
		self.assertTrue('version' in data['python'])
		self.assertTrue('time' in data)
		self.assertTrue('current' in data['time'])
		self.assertTrue('running' in data['time'])
		self.assertTrue('start' in data['time'])
