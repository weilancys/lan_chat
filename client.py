import socket
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext
from frame import MessageFrame

SERVER = 'localhost'
PORT = 7777

class Window(tk.Tk):
    def __init_ui(self):
        self.title("LAN Chat")

        self.frame_messages = ttk.Frame(self)
        self.frame_input = ttk.Frame(self)

        self.message_display = tk.scrolledtext.ScrolledText(self.frame_messages)
        self.message_display.pack()
        self.message_input = ttk.Entry(self.frame_input)
        self.message_input.pack() 
        self.btn_send = ttk.Button(self.frame_input, text="Send", command=self.on_btn_send_click)
        self.btn_send.pack()

        self.frame_messages.pack()
        self.frame_input.pack()

    def __init__(self):
        super().__init__()
        self.__init_ui()
        self.connect_to_server()
        self.after(300, self.dispatch_recv_job)
    
    def connect_to_server(self):
        sock = socket.socket()
        try:
            sock.connect((SERVER, PORT))
            self.title("LAN Chat - Connected")
            self.sock = sock
            self.sock.setblocking(False)
        except:
            self.title("LAN Chat - Not Connected")
            self.sock = None

    def start(self):
        self.mainloop()
    
    def dispatch_recv_job(self):
        if self.sock:
            try:
                msg = self.sock.recv(1024)
                msg = msg.decode('utf-8')
                self.message_display.insert(tk.INSERT, msg)
            except:
                pass
            finally:
                self.after(300, self.dispatch_recv_job)

    def on_btn_send_click(self):
        msg = self.message_input.get()
        if msg:
            if self.sock:
                # msg = msg.strip() + "\n"
                MSG = MessageFrame(msg)
                self.sock.sendall(MSG.get_bin())
            self.message_input.delete(0, tk.END)


if __name__ == "__main__":
    window = Window()
    window.start()