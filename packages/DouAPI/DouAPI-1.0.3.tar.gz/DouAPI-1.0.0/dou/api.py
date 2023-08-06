import requests



class DouAPI(object):

	def method(self, method, values=None):

		if values is not None: values['limit'] = 10000

		response = requests.get('https://api.dou.ua/{0}/'.format(method), params=values)

		if response.status_code == 200:
			return response.json()['results']
		else:
			return 'A request to the Dou API was unsuccessful. The server returned HTTP {0} {1}.'.format(response.status_code, response.reason)


	

class Dou():

	__slots__ = ('_dou')

	def __init__(self):
		self._dou = DouAPI()
		

	def lenta(self, category=None, tag=None, author=None, date_from=None, date_to=None):

		values = locals().copy()
		values.pop('self')

		values = {header:value for header, value in values.items() if value != None}

		return self._dou.method('articles', values=values)





