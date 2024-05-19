import http.server
from http import HTTPStatus
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs, quote
import jinja2
import os
import json
from seq import Seq


PORT = 8081
HTML_FOLDER = "html"
EMSEMBL_SERVER = "rest.ensembl.org"
RESOURCE_TO_ENSEMBL_REQUEST = {
    '/listSpecies': {'resource': "/info/species", 'params': "content-type=application/json"},
    '/karyotype': {'resource': "/info/assembly", 'params': "content-type=application/json"},
    '/chromosomeLength': {'resource': "/info/assembly", 'params': "content-type=application/json"},
    '/geneSeq': {'resource': "/sequence/id", 'params': "content-type=application/json"},
    '/geneInfo': {'resource': "/overlap/id", 'params': "content-type=application/json;feature=gene"},
    '/geneCalc': {'resource': "/sequence/id", 'params': "content-type=application/json"},
    '/geneList': {'resource': "/overlap/region/human", 'params': "content-type=application/json;feature=gene"}
}
RESOURCE_NOT_AVAILABLE_ERROR = "Resource not available"
ENDPOINT_ERROR = "Ups! Something went wrong"


def read_html_template(file_name):
    file_path = os.path.join(HTML_FOLDER, file_name)
    contents = Path(file_path).read_text()
    contents = jinja2.Template(contents)
    return contents


def server_request(server, url):
    import http.client

    error = False
    data = None
    connection = http.client.HTTPSConnection(server)
    connection.request("GET", url)
    response = connection.getresponse()
    if response.status == HTTPStatus.OK:
        json_str = response.read().decode()
        data = json.loads(json_str)
    else:
        error = True
    return error, data


def handle_error(endpoint, message):
    context = {
        'endpoint': endpoint,
        'message': message
    }
    return read_html_template("error.html").render(context=context)


def list_species(parameters):
    endpoint = '/listSpecies'

    code = HTTPStatus.NOT_FOUND
    content_type = "text/html"
    contents = handle_error(endpoint, ENDPOINT_ERROR)

    try:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}?{request['params']}"
        error, data = server_request(EMSEMBL_SERVER, url)
        if not error:
            limit = None
            if 'limit' in parameters:
                limit = int(parameters['limit'][0])
            species = data['species']  # list<dict>
            name_species = []
            for specie in species[:limit]:
                name_species.append(specie['display_name'])
            context = {
                'number_of_species': len(species),
                'limit': limit,
                'name_species': name_species
            }
            if 'json' in parameters and parameters['json'][0] == '1':
                content_type = "application/json"
                contents = json.dumps(context)
            else:
                content_type = "text/html"
                contents = read_html_template("species.html").render(context=context)
            code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")
    return code, content_type, contents


def karyotype(parameters):
    endpoint = '/karyotype'

    code = HTTPStatus.NOT_FOUND
    content_type = "text/html"
    contents = handle_error(endpoint, ENDPOINT_ERROR)

    try:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        species = quote(parameters['species'][0])
        url = f"{request['resource']}/{species}?{request['params']}"
        error, data = server_request(EMSEMBL_SERVER, url)
        if not error:
            context = {
                'species': species,
                'karyotype': data['karyotype']
            }
            if 'json' in parameters and parameters['json'][0] == '1':
                content_type = "application/json"
                contents = json.dumps(context)
            else:
                content_type = "text/html"
                contents = read_html_template("karyotype.html").render(context=context)
            code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")
    return code, content_type, contents


def chromosome_length(parameters):
    endpoint = '/chromosomeLength'

    code = HTTPStatus.NOT_FOUND
    content_type = "text/html"
    contents = handle_error(endpoint, ENDPOINT_ERROR)

    try:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        species = parameters['species'][0]
        chromo = parameters['chromo'][0]
        url = f"{request['resource']}/{species}?{request['params']}"
        error, data = server_request(EMSEMBL_SERVER, url)
        if not error:
            print(data)
            chromosomes = data['top_level_region']
            length = None
            found = False
            i = 0
            while not found and i < len(chromosomes):
                chromosome = chromosomes[i]
                if chromosome['name'] == chromo:
                    length = chromosome['length']
                    found = True
                i += 1
            # for chromosome in chromosomes:
            #     if chromosome['name'] == chromo:
            #         length = chromosome['length']
            #         break
            context = {
                'chromosome': chromo,
                'length': length
            }
            if 'json' in parameters and parameters['json'][0] == '1':
                content_type = "application/json"
                contents = json.dumps(context)
            else:
                content_type = "text/html"
                contents = read_html_template("chromosome_length.html").render(context=context)
            code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")
    return code, content_type, contents


def get_id(gene):
    resource = "/homology/symbol/human/" + gene
    params = 'content-type=application/json;format=condensed'
    url = f"{resource}?{params}"
    error, data = server_request(EMSEMBL_SERVER, url)
    gene_id = None
    if not error:
        gene_id = data['data'][0]['id'] 
    return gene_id


