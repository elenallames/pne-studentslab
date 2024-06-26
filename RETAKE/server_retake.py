import http.server
from http import HTTPStatus
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs, quote
import jinja2
import os
import json


PORT = 8081
HTML_FOLDER = "html"
ENSEMBL_SERVER = "rest.ensembl.org"
RESOURCE_TO_ENSEMBL_REQUEST = {
    '/listSpecies': {'resource': "/info/species", 'params': "content-type=application/json"},
    '/karyotype': {'resource': "/info/assembly", 'params': "content-type=application/json"},
    '/chromosomeLength': {'resource': "/info/assembly", 'params': "content-type=application/json"},
    '/geneSeq': {'resource': "/sequence/id", 'params': "content-type=application/json"},
    '/geneInfo': {'resource': "/overlap/id", 'params': "content-type=application/json;feature=gene"},
    '/geneCalc': {'resource': "/sequence/id", 'params': "content-type=application/json"},
    '/geneList': {'resource': "/overlap/region/human", 'params': "content-type=application/json;feature=gene"}
}
RESOURCE_NOT_AVAILABLE = "Resource not available"
ENDPOINT_ERROR = "Ups! Something went wrong"


def read_html_template(file_name):
    file_path = os.path.join(HTML_FOLDER, file_name)
    contents = Path(file_path).read_text()
    return jinja2.Template(contents)


def server_request(server, url):
    import http.client

    connection = http.client.HTTPSConnection(server)
    connection.request("GET", url)
    response = connection.getresponse()
    if response.status == HTTPStatus.OK:
        json_str = response.read().decode()
        return False, json.loads(json_str)
    return True, None


def handle_error(endpoint, message):
    context = {'endpoint': endpoint, 'message': message}
    return read_html_template("error.html").render(context=context)


def get_ensembl_data(endpoint, parameters):
    try:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}?{request['params']}"
        if endpoint in ['/karyotype', '/chromosomeLength']:
            species = quote(parameters['species'][0])
            url = f"{request['resource']}/{species}?{request['params']}"
        if endpoint in ['/chromosomeLength']:
            url = f"{request['resource']}/{quote(species)}?{request['params']}"
            chromo = parameters['chromo'][0]
        return server_request(ENSEMBL_SERVER, url)
    except Exception as e:
        print(f"Error: {e}")
        return True, None


def list_species(parameters):
    endpoint = '/listSpecies'
    error, data = get_ensembl_data(endpoint, parameters)
    if error:
        return HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    limit = int(parameters.get('limit', [len(data['species'])])[0])
    name_species = [specie['display_name'] for specie in data['species'][:limit]]
    context = {'number_of_species': len(data['species']), 'limit': limit, 'name_species': name_species}

    if parameters.get('json', ['0'])[0] == '1':
        return HTTPStatus.OK, "application/json", json.dumps(context)
    return HTTPStatus.OK, "text/html", read_html_template("species.html").render(context=context)


def karyotype(parameters):
    endpoint = '/karyotype'
    error, data = get_ensembl_data(endpoint, parameters)
    if error:
        return HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    species = quote(parameters['species'][0])
    context = {'species': species, 'karyotype': data['karyotype']}

    if parameters.get('json', ['0'])[0] == '1':
        return HTTPStatus.OK, "application/json", json.dumps(context)
    return HTTPStatus.OK, "text/html", read_html_template("karyotype.html").render(context=context)


def chromosome_length(parameters):
    endpoint = '/chromosomeLength'
    error, data = get_ensembl_data(endpoint, parameters)
    if error:
        return HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    species = parameters['species'][0]
    chromo = parameters['chromo'][0]
    length = next((chr['length'] for chr in data['top_level_region'] if chr['name'] == chromo), None)
    context = {'chromosome': chromo, 'length': length}

    if parameters.get('json', ['0'])[0] == '1':
        return HTTPStatus.OK, "application/json", json.dumps(context)
    return HTTPStatus.OK, "text/html", read_html_template("chromosomelength.html").render(context=context)


def get_id(gene):
    resource = f"/homology/symbol/human/{gene}"
    params = 'content-type=application/json;format=condensed'
    url = f"{resource}?{params}"
    error, data = server_request(ENSEMBL_SERVER, url)
    return None if error else data['data'][0]['id']


