import http.client
import json
from http import HTTPStatus

SERVER = 'localhost'
PORT = 8081


def make_request(path):
    try:
        connection = http.client.HTTPConnection(SERVER, port=PORT)
        connection.request("GET", path)
        response = connection.getresponse()
        print(f"Response received!: {response.status} {response.reason}\n")
        if response.status == HTTPStatus.OK:
            data_str = response.read().decode()
            data = json.loads(data_str)
            return data
        else:
            print(f"Error: {response.status} - {response.read().decode()}")
            return None
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()


def process_chromosome_length():
    data = make_request("/chromosomeLength?species=mouse&chromo=18&json=1")
    if data:
        chromosome = data['chromosome']
        length = data['length']
        print(f"Chromosome: {chromosome}, Length: {length}")


def process_gene_seq(gene):
    data = make_request(f"/geneSeq?gene={gene}&json=1")
    if data:
        gene = data['gene']
        bases = data['bases']
        print(f"Gene: {gene}, Bases: {bases}")


def main():
    process_chromosome_length()
    process_gene_seq("FRAT1")
    process_gene_seq("TEST")


if __name__ == "__main__":
    main()
