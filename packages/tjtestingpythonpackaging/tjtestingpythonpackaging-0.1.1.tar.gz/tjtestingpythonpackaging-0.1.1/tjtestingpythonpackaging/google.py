import requests


class Google(object):
	def __init__(self):
		pass

	def get_homepage_html(self):
		response = requests.get('https://www.google.com')
		print response.text
		
