import http.server
from http import HTTPStatus
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import jinja2
import os
import json
from Seq import Seq


PORT = 8080
HTML_FOLDER = "html"  # optional, since we could have the html files in the same directory as the server
ENSEMBL_SERVER = "rest.ensembl.org"  # the IP of the server
RESOURCE_TO_ENSEMBL_REQUEST = {
    '/listSpecies': {'resource': "/info/species", 'params': "content-type=application/json"},
    '/karyotype': {'resource': "/info/assembly", 'params': "content-type=application/json"},
    '/chromosomeLength': {'resource': "/info/assembly", 'params': "content-type=application/json"},
    '/geneSeq': {'resource': "/sequence/id", 'params': "content-type=application/json"},
    '/geneInfo': {'resource': "/overlap/id", 'params': "content-type=application/json;feature=gene"}
}  # dict that contains a resource/endpoint as key with a dict as value. we state what we will request to ensembl
RESOURCE_NOT_AVAILABLE_ERROR = "Resource not available"
ENSEMBL_COMMUNICATION_ERROR = "Error in communication with the Ensembl server"
GENES = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]


def read_html_template(file_name):  # RETURNS A TEMPLATE, we don't use it with index.html (static), or could render()
    file_path = os.path.join(HTML_FOLDER, file_name)
    contents = Path(file_path).read_text()
    contents = jinja2.Template(contents)
    return contents


def server_request(server, url):  # the server we connect to and the url of the request
    import http.client  # local import, since we are only using it in this function

    error = False
    data = None
    try:  # if everything is ok, data = content and error = false
        connection = http.client.HTTPSConnection(server)  # HTTPS since "ensembl.org" works with a security layer
        connection.request("GET", url)
        response = connection.getresponse()  # response is type http response
        if response.status == HTTPStatus.OK:
            json_str = response.read().decode()
            data = json.loads(json_str)
        else:  # if response is not OK
            error = True
    except Exception:  # if there is ANY error in the communication with the server, data = none and error = true
        error = True
    return error, data  # returns a duple


def handle_error(endpoint, message):  # endpoint: resource received from the user: message: str response
    # the error.html file has been turned into a TEMPLATE, since the server fills the info depending on the error type
    context = {
        'endpoint': endpoint,
        'message': message
    }
    return read_html_template("error.html").render(context=context)