def geneSeq(parameters):
    endpoint = '/geneSeq'
    gene = parameters['gene'][0]
    gene_id = get_id(gene)

    if gene_id is None:
        return HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    error, data = get_ensembl_data(endpoint, parameters)
    if error:
        return HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    context = {'gene': gene, 'bases': data['seq']}

    if parameters.get('json', ['0'])[0] == '1':
        return HTTPStatus.OK, "application/json", json.dumps(context)
    return HTTPStatus.OK, "text/html", read_html_template("humangene.html").render(context=context)


def geneInfo(parameters):
    endpoint = '/geneInfo'
    gene = parameters['gene'][0]
    gene_id = get_id(gene)

    if gene_id is None:
        return HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    error, data = get_ensembl_data(endpoint, parameters)
    if error:
        return HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    data = data[0]
    context = {
        'gene': gene,
        'start': data['start'],
        'end': data['end'],
        'length': data['end'] - data['start'],
        'id': gene_id,
        'chromosome_name': data['assembly_name']
    }

    if parameters.get('json', ['0'])[0] == '1':
        return HTTPStatus.OK, "application/json", json.dumps(context)
    return HTTPStatus.OK, "text/html", read_html_template("geneinfo.html").render(context=context)


def geneCalc(parameters):
    from seq import Seq
    endpoint = '/geneCalc'
    gene = parameters['gene'][0]
    gene_id = get_id(gene)

    if gene_id is None:
        return HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    error, data = get_ensembl_data(endpoint, parameters)
    if error:
        return HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)
    if not error:
        seq = data['seq']
        s = Seq(seq)
        context = {
            'gene': gene,
            'length': s.len(),
            'infoA': f"{s.count_base('A')} ({round((s.count_base('A') / s.len() * 100), 1)}%)",
            'infoC': f"{s.count_base('C')} ({round((s.count_base('C') / s.len() * 100), 1)}%)",
            'infoG': f"{s.count_base('G')} ({round((s.count_base('G') / s.len() * 100), 1)}%)",
            'infoT': f"{s.count_base('T')} ({round((s.count_base('T') / s.len() * 100), 1)}%)",
        }
    code = 200

    if parameters.get('json', ['0'])[0] == '1':
        return HTTPStatus.OK, "application/json", json.dumps(context)
    return HTTPStatus.OK, "text/html", read_html_template("genecalculations.html").render(context=context)


def geneList(parameters):
    endpoint = '/geneList'
    chromo = parameters['chromo'][0]
    start = int(parameters['start'][0])
    end = int(parameters['end'][0])
    url = f"{RESOURCE_TO_ENSEMBL_REQUEST[endpoint]['resource']}/{chromo}:{start}-{end}?{RESOURCE_TO_ENSEMBL_REQUEST[endpoint]['params']}"
    error, data = server_request(ENSEMBL_SERVER, url)
    if error:
        return HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    names = [gene['external_name'] for gene in data if 'external_name' in gene]
    context = {'names': names}

    if parameters.get('json', ['0'])[0] == '1':
        return HTTPStatus.OK, "application/json", json.dumps(context)
    return HTTPStatus.OK, "text/html", read_html_template("genelist.html").render(context=context)


socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path
        parameters = parse_qs(parsed_url.query)

        handlers = {
            "/": lambda: (HTTPStatus.OK, "text/html", Path(os.path.join(HTML_FOLDER, "index.html")).read_text()),
            "/listSpecies": lambda: list_species(parameters),
            "/karyotype": lambda: karyotype(parameters),
            "/chromosomeLength": lambda: chromosome_length(parameters),
            "/geneSeq": lambda: geneSeq(parameters),
            "/geneInfo": lambda: geneInfo(parameters),
            "/geneCalc": lambda: geneCalc(parameters),
            "/geneList": lambda: geneList(parameters),
        }

        code, content_type, contents = handlers.get(endpoint, lambda: (
            HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, RESOURCE_NOT_AVAILABLE)))()
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(contents.encode())))
        self.end_headers()
        self.wfile.write(contents.encode())


with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"Serving at PORT {PORT}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()
