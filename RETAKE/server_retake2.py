import http.server
from http import HTTPStatus
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs, quote
import jinja2
import os
import json


# Configuration
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
RESOURCE_NOT_AVAILABLE_ERROR = "Resource not available"
ENDPOINT_ERROR = "Oops! Something went wrong"


def read_html_template(file_name):
    file_path = os.path.join(HTML_FOLDER, file_name)
    contents = Path(file_path).read_text()
    template = jinja2.Template(contents)
    return template


def server_request(server, url):
    import http.client

    connection = http.client.HTTPSConnection(server)
    connection.request("GET", url)
    response = connection.getresponse()
    if response.status == HTTPStatus.OK:
        json_str = response.read().decode()
        data = json.loads(json_str)
        return False, data
    else:
        return True, None


def handle_error(endpoint, message):
    context = {'endpoint': endpoint, 'message': message}
    return read_html_template("error.html").render(context=context)


def list_species(parameters):
    endpoint = '/listSpecies'
    code, content_type, contents = HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    try:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}?{request['params']}"
        error, data = server_request(ENSEMBL_SERVER, url)
        if not error:
            limit = int(parameters.get('limit', [None])[0]) if 'limit' in parameters else None
            species = data['species']
            name_species = [specie['display_name'] for specie in species[:limit]]
            context = {'number_of_species': len(species), 'limit': limit, 'name_species': name_species}
            if parameters.get('json', ['0'])[0] == '1':
                content_type, contents = "application/json", json.dumps(context)
            else:
                content_type, contents = "text/html", read_html_template("species.html").render(context=context)
            code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")

    return code, content_type, contents


def karyotype(parameters):
    endpoint = '/karyotype'
    code, content_type, contents = HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    try:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        species = quote(parameters['species'][0])
        url = f"{request['resource']}/{species}?{request['params']}"
        error, data = server_request(ENSEMBL_SERVER, url)
        if not error:
            context = {'species': species, 'karyotype': data['karyotype']}
            if parameters.get('json', ['0'])[0] == '1':
                content_type, contents = "application/json", json.dumps(context)
            else:
                content_type, contents = "text/html", read_html_template("karyotype.html").render(context=context)
            code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")

    return code, content_type, contents


def chromosome_length(parameters):
    endpoint = '/chromosomeLength'
    code, content_type, contents = HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    try:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        species = parameters['species'][0]
        chromo = parameters['chromo'][0]
        url = f"{request['resource']}/{species}?{request['params']}"
        error, data = server_request(ENSEMBL_SERVER, url)
        if not error:
            chromosomes = data['top_level_region']
            length = next((chromosome['length'] for chromosome in chromosomes if chromosome['name'] == chromo), None)
            context = {'chromosome': chromo, 'length': length}
            if parameters.get('json', ['0'])[0] == '1':
                content_type, contents = "application/json", json.dumps(context)
            else:
                content_type, contents = "text/html", read_html_template("chromosomelength.html").render(context=context)
            code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")

    return code, content_type, contents


def get_id(gene):
    resource = f"/homology/symbol/human/{gene}"
    params = 'content-type=application/json;format=condensed'
    url = f"{resource}?{params}"
    error, data = server_request(ENSEMBL_SERVER, url)
    if not error:
        return data['data'][0]['id']
    return None


def gene_seq(parameters):
    endpoint = '/geneSeq'
    code, content_type, contents = HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    try:
        gene = parameters['gene'][0]
        gene_id = get_id(gene)
        if gene_id:
            request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
            url = f"{request['resource']}/{gene_id}?{request['params']}"
            error, data = server_request(ENSEMBL_SERVER, url)
            if not error:
                context = {'gene': gene, 'bases': data['seq']}
                if parameters.get('json', ['0'])[0] == '1':
                    content_type, contents = "application/json", json.dumps(context)
                else:
                    content_type, contents = "text/html", read_html_template("humangene.html").render(context=context)
                code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")

    return code, content_type, contents


def gene_info(parameters):
    endpoint = '/geneInfo'
    code, content_type, contents = HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    try:
        gene = parameters['gene'][0]
        gene_id = get_id(gene)
        if gene_id:
            request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
            url = f"{request['resource']}/{gene_id}?{request['params']}"
            error, data = server_request(ENSEMBL_SERVER, url)
            if not error:
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
                    content_type, contents = "application/json", json.dumps(context)
                else:
                    content_type, contents = "text/html", read_html_template("geneinfo.html").render(context=context)
                code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")

    return code, content_type, contents


def gene_calc(parameters):
    from seq import Seq
    endpoint = '/geneCalc'
    code, content_type, contents = HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    try:
        gene = parameters['gene'][0]
        gene_id = get_id(gene)
        if gene_id:
            request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
            url = f"{request['resource']}/{gene_id}?{request['params']}"
            error, data = server_request(ENSEMBL_SERVER, url)
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
                if parameters.get('json', ['0'])[0] == '1':
                    content_type, contents = "application/json", json.dumps(context)
                else:
                    content_type, contents = "text/html", read_html_template("genecalculations.html").render(context=context)
                code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")

    return code, content_type, contents


def gene_list(parameters):
    endpoint = '/geneList'
    code, content_type, contents = HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, ENDPOINT_ERROR)

    try:
        chromo = parameters['chromo'][0]
        start, end = int(parameters['start'][0]), int(parameters['end'][0])
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}/{chromo}:{start}-{end}?{request['params']}"
        error, data = server_request(ENSEMBL_SERVER, url)
        if not error:
            names = [gene['external_name'] for gene in data if 'external_name' in gene]
            context = {'names': names}
            if parameters.get('json', ['0'])[0] == '1':
                content_type, contents = "application/json", json.dumps(context)
            else:
                content_type, contents = "text/html", read_html_template("genelist.html").render(context=context)
            code = HTTPStatus.OK
    except Exception as e:
        print(f"Error: {e}")

    return code, content_type, contents


socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path
        parameters = parse_qs(parsed_url.query)

        code, content_type, contents = HTTPStatus.OK, "text/html", None

        if endpoint == "/":
            file_path = os.path.join(HTML_FOLDER, "index.html")
            contents = Path(file_path).read_text()
        elif endpoint in RESOURCE_TO_ENSEMBL_REQUEST:
            handler = {
                "/listSpecies": list_species,
                "/karyotype": karyotype,
                "/chromosomeLength": chromosome_length,
                "/geneSeq": gene_seq,
                "/geneInfo": gene_info,
                "/geneCalc": gene_calc,
                "/geneList": gene_list,
            }.get(endpoint)
            code, content_type, contents = handler(parameters) if handler else (HTTPStatus.NOT_FOUND, "text/html", handle_error(endpoint, RESOURCE_NOT_AVAILABLE_ERROR))
        else:
            contents = handle_error(endpoint, RESOURCE_NOT_AVAILABLE_ERROR)
            code = HTTPStatus.NOT_FOUND

        self.send_response(code)
        contents_bytes = contents.encode()
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()
        self.wfile.write(contents_bytes)


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Serving at PORT {PORT}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped by the user")
            httpd.server_close()
