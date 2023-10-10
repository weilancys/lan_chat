from socketserver import StreamRequestHandler, ThreadingTCPServer

HOST = 'localhost'
PORT = 7777
clients = set()


class MyHandler(StreamRequestHandler):
    def handle(self):
        clients.add(self)
        while True:
            msg = self.rfile.readline()
            if not msg:
                break
            print(f"{self.client_address} says {msg}")
            for client in clients:
                if client is not self.connection:
                    client.sendall(msg)
        print(f"{self.client_address} disconnected.")
        

with ThreadingTCPServer((HOST, PORT), MyHandler) as server:
    server.serve_forever()