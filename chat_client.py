import socket
import threading
import time
import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter import ttk

# Socket setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 9999


class ChatClient:
    def __init__(self):
        self.root = Tk()
        self.build_ui(self.root)

        self.msg_field = None
        self.entry_box = None

    def build_ui(self, root):
        root.title("Chat Client")

        frame = ttk.Frame(root, padding=10)
        frame.grid(row=0, column=0, sticky='e')

        launch_btn = Button(frame, text="Connect service", command=(lambda: self.connect_server()))
        launch_btn.pack()

        frame1 = ttk.Frame(root, padding=10)
        frame1.grid(row=1, column=0, sticky='w')

        self.msg_field = Text(frame1)
        self.msg_field.tag_config('server', foreground='red', font=('bold',))
        self.msg_field.tag_config('client', foreground='blue', font=('bold',))
        self.msg_field.size()
        self.msg_field.pack()

        frame2 = ttk.Frame(root, padding=10)
        frame2.grid(row=2, column=0, sticky='w')

        self.entry_box = ttk.Entry(frame2, width=86)
        self.entry_box.bind("<KeyPress-Return>", self.key_event)
        self.entry_box.pack(side='left')

        send_btn = Button(frame2, text="Send", command=(lambda: self.send_msg()))
        send_btn.pack(side='left')

        root.mainloop()

    def send_msg(self):
        msg = self.entry_box.get()
        if len(msg) > 0 and msg is not None:
            s.send(msg.encode('UTF-8'))
            self.msg_field.insert(tkinter.INSERT,
                                  'Client: ' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                             time.localtime()) + '\n' + msg + '\n'
                                  , 'client')
            self.entry_box.delete(0, END)
        else:
            tkinter.messagebox.showinfo('Warning', "No blank message allowed!")

    def connect_server(self):
        global s
        s.connect((host, port))
        t = threading.Thread(target=self.listen)
        try:
            t.start()
        except threading.ThreadError:
            print('error, cannot connect')

    def listen(self):
        while True:
            data = s.recv(1024).decode('UTF-8')
            if len(data) > 0 and data is not None:
                self.msg_field.insert(tkinter.INSERT,
                                      'Server: ' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                 time.localtime()) + '\n' + data + '\n'
                                      , 'server')

    def key_event(self, event):
        if event.keysym == 'Return':
            self.send_msg()


def main():
    ChatClient()


if __name__ == '__main__':
    main()
