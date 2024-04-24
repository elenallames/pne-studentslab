import http.client
import json
from http import HTTPStatus

SERVER = 'rest.ensembl.org'
RESOURCE = '/info/ping'
PARAMS = '?content-type=application/json'
URL = RESOURCE + PARAMS

print()
print(f"SERVER: {SERVER}")
print(f"URL: {URL}")

connection = http.client.HTTPConnection(SERVER)

try:
    connection.request("GET", URL)
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

response = connection.getresponse()
print(f"Response received!: {response.status} {response.reason}\n")
if response.status == HTTPStatus.OK:
    data_str = response.read().decode()
    data = json.loads(data_str)
    ping = data['ping']
    if ping == 1:
        print("PING OK! The database is running!")
    else:
        print("...")
