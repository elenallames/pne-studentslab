import http.client
import json
import termcolor

SERVER = 'rest.ensembl.org'
ENDPOINT = '/sequence/id/ENSG00000207552'
PARAMS = '?content-type=application/json'
URL = SERVER + ENDPOINT + PARAMS

print()
print(f"Server: {SERVER}")
print(f"URL : {URL}")

#Connect with the server
conn = http.client.HTTPConnection(SERVER)


try:
    conn.request("GET", ENDPOINT + PARAMS)
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

# -- Read the response message from the server
r1 = conn.getresponse()

# -- Print the status line
print(f"Response received!: {r1.status} {r1.reason}\n")

# -- Read the response's body
data1 = r1.read().decode("utf-8")

gene = json.loads(data1)

print()
termcolor.cprint("Gene: ", 'green', end="")
print("MIR633")

termcolor.cprint("Description: ", 'green', end="")
print(gene['desc'])


termcolor.cprint("Bases: ", 'green', end="")
print(gene['seq'])
