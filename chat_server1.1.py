import socket
import threading
import time
import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.messagebox

# Socket setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
# bind ip and port
s.bind((host, 9999))
# open listener, 10 connects
s.listen(10)
# list to hold connected clients
socs = []
client_map = {}


class ChatServer:
    def __init__(self):
        self.root = Tk()
        self.build_ui(self.root)

        self.work = None
        self.msg_field = None
        self.entry_box = None

    def build_ui(self, root):
        root.title('Chat Server')

        frame = ttk.Frame(root, padding=10)
        frame.grid(row=0, column=0, sticky='e')

        launch_btn = Button(frame, text="Start service", command=(lambda: self.start_server()))
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

    def start_server(self):
        self.work = threading.Thread(target=self.listener_thread, )
        self.work.start()

    def listener_thread(self):
        print('I am thread, waiting for connection...')
        while True:
            # accept a connection
            sock, addr = s.accept()
            socs.append(sock)
            index = socs.index(sock)
            client_map[index] = sock
            t = threading.Thread(target=self.receive_thread, args=(sock, addr, self.msg_field,))
            try:
                t.start()
            except threading.ThreadError:
                print('listen thread error')
        # end thread and remove from list and dict
        time.sleep(3)
        t.join()
        self.work.join()
        client_map.pop(index)
        print(client_map)
        socs.remove(index)
        print('connection dropped')

    def receive_thread(self, sock, addr, msg_field):
        print('Accept new connection from %s:%s...' % addr)
        sock.send(('Welcome! Client' + str(socs.index(sock))).encode())
        while True:
            try:
                data = sock.recv(1024)
            except ConnectionResetError:
                print('connection dropped' + str(sock))
                socs.remove(sock)
                return
            if len(data) > 0 and data is not None:
                msg_field.insert(tkinter.INSERT,
                                 'Client' + str(socs.index(sock))
                                 + ': ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                 + '\n' + data.decode('UTF-8') + '\n', 'client')
            if data.decode('UTF-8') == 'exit' or not data:
                time.sleep(5)
                return;
            time.sleep(1)
        sock.close()
        print('Connection from %s:%s closed.' % addr)

    def send_msg(self):
        msg = self.entry_box.get()
        if len(msg) > 0 and msg is not None:
            for soc in socs:
                if isinstance(soc, socket.socket):
                    soc.send(self.entry_box.get().encode())
            self.msg_field.insert(tkinter.INSERT,
                                  'Server: '
                                  + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                  + '\n' + self.entry_box.get() + '\n', 'server')
            self.entry_box.delete(0, END)
        else:
            tkinter.messagebox.showinfo('Warning', "No blank message allowed!")

    def key_event(self, event):
        if event.keysym == 'Return':
            self.send_msg()


def main():
    ChatServer()


if __name__ == '__main__':
    main()
