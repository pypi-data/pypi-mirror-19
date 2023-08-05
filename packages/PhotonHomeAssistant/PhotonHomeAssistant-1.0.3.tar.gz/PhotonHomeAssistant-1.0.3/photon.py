from http.client import HTTPSConnection
from json import loads as parseJson

def request(deviceId, accessToken, command):
	connection = HTTPSConnection("api.particle.io")
	
	path = "/v1/devices/{deviceId}/light?access_token={accessToken}".format(deviceId=deviceId,accessToken=accessToken)
	data = "args=" + command
	headers = { "Content-type": "application/x-www-form-urlencoded" }
	connection.request("POST", path, data, headers)

	response = connection.getresponse()
	body = parseJson(response.read().decode())
	return body