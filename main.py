from HTTP import Http

Host = '127.0.0.1'
port = 8888
server = Http.Http(Host, port)

@server.route("/cal")
def calculator(a,b):
    return int(a)+int(b)
    

server.runServer()