from socketserver import StreamRequestHandler, ThreadingTCPServer

HOST = 'localhost'
PORT = 7777

clients = set()

class MyHandler(StreamRequestHandler):
    def handle(self):
        clients.add(self)
        while True:
            msg = None
            try:
                msg = self.rfile.readline()
            except ConnectionResetError as ex:
                print(ex)
                break
            if not msg:
                break
            print(f"{self.client_address} says {msg}")
            for client in clients:
                if client is not self.connection:
                    client.connection.sendall(msg)
        print(f"{self.client_address} disconnected.")
        clients.remove(self)
        

with ThreadingTCPServer((HOST, PORT), MyHandler) as server:
    server.serve_forever()