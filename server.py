from socketserver import StreamRequestHandler, ThreadingTCPServer
import frame
import struct

HOST = 'localhost'
PORT = 7777

clients = set()

class MyHandler(StreamRequestHandler):
    def handle(self):
        clients.add(self)
        while True:
            # msg = None
            try:
                header = self.rfile.read(frame.HEADER_SIZE)
                if not header:
                    break
                if not header.startswith(frame.FS):
                    continue
                FS, version, type_, arg, length = struct.unpack(frame.HEADER_FORMAT, header)
                msg = self.rfile.read(length)
                if not msg:
                    break
            except ConnectionResetError as ex:
                print(ex)
                break
            print(f"{self.client_address} says {msg}")
            for client in clients:
                if client is not self.connection:
                    client.connection.sendall(msg)
        print(f"{self.client_address} disconnected.")
        clients.remove(self)
        

with ThreadingTCPServer((HOST, PORT), MyHandler) as server:
    server.serve_forever()