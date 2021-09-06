import socket

class ProxyRequestHandler():
    def __init__(self, laddr, lport):
        self.lport = lport
        self.laddr = laddr
        self.raddr = None

    def listen(self):
        resp = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.laddr, self.lport))
            s.listen()
            conn, self.raddr = s.accept()
            with conn:
                print(f"Connected to {self.raddr}")
                #while True:
                data = conn.recv(2048)
                # if not data:
                #     break
                resp = self.handleReq(data)
                conn.sendall(resp)
    
    def handleReq(self, data):
        req = self.reqToJSON(data)
        if req == 0:
            return 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((req['host'], 80))
            s.sendall(data)
            resp = s.recv(2048)
        
        return resp
    
    def reqToJSON(self, data):
        req = {}
        chunks = data.decode().split('\r\n')

        chunks[0] = chunks[0].split(' ')
        req['method'] = chunks[0][0]
        if req['method'] != 'GET':
            return 0
        req['path'] = chunks[0][1]
        req['httpv'] = chunks[0][2]

        req['host'] = chunks[1].split(":")[1][1:]
        req['headers'] = {}

        for c in chunks[2:]:
            h = c.split(':')
            if h[0] == '' or h[1] == '':
                continue
            req['headers'][h[0]] = h[1][1:]
        return req