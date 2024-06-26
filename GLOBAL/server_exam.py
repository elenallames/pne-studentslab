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
    '/geneList': {'resource': "/overlap/region/human", 'params': "content-type=application/json;feature=gene"},
    '/sequence': {'resource': "/sequence/id", 'params': "db_type=otherfeatures;content-type=application/json;" "type=cds;object_type=transcript"}
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


def handle_error(endpoint, message, json_format=False):
    context = {
        'endpoint': endpoint,
        'message': message
    }

    code = HTTPStatus.NOT_FOUND
    if json_format:
        content_type = "application/json"
        contents = json.dumps(context)
    else:
        content_type = "text/html"
        contents = read_html_template("error.html").render(context=context)
    return code, content_type, contents


def list_species(parameters):
    endpoint = '/listSpecies'

    code = None
    content_type = None
    contents = None

    ok = True
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
            code = HTTPStatus.OK
            if 'json' in parameters and parameters['json'][0] == '1':
                content_type = "application/json"
                contents = json.dumps(context)
            else:
                content_type = "text/html"
                contents = read_html_template("species.html").render(context=context)
        else:
            ok = False
    except Exception as e:
        print(f"Error: {e}")
        ok = False
    if not ok:
        code, content_type, contents = handle_error(endpoint, ENDPOINT_ERROR,
                                                    json_format='json' in parameters and parameters['json'][0] == '1')
    return code, content_type, contents


def karyotype(parameters):
    endpoint = '/karyotype'

    code = None
    content_type = None
    contents = None

    ok = True
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
            code = HTTPStatus.OK
            if 'json' in parameters and parameters['json'][0] == '1':
                content_type = "application/json"
                contents = json.dumps(context)
            else:
                content_type = "text/html"
                contents = read_html_template("karyotype.html").render(context=context)
        else:
            ok = False
    except Exception as e:
        print(f"Error: {e}")
        ok = False
    if not ok:
        code, content_type, contents = handle_error(endpoint, ENDPOINT_ERROR, json_format='json' in parameters and parameters['json'][0] == '1')
    return code, content_type, contents


def chromosome_length(parameters):
    endpoint = '/chromosomeLength'

    code = None
    content_type = None
    contents = None

    ok = True
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
            context = {
                'chromosome': chromo,
                'length': length
            }
            code = HTTPStatus.OK
            if 'json' in parameters and parameters['json'][0] == '1':
                content_type = "application/json"
                contents = json.dumps(context)
            else:
                content_type = "text/html"
                contents = read_html_template("chromosomelength.html").render(context=context)
        else:
            ok = False
    except Exception as e:
        print(f"Error: {e}")
        ok = False
    if not ok:
        code, content_type, contents = handle_error(endpoint, ENDPOINT_ERROR, json_format='json' in parameters and parameters['json'][0] == '1')
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

    code = None
    content_type = None
    contents = None

    ok = True
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
                code = HTTPStatus.OK
                if 'json' in parameters and parameters['json'][0] == '1':
                    content_type = "application/json"
                    contents = json.dumps(context)
                else:
                    content_type = "text/html"
                    contents = read_html_template("gene_seq.html").render(context=context)
            else:
                ok = False
        else:
            ok = False
    except Exception as e:
        print(f"Error: {e}")
        ok = False
    if not ok:
        code, content_type, contents = handle_error(endpoint, ENDPOINT_ERROR, json_format='json' in parameters and parameters['json'][0] == '1')
    return code, content_type, contents


def geneInfo(parameters):
    endpoint = '/geneInfo'

    code = None
    content_type = None
    contents = None

    ok = True
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
                code = HTTPStatus.OK
                if 'json' in parameters and parameters['json'][0] == '1':
                    content_type = "application/json"
                    contents = json.dumps(context)
                else:
                    content_type = "text/html"
                    contents = read_html_template("geneinfo.html").render(context=context)
            else:
                ok = False
        else:
            ok = False
    except Exception as e:
        print(f"Error: {e}")
        ok = False
    if not ok:
        code, content_type, contents = handle_error(endpoint, ENDPOINT_ERROR, json_format='json' in parameters and parameters['json'][0] == '1')
    return code, content_type, contents


def geneCalc(parameters):
    endpoint = '/geneCalc'

    code = None
    content_type = None
    contents = None

    ok = True
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
                code = HTTPStatus.OK
                if 'json' in parameters and parameters['json'][0] == '1':
                    content_type = "application/json"
                    contents = json.dumps(context)
                else:
                    content_type = "text/html"
                    contents = read_html_template("gene_calc.html").render(context=context)
            else:
                ok = False
        else:
            ok = False
    except Exception as e:
        print(f"Error: {e}")
        ok = False
    if not ok:
        code, content_type, contents = handle_error(endpoint, ENDPOINT_ERROR, json_format='json' in parameters and parameters['json'][0] == '1')
    return code, content_type, contents


def geneList(parameters):
    endpoint = '/geneList'

    code = None
    content_type = None
    contents = None

    ok = True
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
            code = HTTPStatus.OK
            if 'json' in parameters and parameters['json'][0] == '1':
                content_type = "application/json"
                contents = json.dumps(context)
            else:
                content_type = "text/html"
                contents = read_html_template("genelist.html").render(context=context)
        else:
            ok = False
    except Exception as e:
        print(f"Error: {e}")
        ok = False
    if not ok:
        code, content_type, contents = handle_error(endpoint, ENDPOINT_ERROR, json_format='json' in parameters and parameters['json'][0] == '1')
    return code, content_type, contents


def sequence(parameters):
    endpoint = "/sequence"

    code = None
    content_type = None
    contents = None

    ok = True
    try:
        id = parameters['id'][0]
        species = parameters['species'][0]
        even_bases = 'even_bases' in parameters
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}/{id}?{request['params']};species={species}"
        print(url)
        error, data = server_request(EMSEMBL_SERVER, url)
        if not error:
            # print(f"Data: {data}")
            print(f"Bases: {data['seq']}")
            bases = data['seq']
            s = Seq(bases)
            context = {
                'id': id,
                'species': species,
                'even_bases': even_bases,
                'bases': str(s),
                'length': s.len(),
                'is_even': s.len() % 2 == 0
            }
            code = HTTPStatus.OK
            if 'json' in parameters and parameters['json'][0] == '1':
                content_type = "application/json"
                contents = json.dumps(context)
            else:
                content_type = "text/html"
                contents = read_html_template("sequence.html").render(context=context)

        else:
            ok = False
    except Exception as e:
        print(f"Error: {e}")
        ok = False
    if not ok:
        code, content_type, contents = handle_error(endpoint, ENDPOINT_ERROR, json_format='json' in parameters and parameters['json'][0] == '1')
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
        elif endpoint == "/sequence":
            code, content_type, contents = sequence(parameters)
        else:
            code, content_type, contents = (
                handle_error(endpoint,
                             RESOURCE_NOT_AVAILABLE_ERROR,
                             'json' in parameters and parameters['json'][0] == '1'))

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
