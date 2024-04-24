import http.server
from http import HTTPStatus   # another way to determine status
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import jinja2
import os
from Seq import Seq


PORT = 8080
HTML_FOLDER = "html"
SEQUENCES = ["CATGA", "TTACG", "AAAAA", "CGCGC", "TATAT"]
GENES = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]
OPERATIONS = ["info", "comp", "rev"]


def read_html_template(file_name):  # receives the name of a file, and we create the path to that file
    file_path = os.path.join(HTML_FOLDER, file_name)
    contents = Path(file_path).read_text()  # create an object (str) of call Path and if it exists it will read it
    contents = jinja2.Template(contents)  # give Template the variable contents and state that our web page is dynamic
    return contents  # returns the object of class Template which will work when using "render"


def handle_get(arguments):  # arguments= dict with the arguments that the server has received from the client
    try:
        sequence_number = int(arguments['sequence_number'][0])  # number of sequence that the user has selected
        # as the value received is a list, we need to access to the 0 position (in this case we receive ONE str value)
        contents = read_html_template("get.html")
        context = {'number': sequence_number, 'sequence': SEQUENCES[sequence_number]}  # I access to the seq of the list
        contents = contents.render(context=context)
        code = HTTPStatus.OK  # integer 200
    except (KeyError, IndexError, ValueError):
        file_path = os.path.join(HTML_FOLDER, "error.html")
        contents = Path(file_path).read_text()
        code = HTTPStatus.NOT_FOUND  # integer 404
    return contents, code  # always executed


socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)
        resource = parsed_url.path  # path
        print(f"Resource: {resource}")
        arguments = parse_qs(parsed_url.query)
        print(f"Arguments: {arguments}")

        code = HTTPStatus.OK
        if resource == "/":  # or resource == "/index.html":  # MAIN WEB PAGE IS A TEMPLATE SINCE IT HAS DYNAMIC PART
            contents = read_html_template("index.html")
            context = {'n_sequences': len(SEQUENCES), 'genes': GENES}
            contents = contents.render(context=context)
            # render = update, it is a str once it has rendered since everything that had to be changed is done
        elif resource == "/ping":  # here we don't build a template since it doesn't have a variable part
            file_path = os.path.join(HTML_FOLDER, "ping.html")
            contents = Path(file_path).read_text()
        elif resource == "/get":
            contents, code = handle_get(arguments)  # the handle_get function returns two values, a duple
            # content=str web page sent as a response from server and the code=status code integer
        elif resource == "/gene":
            try:
                gene_name = arguments['gene_name'][0]
                contents = read_html_template("gene.html")
                file_name = os.path.join("..", "sequences", gene_name + ".txt.fa")
                s = Seq()  # null sequence
                s.read_fasta(file_name)  # we give the objet a value
                context = {'gene_name': gene_name, 'sequence': str(s)}  # __str__ method is called
                contents = contents.render(context=context)
            except (KeyError, IndexError, FileNotFoundError):
                file_path = os.path.join(HTML_FOLDER, "error.html")
                contents = Path(file_path).read_text()
                code = HTTPStatus.NOT_FOUND
        elif resource == "/operation":
            try:
                bases = arguments['bases'][0]
                op = arguments['op'][0]  # we could use lower() and make it in lower case if the user changes url
                contents = read_html_template("operation.html")
                s = Seq(bases)  # object of the class Seq that contains the seq given by the user. COULD BE CONTROLLED
                if op in OPERATIONS:
                    if op == "info":
                        result = s.info().replace("\n", "<br><br>")  # as we are in html we change the line break
                    elif op == "comp":
                        result = s.complement()
                    else:  # elif op == "rev":
                        result = s.reverse()
                    context = {'sequence': str(s), 'op': op, 'result': result}
                    contents = contents.render(context=context)
                else:
                    file_path = os.path.join(HTML_FOLDER, "error.html")
                    contents = Path(file_path).read_text()
                    code = HTTPStatus.NOT_FOUND
            except (KeyError, IndexError):
                file_path = os.path.join(HTML_FOLDER, "error.html")
                contents = Path(file_path).read_text()
                code = HTTPStatus.NOT_FOUND
        else:
            file_path = os.path.join(HTML_FOLDER, "error.html")
            contents = Path(file_path).read_text()
            code = HTTPStatus.NOT_FOUND

        self.send_response(code)
        contents_bytes = contents.encode()
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)


# MAIN PROGRAM
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at PORT...", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()