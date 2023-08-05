from caboodle import web
import caboodle.challenges.util as util
import os
import unittest

DEBIAN = None
WIKIPEDIA = None

# Locate data file and read it
for root, dirs, files in os.walk(os.getcwd()):
	if 'debian' in files:
		DEBIAN = os.path.join(root, 'debian')
		DEBIAN = open(DEBIAN, 'rb').read()

	if 'wikipedia' in files:
		WIKIPEDIA = os.path.join(root, 'wikipedia')
		WIKIPEDIA = open(WIKIPEDIA, 'rb').read()

class UtilTest(unittest.TestCase):
	'''
	Tests the Challenge utility functions to verify they work correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a Browser to use
		'''

		self.browser = web.Browser(None)

	def test_get_element_image(self):
		'''
		Tests that the function returns the correct image
		'''

		if WIKIPEDIA:
			self.browser.get('https://www.wikipedia.org')

			image = self.browser.find_element_by_tag_name('img')
			image = util.get_element_image(image, self.browser)

			self.assertEqual(image, WIKIPEDIA)
		else:
			self.fail('Could not locate data file')

	def test_get_image_src(self):
		'''
		Tests that the function returns the correct image
		'''

		if DEBIAN:
			self.browser.get('https://www.debian.org')

			image = self.browser.find_element_by_tag_name('img')
			image = util.get_image_src(image)

			self.assertEqual(image, DEBIAN)
		else:
			self.fail('Could not locate data file')

	@classmethod
	def tearDownClass(self):
		'''
		Closes the Browser to end the test
		'''

		self.browser.quit()

if __name__ == '__main__':
	unittest.main()