def list_species(endpoint, parameters):
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]  # storing the dict what contains the keys "resource", "params"
    url = f"{request['resource']}?{request['params']}"
    error, data = server_request(ENSEMBL_SERVER, url)  # we use our function
    if not error:
        limit = None  # REMEMBER LIMIT IS OPTIONAL("None" as default), so if we receive it:
        if 'limit' in parameters:
            limit = int(parameters['limit'][0])
        """print(data)"""

        """WE PARSE THE INFO FROM ENSEMBL"""
        species = data['species']  # list<dict>, each species is a dict
        name_species = []
        for specie in species[:limit]:
            name_species.append(specie['display_name'])
        context = {
            'number_of_species': len(species),
            'limit': limit,
            'name_species': name_species  # list
        }
        contents = read_html_template("species.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)  # we use our function and state a general error
        code = HTTPStatus.SERVICE_UNAVAILABLE  # we change code to "503"
    return code, contents  # returns a duple


def karyotype(endpoint, parameters):
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
    specie = parameters['species'][0]
    url = f"{request['resource']}/{specie}?{request['params']}"
    error, data = server_request(ENSEMBL_SERVER, url)  # we use our function
    if not error:
        """print(data)"""

        """WE PARSE THE INFO FROM ENSEMBL"""
        context = {
            'specie': specie,
            'karyotype': data['karyotype']
        }
        contents = read_html_template("karyotype.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
    return code, contents


def chromosome_length(endpoint, parameters):
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
    specie = parameters['species'][0]  # introduced by user
    user_chromosome = parameters['chromo'][0]  # introduced by user, it is not always an integer!!!
    url = f"{request['resource']}/{specie}?{request['params']}"
    error, data = server_request(ENSEMBL_SERVER, url)  # we use our function
    if not error:
        length = None
        print(data)
        chromosomes_list = data['top_level_region']  # obtain all chromosomes of the specie, it is an array of objects
        for chromo in chromosomes_list:  # will iterate the list of dicts
            if chromo['name'] == user_chromosome:  # WE HAVE FOUND THE REQUESTED CHROMOSOME
                length = chromo['length']
                break

        """OTHER WAY TO DO IT
        length = None
        found = False
        i = 0  # index starts at 0
        while not found and i < len(chromosomes_list):  # not found = True
            chromo = chromosomes_list[i]
            if chromo['name'] == user_chromosome:  # WE HAVE FOUND THE REQUESTED CHROMOSOME 
                length = chromo['length']
                found = True
            i += 1
        """
        context = {
            'length': length,
            'chromosomes_list': chromosomes_list
        }
        contents = read_html_template("chromosome_length.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
    return code, contents


def get_id(gene):  # petition to ensembl that given a gene we transform it to its identifier id
    resource = "/homology/symbol/human/" + gene
    params = 'content-type=application/json;format=condensed'
    url = f"{resource}?{params}"
    error, data = server_request(ENSEMBL_SERVER, url)  # we use our function
    gene_id = None  # in case we ask a nonhuman gene
    if not error:
        print(f"Gene id: {data}")
        gene_id = data["data"][0]["id"]  # we access the position 0 because we only receive one element on the list
    return gene_id


def human_gene(endpoint, parameters):
    gene = parameters['gene'][0]  # 'gene' has to be equal to name="gene"
    gene_id = get_id(gene)
    print(f"Gene: {gene} - Gene ID: {gene_id}")
    if gene_id is not None:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}/{gene_id}?{request['params']}"
        error, data = server_request(ENSEMBL_SERVER, url)  # we use our function
        if not error:
            print(f"Gene sequence: {data}")
            bases = data["seq"]
            context = {
                'gene': gene,
                'bases': bases
            }
            contents = read_html_template("human_gene.html").render(context=context)
            code = HTTPStatus.OK
        else:
            contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
            code = HTTPStatus.SERVICE_UNAVAILABLE
        return code, contents
    """else:
        contents = handle_error(endpoint, GENE_ERROR)
        code = HTTPStatus.NOT_FOUND
        """


def geneInfo(endpoint, parameters):
    gene = parameters['gene'][0]  # 'gene' has to be equal to name="gene"
    gene_id = get_id(gene)
    print(f"Gene: {gene} - Gene ID: {gene_id}")
    if gene_id is not None:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}/{gene_id}?{request['params']}"
        error, data = server_request(ENSEMBL_SERVER, url)  # we use our function
        if not error:
            print(f"Gene Info: {data}")
            start = data[0]["start"]  # we must take the position 0 from the list which is the dict will all the info
            end = data[0]["end"]
            length = end - start
            chromosome = data[0]['assembly_name']
            context = {
                'id': gene_id,
                'gene': gene,
                'start': start,
                'end': end,
                'length': length,
                'chromosome': chromosome
            }
            contents = read_html_template("gene_info.html").render(context=context)
            code = HTTPStatus.OK
        else:
            contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
            code = HTTPStatus.SERVICE_UNAVAILABLE
        return code, contents


"""MAIN PROGRAM"""

socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path  # also known as resource/ path
        print(f"Endpoint: {endpoint}")
        parameters = parse_qs(parsed_url.query)  # takes the request and gets the info from "?": it is a dictionary
        print(f"Parameters: {parameters}")

        code = HTTPStatus.OK  # we establish "200" as default
        content_type = "text/html"
        if endpoint == "/":  # THIS FILE IS NOW A TEMPLATE
            context = {
                'genes': GENES
            }
            contents = read_html_template("index2.html").render(context=context)
            code = HTTPStatus.OK
        elif endpoint == "/listSpecies":
            code, contents = list_species(endpoint, parameters)  # we use our function
        elif endpoint == "/karyotype":
            code, contents = karyotype(endpoint, parameters)  # we use our function
        elif endpoint == "/chromosomeLength":
            code, contents = chromosome_length(endpoint, parameters)  # we use our function
        elif endpoint == "/geneSeq":
            code, contents = human_gene(endpoint, parameters)  # we use our function
        elif endpoint == "/geneInfo":
            code, contents = geneInfo(endpoint, parameters)  # we use our function
        else:
            contents = handle_error(endpoint, RESOURCE_NOT_AVAILABLE_ERROR)  # we use our function
            code = HTTPStatus.NOT_FOUND  # we change code to "404"

        self.send_response(code)
        contents_bytes = contents.encode()
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)


with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at PORT...", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()