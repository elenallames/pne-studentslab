import http.server
import socketserver
import termcolor

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

        # IN this simple server version:
        # We are NOT processing the client's request
        # It is a happy server: It always returns a message saying
        # that everything is ok

        # Message to send back to the client
        contents = "I am the happy server! :-)"

        # Generating the response message
        self.send_response(200)  # -- Status line: OK! # es un subprograma que nos viene heredado de la clase http handler # establece cual es el codigo

        # Define the content-type header:
        self.send_header('Content-Type', 'text/plain')  # de la cabecera del content type
        self.send_header('Content-Length', len(contents.encode()))

        # The header is finished
        self.end_headers()  # añade la line blanca

        # Send the response message
        self.wfile.write(contents.encode())  # envia de vuelta el contenido (en este caso texto plano)

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
        print("Stoped by the user")
        httpd.server_close()
