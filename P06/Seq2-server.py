import http.server
from http import HTTPStatus
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import jinja2
import os
from seq import Seq

PORT = 8080
HTML_FOLDER = "html"
SEQUENCES = ["CATGA", "TTACG", "AAAAA", "CGCGC", "TATAT"]
GENES = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]
OPERATIONS = ["info", "comp", "rev"]


def read_html_template(file_name):
    """Reads and returns the HTML template content."""
    file_path = os.path.join(HTML_FOLDER, file_name)
    contents = Path(file_path).read_text()
    template = jinja2.Template(contents)
    return template


def handle_get(arguments):
    """Handles the GET operation for sequences."""
    try:
        sequence_number = int(arguments['sequence_number'][0])
        template = read_html_template("get.html")
        context = {'number': sequence_number, 'sequence': SEQUENCES[sequence_number]}
        contents = template.render(context=context)
        code = HTTPStatus.OK
    except (KeyError, IndexError, ValueError):
        template = read_html_template("error.html")
        contents = template.render()
        code = HTTPStatus.NOT_FOUND
    return contents, code


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        parsed_url = urlparse(self.path)
        resource = parsed_url.path
        arguments = parse_qs(parsed_url.query)

        print(f"Resource: {resource}")
        print(f"Arguments: {arguments}")

        code = HTTPStatus.OK
        contents = ""

        if resource == "/":
            template = read_html_template("index.html")
            context = {'n_sequences': len(SEQUENCES), 'genes': GENES}
            contents = template.render(context=context)
        elif resource == "/ping":
            template = read_html_template("ping.html")
            contents = template.render()
        elif resource == "/get":
            contents, code = handle_get(arguments)
        elif resource == "/gene":
            contents, code = self.handle_gene(arguments)
        elif resource == "/operation":
            contents, code = self.handle_operation(arguments)
        else:
            template = read_html_template("error.html")
            contents = template.render()
            code = HTTPStatus.NOT_FOUND

        self.respond(contents, code)

    def handle_gene(self, arguments):
        """Handles the GENE operation."""
        try:
            gene_name = arguments['gene_name'][0]
            template = read_html_template("gene.html")
            file_name = os.path.join("..", "sequences", f"{gene_name}.txt.fa")
            s = Seq()
            s.read_fasta(file_name)
            context = {'gene_name': gene_name, 'sequence': str(s)}
            contents = template.render(context=context)
            code = HTTPStatus.OK
        except (KeyError, IndexError, FileNotFoundError):
            template = read_html_template("error.html")
            contents = template.render()
            code = HTTPStatus.NOT_FOUND
        return contents, code

    def handle_operation(self, arguments):
        try:
            bases = arguments['bases'][0]
            op = arguments['op'][0]
            template = read_html_template("operation.html")
            s = Seq(bases)

            if op in OPERATIONS:
                result = self.perform_operation(s, op)
                context = {'sequence': str(s), 'op': op, 'result': result}
                contents = template.render(context=context)
                code = HTTPStatus.OK
            else:
                raise KeyError
        except (KeyError, IndexError):
            template = read_html_template("error.html")
            contents = template.render()
            code = HTTPStatus.NOT_FOUND
        return contents, code

    def perform_operation(self, seq_obj, operation):
        """Performs the specified operation on the sequence object."""
        if operation == "info":
            return seq_obj.info().replace("\n", "<br><br>")
        elif operation == "comp":
            return seq_obj.complement()
        elif operation == "rev":
            return seq_obj.reverse()

    def respond(self, contents, code):
        """Sends the HTTP response back to the client."""
        self.send_response(code)
        contents_bytes = contents.encode()
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()
        self.wfile.write(contents_bytes)


def main():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Serving at PORT {PORT}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped by the user")
            httpd.server_close()


if __name__ == "__main__":
    main()
