import struct

ENCODING = 'utf-8'

# frame start
FS = b"LB_S"
FE = b"LB_E"

HEADER_FORMAT = "!4s2sI256sI"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

PROTOCOL_VERSION = {
    "0.1": b"01",
}

TYPE = {
    'Chat Message': 1,
}

"""
frame structure:

- start flag - 4 bytes
- header
    - protocol version - 2 bytes
    - type - 4 bytes
    - arg - 256 bytes
    - length - 4 bytes
- payload
"""

class Frame:
    def __init__(self, type, args, payload, version=PROTOCOL_VERSION["0.1"]):
        self.version = version
        self.type = type
        self.args = args
        self.header_length = struct.calcsize(HEADER_FORMAT)
        self.payload = payload
        self.payload_length = len(self.payload)
        self.FORMAT = f"{HEADER_FORMAT}{self.payload_length}s"

    def get_header_size(self):
        return self.header_length

    def get_size(self):
        return struct.calcsize(self.FORMAT)
    
    def get_bin(self):
        # return the packed binary representation of this frame
        frame = struct.pack(self.FORMAT, FS, self.version, self.type, self.args, self.payload_length, self.payload)
        return frame


class MessageFrame(Frame):
    def __init__(self, msg):
        super().__init__(TYPE['Chat Message'], b"", msg.encode('utf-8'))


if __name__ == "__main__":
    msg = "my name is lightblue"
    frame = MessageFrame(msg)
    b = frame.get_bin()
    print("bin:", b)
    print("FORMAT:", frame.FORMAT)
    print("size should be:", frame.get_size())
    print("actual size:", len(b))
    print("header length:", frame.get_header_size())