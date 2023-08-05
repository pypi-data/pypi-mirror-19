from caboodle import web
from caboodle.challenges.solve_media import SolveMediaTextChallenge
from caboodle.challenges.spec import Challenge
import unittest

class SolveMediaTextChallengeTest(unittest.TestCase):
	'''
	Tests the SolveMediaTextChallenge to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a Challenge to test
		'''

		self.browser = web.Browser(None)
		self.challenge = SolveMediaTextChallenge()

	def test_init(self):
		'''
		Tests that the SolveMediaTextChallenge initializes correctly
		'''

		self.assertIsInstance(self.challenge, Challenge)

	def test_get_data(self):
		'''
		Tests that the SolveMediaTextChallenge can collect data
		'''

		self.assertFalse(self.challenge.get_data(self.browser))

		self.browser.get(
			'http://wsnippets.com/demo/solve-media-captcha-php/index.php'
		)

		data = self.challenge.get_data(self.browser)
		self.assertTrue(data['image'])
		self.assertTrue(data['form'])
		self.assertTrue(data['reload'])

		with self.assertRaises(TypeError):
			self.challenge.get_data(None)

	def test_submit_data(self):
		'''
		Tests that the SolveMediaTextChallenge can submit data
		'''

		self.browser.get(
			'http://wsnippets.com/demo/solve-media-captcha-php/index.php'
		)

		data = self.challenge.get_data(self.browser)
		data['result'] = '42'

		self.challenge.submit_data(data)

		self.assertEqual(data['form'].get_attribute('value'), '42')

	@classmethod
	def tearDownClass(self):
		'''
		Closes the Browser to end the test
		'''

		self.browser.quit()

if __name__ == '__main__':
	unittest.main()
