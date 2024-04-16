import http.server
import socketserver

# -- This is for preventing the error: "Port already in use", works like:
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) , but now we put it in a better way
socketserver.TCPServer.allow_reuse_address = True
# equal to True means we are reusing the socketserver


# -- Use the http.server Handler
handler = http.server.SimpleHTTPRequestHandler  # = simple http request handler
# stores the name of the class whose object will be in charge of handling the http requests received by the server
# will only process http received from clients to the server, but ONLY performs SIMPLE functions


# -- Open the socket server (creates the server socket, does a bind and creates an object to handle http requests)
with socketserver.TCPServer(("", PORT), handler) as httpd:  # d states for "Demon"
    # "with" creates a context, and with "as" we introduce the variable
    # socketserver is a module, TCPServer is a class, and we put () to call the init of this class TO CREATE AN OBJECT
    # we pass to this constructor the server_address and the handler(object) that accepts the conexions & process http

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new clint, the handler is called
    try:
        httpd.serve_forever()  # would act as a while true, accept, processing and closing of connexion
    except KeyboardInterrupt:
        print("Server Stopped!")
        httpd.server_close()
