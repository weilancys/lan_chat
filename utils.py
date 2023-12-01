import socket

def recvall(sock: socket.socket, length: int) -> bytes:
    if length <= 0:
        raise ValueError("invalid length")
    buffer = []
    bytes_recved = 0
    CHUNK_SIZE = 256
    while bytes_recved < length:
        chunk = sock.recv(min(CHUNK_SIZE, length-bytes_recved))
        if not chunk:
            return b""
        bytes_recved += len(chunk)
        buffer.append(chunk)
    return b"".join(buffer)
        