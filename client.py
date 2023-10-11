import socket
import tkinter as tk
from tkinter import ttk

SERVER = 'localhost'
PORT = 7777

# sock = socket.socket()
# sock.connect((SERVER, PORT))

class Window(tk.Tk):
    def __init_ui(self):
        self.title("LAN Chat")

        self.frame_messages = ttk.Frame(self)
        self.frame_input = ttk.Frame(self)

        self.message_display = tk.Text(self.frame_messages)
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

    def start(self):
        self.mainloop()

    def on_btn_send_click(self):
        msg = self.message_input.get()
        if msg:
            msg = msg.strip() + "\n"
            self.message_display.insert(tk.INSERT, msg)
            self.message_display.see(tk.END)
            self.message_input.delete(0, tk.END)
            # print(msg)


if __name__ == "__main__":
    window = Window()
    window.start()