import socket

# 서버키는거, 라우트 매핑, 반환< 이건 해야댐
class Http(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.routers = {}
    def not_found(self):
        return "404 Not Found"
    def route(self, routerName, methods=["GET"]):
        def wraps(f):
            self.routers[routerName.lower()] = {
                "func":f,
                "methods":methods
                }
            return f
        return wraps


    def routerHandler(self, data):
        try:
            func, method = self.routers[data.lower()].values()
        except :
            func = self.not_found
            method = True
        return (func, method)
    def httpDataParser(self,data):
        method = data[0]
        route = data[1].split('?')
        if len(route) > 1:
            route, query = route
            querys = query.split("&")
            query = {}
            for q in querys:
                q=q.split("=")
                query[q[0]]=q[1]
            print(route,"?")
            return {"method":method, "route":route, "query":query}
        else:
            route = route.pop()
        return {"method":method, "route":route, "query":None}

    def request(self, f,data):
         
        if data['query']:
            try:
                data = f(**data['query'])
                return "HTTP/1.1 200 OK\n Content_Type: text/html\n\n"+str(data)
            except:
                return "HTTP/1.1 400 Bad Request\n Content_Type: text/html\n\n"+"Bad Request"
            
        return "HTTP/1.1 400 Bad Request\n Content_Type: text/html\n\n"+str(f())
    def runServer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(True)
            print('RUNNING SERVER')
            while True:
                conn, addr = sock.accept()
                req = str(conn.recv(1024))[2:-1].split()
                # 여기에 뭔가 로직이 들어가는 함수를 하나 만들어 봅시다.
                req = self.httpDataParser(req)
                print(req)
                print(req['route'])
                func, method = self.routerHandler(req['route'])
                req = self.request(func,req)
                conn.sendall(req.encode())
                conn.close()
