import requests
from .response import UnwiredResponse


class UnwiredConnection:
	"""
	Unwiredlabs server connection class.

	You may specify a custom server by supplying ``server``, defaults to the EU server.
	If you only use one account on that connection you may specify your API Key ``key``
	while initializing this
	"""

	def __init__(self, server='eu1.unwiredlabs.com', key=None):
		self.session = requests.Session()
		self.server = server
		self.key = key

	def performRequest(self, request):
		"""
		Perform a request on the connection and return the response, blocks until response received
		This may throw network and runtime errors when something goes wrong.

		:param request: the request to perform
		:return: ``UnwiredResponse`` object with the response
		"""
		headers = {
			"ContentType": "application/json",
			"Accept": "application/json"
		}
		request = requests.Request(
			"POST",
			"https://{}/v2/process.php".format(self.server),
			headers=headers,
			json=request.serialize(key=self.key)
		)
		prep = self.session.prepare_request(request)
		response = self.session.send(prep)
		return UnwiredResponse(response)