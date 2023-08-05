'''
Utility Functions for Challenges

This module defines useful and frequently used functions for use in Challenges.
Import this module to use them.
'''

from io import BytesIO
from PIL import Image
import base64
import requests

def get_element_image(element, browser):
	'''
	Takes a screenshot and crops out the element

	Args:
		element (WebElement): The element to crop
		browser (Browser): The web browser to use

	Returns:
		A base64 encoded JPEG image
	'''

	result = BytesIO()

	x, y = element.location['x'], element.location['y']
	w, h = element.size['width'], element.size['height']

	screen = BytesIO(base64.b64decode(browser.get_screenshot_as_base64()))
	Image.open(screen).crop((x, y, x + w, y + h)).save(result, format = 'JPEG')

	return base64.b64encode(result.getvalue())

def get_image_src(element):
	'''
	Downloads the source of an image

	Args:
		element (WebElement): The element to download

	Returns:
		A base64 encoded image
	'''

	return base64.b64encode(requests.get(element.get_attribute('src')).content)
