import http.server
import socketserver
import termcolor
from pathlib import Path
import jinja2 as j
from urllib.parse import parse_qs, urlparse
from Seq0 import seq_reverse, seq_complement, seq_len, seq_count

# Define the Server's port
PORT = 8081

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inherits all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # Open the form1.html file
        # Read the index from the file

        def read_html_file(filename):
            contents = Path("html/" + filename).read_text()
            contents = j.Template(contents)
            return contents

        def get_info(sequence):
            text = "Sequence: " + sequence + "<p>" + "Total length: " + str(seq_len(sequence)) + "<p>"
            dict1 = seq_count(sequence)
            for e in dict1:
                index = e + ": "
                percentage = (dict1[e] / seq_len(sequence)) * 100
                percentage = "(" + str(round(percentage, 2)) + "%)"
                text += "<p>" + index + str(dict1[e]) + percentage + "<p>"
            return text

        url_path = urlparse(self.path)
        path = url_path.path  # we get it from here
        arguments = parse_qs(url_path.query)

        SEQUENCES = ["AAACCGTA", "GATA", "AACGT", "CCTGC", "ACGTACGT"]
        keys = ["U5", "ADA", "FRAT1", "RNU6_269P", "FXN"]
        values = []
        for e in keys:
            filename = "Sequences/" + e + ".txt"
            gene = Path(filename).read_text()
            gene = gene[gene.find("\n"):]
            values.append(gene)
        dict1 = dict(zip(keys, values))

        if path == "/":
            contents = Path("html/index.html").read_text()
        elif path == "/ping":
            contents = Path("html/ping.html").read_text()
        elif path == "/get":
            number = arguments["s"][0]
            text = SEQUENCES[int(number)]
            contents = read_html_file("get.html").render(context={"todisplay": text})
        elif path == "/gene":
            key = arguments["g"][0]
            text = dict1[key]
            contents = read_html_file("gene.html").render(context={"todisplay": text})
        elif path == "/operation":
            key = arguments["op"][0]
            if key == "Info":
                text = arguments["operation"][0]
                text2 = "Info"
                text3 = get_info(arguments["operation"][0])
            elif key == "Comp":
                text = arguments["operation"][0]
                text2 = "Comp"
                text3 = seq_complement(arguments["operation"][0])
            else:
                text = arguments["operation"][0]
                text2 = "Rev"
                text3 = seq_reverse(arguments["operation"][0], None)
            contents = read_html_file("operation.html").render(
                context={"todisplay": text, "todisplay2": text2, "todisplay3": text3})
        else:
            contents = Path("html/error.html").read_text()
        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(str.encode(contents))))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