def geneSeq(parameters):
    endpoint = '/geneSeq'

    code = HTTPStatus.NOT_FOUND
    content_type = "text/html"
    contents = handle_error(endpoint, ENDPOINT_ERROR)

    try:
        gene = parameters['gene'][0]
        gene_id = get_id(gene)
        print(f"Gene: {gene} - Gene ID: {gene_id}")
        if gene_id is not None:
            request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
            url = f"{request['resource']}/{gene_id}?{request['params']}"
            error, data = server_request(EMSEMBL_SERVER, url)
            if not error:
                bases = data['seq']
                context = {
                    'gene': gene,
                    'bases': bases
                }
                if 'json' in parameters and parameters['json'][0] == '1':
                    content_type = "application/json"
                    contents = json.dumps(context)
                else:
                    content_type = "text/html"
                    contents = read_html_template("gene_seq.html").render(context=context)
                code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")
    return code, content_type, contents


def geneInfo(parameters):
    endpoint = '/geneInfo'

    code = HTTPStatus.NOT_FOUND
    content_type = "text/html"
    contents = handle_error(endpoint, ENDPOINT_ERROR)

    try:
        gene = parameters['gene'][0]
        gene_id = get_id(gene)
        print(f"Gene: {gene} - Gene ID: {gene_id}")
        if gene_id is not None:
            request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
            url = f"{request['resource']}/{gene_id}?{request['params']}"
            error, data = server_request(EMSEMBL_SERVER, url)
            if not error:
                data = data[0]
                start = data['start']
                end = data['end']
                length = end - start
                id = gene_id
                chromosome_name = data['assembly_name']
                context = {
                    'gene': gene,
                    'start': start,
                    'end': end,
                    'length': length,
                    'id': id,
                    'chromosome_name': chromosome_name
                }
                if 'json' in parameters and parameters['json'][0] == '1':
                    content_type = "application/json"
                    contents = json.dumps(context)
                else:
                    content_type = "text/html"
                    contents = read_html_template("gene_info.html").render(context=context)
                code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")
    return code, content_type, contents


def geneCalc(parameters):
    endpoint = '/geneCalc'

    code = HTTPStatus.NOT_FOUND
    content_type = "text/html"
    contents = handle_error(endpoint, ENDPOINT_ERROR)

    try:
        gene = parameters['gene'][0]
        gene_id = get_id(gene)
        print(f"Gene: {gene} - Gene ID: {gene_id}")
        if gene_id is not None:
            request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
            url = f"{request['resource']}/{gene_id}?{request['params']}"
            error, data = server_request(EMSEMBL_SERVER, url)
            if not error:
                bases = data['seq']
                s = Seq(bases)
                context = {
                    'gene': gene,
                    'length': s.len(),
                    'info': s.info()
                }
                if 'json' in parameters and parameters['json'][0] == '1':
                    content_type = "application/json"
                    contents = json.dumps(context)
                else:
                    content_type = "text/html"
                    contents = read_html_template("gene_calc.html").render(context=context)
                code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")
    return code, content_type, contents


def geneList(parameters):
    endpoint = '/geneList'

    code = HTTPStatus.NOT_FOUND
    content_type = "text/html"
    contents = handle_error(endpoint, ENDPOINT_ERROR)

    try:
        chromo = parameters['chromo'][0]
        start = int(parameters['start'][0])
        end = int(parameters['end'][0])
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}/{chromo}:{start}-{end}?{request['params']}"
        error, data = server_request(EMSEMBL_SERVER, url)
        if not error:
            names = []
            for gene in data:
                if 'external_name' in gene:
                    names.append(gene['external_name'])
            context = {
                'names': names,
            }
            if 'json' in parameters and parameters['json'][0] == '1':
                content_type = "application/json"
                contents = json.dumps(context)
            else:
                content_type = "text/html"
                contents = read_html_template("gene_list.html").render(context=context)
            code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")
    return code, content_type, contents


socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path  # resource or path
        print(f"Endpoint: {endpoint}")
        parameters = parse_qs(parsed_url.query)
        print(f"Parameters: {parameters}")

        code = HTTPStatus.OK
        content_type = "text/html"
        if endpoint == "/":
            file_path = os.path.join(HTML_FOLDER, "index.html")
            contents = Path(file_path).read_text()
        elif endpoint == "/listSpecies":
            code, content_type, contents = list_species(parameters)
        elif endpoint == "/karyotype":
            code, content_type, contents = karyotype(parameters)
        elif endpoint == "/chromosomeLength":
            code, content_type, contents = chromosome_length(parameters)
        elif endpoint == "/geneSeq":
            code, content_type, contents = geneSeq(parameters)
        elif endpoint == "/geneInfo":
            code, content_type, contents = geneInfo(parameters)
        elif endpoint == "/geneCalc":
            code, content_type, contents = geneCalc(parameters)
        elif endpoint == "/geneList":
            code, content_type, contents = geneList(parameters)
        else:
            contents = handle_error(endpoint, RESOURCE_NOT_AVAILABLE_ERROR)
            code = HTTPStatus.NOT_FOUND

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
