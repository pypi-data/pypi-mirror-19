'''
ReCAPTCHA CAPTCHA Challenges

This module is an implementation of the Challenge specification and collects
data to solve ReCAPTCHA CAPTCHAs. To use these Challenges, create a new
instance of them and call the `get_data()` function. Then, process the data
using an Agent and submit it by calling the `submit_data()` function. See the
unit tests for this module for more information.
'''

from caboodle.challenges.spec import Challenge
import caboodle.challenges.util as util
import time

class RecaptchaV2Challenge(Challenge):
	'''
	A Challenge for ReCAPTCHA v2 CAPTCHAs

	Version 2 of ReCAPTCHA is the common "I'm not a robot" CAPTCHA where you are
	prompted to choose a selection of images from a grid. This Challenge will
	locate the grid of images and add the aggregate of all the images to the
	dictionary with the key 'image'. In addition to the CAPTCHA, the elements to
	click, the verify button, the text instructions, the type of image to look
	for, the reload button to get a new CAPTCHA and the dimensions of the image
	grid are added to the dictionary with the keys 'tiles', 'verify', 'text',
	'tag', 'reload', 'columns' and 'rows' respectively.
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

			# Find widget and switch to it
			browser.switch_to_frame(
				browser.find_element_by_xpath(
					'//iframe[@title="recaptcha widget"]'
				)
			)

			# Start challenge
			browser.find_element_by_id('recaptcha-anchor').click()

			# Return to default frame
			browser.switch_to_default_content()

			# Find challenge and switch to it
			browser.switch_to_frame(
				browser.find_element_by_xpath(
					'//iframe[@title="recaptcha challenge"]'
				)
			)

			# Wait for image to load
			start_time = time.time()
			while len(browser.find_elements_by_tag_name('img')) < 1:
				if time.time() - start_time > 5:
					# Return to default frame
					browser.switch_to_default_content()

					# Find widget and switch to it
					browser.switch_to_frame(
						browser.find_element_by_xpath(
							'//iframe[@title="recaptcha widget"]'
						)
					)

					# Assert challenge is solved
					isChecked = browser.find_element_by_id('recaptcha-anchor')\
						.get_attribute('aria-checked') == 'true'

					if isChecked:
						return 'solved'

					# Return to default frame
					browser.switch_to_default_content()

					# Find challenge and switch to it
					browser.switch_to_frame(
						browser.find_element_by_xpath(
							'//iframe[@title="recaptcha challenge"]'
						)
					)

				time.sleep(1)
			del start_time

			# Get elements
			data['image'] = util.get_image_src(
				browser.find_element_by_tag_name('img')
			)
			data['tiles'] = browser.find_elements_by_class_name(
				'rc-image-tile-target'
			)
			data['verify'] = browser.find_element_by_id(
				'recaptcha-verify-button'
			)
			data['text'] = browser.find_element_by_class_name(
				'rc-imageselect-instructions'
			).text
			data['tag'] = browser.find_element_by_xpath(
				'//div[@class="rc-imageselect-instructions"]//strong'
			).text
			data['reload'] = browser.find_element_by_id(
				'recaptcha-reload-button'
			)
			table = browser.find_element_by_tag_name('table')
			value = table.get_attribute('class')[-2:]
			data['columns'] = int(value[0])
			data['rows'] = int(value[1])

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

		for tile in data['result']:
			try:
				data['tiles'][tile].click()
			except IndexError:
				pass

		data['verify'].click()
