from socketserver import BaseRequestHandler, StreamRequestHandler, ThreadingTCPServer
import frame
import struct

HOST = '0.0.0.0'
PORT = 7777

clients = set()

class MyHandler(StreamRequestHandler):
    def handle(self):
        clients.add(self)
        while True:
            try:
                header = self.rfile.read(frame.HEADER_SIZE)
                if not header:
                    break
                if not header.startswith(frame.FS):
                    continue
                FS, version, type_, arg, length = struct.unpack(frame.HEADER_FORMAT, header)

                payload = self.rfile.read(length)
                if not payload:
                    break

                if version == frame.PROTOCOL_VERSION["0.1"]:
                    if type_ == frame.TYPE['Chat Message']:
                        message = payload.decode(frame.ENCODING)
                        print(f"{self.client_address} says {message}")
                        for client in clients:
                            if client is not self.connection:
                                client.connection.sendall(message.encode())
                    else:
                        raise NotImplementedError("other types not implemented.")                  
                else:
                    raise NotImplementedError("other protocol versions not implemented.")
            except NotImplementedError as ex:
                print(ex)
                break
            except ConnectionResetError as ex:
                print(ex)
                break
            
        print(f"{self.client_address} disconnected.")
        clients.remove(self)


class LanChatServer(ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate: bool = True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    def server_activate(self):
        super().server_activate()
        print(f"lan chat server is listening on {self.server_address[0]}:{self.server_address[1]}")        


with LanChatServer((HOST, PORT), MyHandler) as server:
    server.serve_forever()