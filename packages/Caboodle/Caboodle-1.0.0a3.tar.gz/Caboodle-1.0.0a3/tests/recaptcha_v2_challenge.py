from caboodle import web
from caboodle.challenges.recaptcha import RecaptchaV2Challenge
from caboodle.challenges.spec import Challenge
import unittest

class RecaptchaV2ChallengeTest(unittest.TestCase):
	'''
	Tests the RecaptchaV2Challenge to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a Challenge to test
		'''

		self.browser = web.Browser(None)
		self.challenge = RecaptchaV2Challenge()

	def test_init(self):
		'''
		Tests that the RecaptchaV2Challenge initializes correctly
		'''

		self.assertIsInstance(self.challenge, Challenge)

	def test_get_data(self):
		'''
		Tests that the RecaptchaV2Challenge can collect data
		'''

		self.assertFalse(self.challenge.get_data(self.browser))

		self.browser.get('https://www.google.com/recaptcha/api2/demo')

		data = self.challenge.get_data(self.browser)
		self.assertTrue(data['image'] or data == 'solved')
		self.assertTrue(data['tiles'] or data == 'solved')
		self.assertTrue(data['verify'] or data == 'solved')
		self.assertTrue(data['text'] or data == 'solved')
		self.assertTrue(data['tag'] or data == 'solved')
		self.assertTrue(data['reload'] or data == 'solved')
		self.assertTrue(data['rows'] or data == 'solved')
		self.assertTrue(data['columns'] or data == 'solved')

		with self.assertRaises(TypeError):
			self.challenge.get_data(None)

	def test_submit_data(self):
		'''
		Tests that the RecaptchaV2Challenge can submit data
		'''

		self.browser.get('https://www.google.com/recaptcha/api2/demo')

		data = self.challenge.get_data(self.browser)
		data['result'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

		self.challenge.submit_data(data)

	@classmethod
	def tearDownClass(self):
		'''
		Closes the Browser to end the test
		'''

		self.browser.quit()

if __name__ == '__main__':
	unittest.main()
