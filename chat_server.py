import _thread
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
s.bind((host, 9999))
s.receive_thread(5)
# list to hold connected clients
socs = []


class ChatServer:
    def __init__(self, msg_field, entry_box):
        super().__init__()
        self.distribute_thread(msg_field)
        entry_box.bind("<KeyPress-Return>", self.key_event(self, entry_box, msg_field))

    def start_threads(self, _id, msg_field, stop):
        print('Waiting for connection...')
        print("I am thread", _id)
        while True:
            print("I am thread {} waiting for connection".format(_id))
            # accept a connection:
            sock, addr = s.accept()
            socs.append(sock)
            # Create a new Thread for new tcp-connection:
            t = threading.Thread(target=self.tcp_link, args=(sock, addr, msg_field))
            t.start()
            if stop():
                print("  Exiting main socket loop.")
                break
        print("Thread {}, signing off".format(_id))

    def tcp_link(self, sock, addr, msg_field):
        print('Accept new connection from %s:%s...' % addr)
        sock.send('Welcome!'.encode())
        while True:
            data = sock.recv(1024)
            if len(data) > 0 and data is not None:
                msg_field.insert(tkinter.INSERT,
                                 'Client' + str(socs.index(sock))
                                 + ' | ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                 + '\n' + data.decode('UTF-8') + '\n')
            time.sleep(1)
            if data == 'exit' or not data:
                break
            # sock.send(('Hello, %s!' % data).encode())
        sock.close()
        print('Connection from %s:%s closed.' % addr)

    def distribute_thread(self, msg_field):
        stop_threads = False
        workers = []
        for _id in range(5):
            tmp = threading.Thread(target=self.start_threads, args=(_id, msg_field, lambda: stop_threads))
            workers.append(tmp)
            tmp.start()
            print(workers)
        time.sleep(3)
        print('main: done sleeping.')
        stop_threads = True
        for worker in workers:
            worker.join()
        print('Finis.')
        s.close()

    def send_msg(self, entry_box, msg_field):
        msg = entry_box.get()
        if len(msg) > 0 and msg is not None:
            for soc in socs:
                if isinstance(soc, socket.socket):
                    soc.send(entry_box.get().encode())
            msg_field.insert(tkinter.INSERT,
                             'Server | '
                             + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                             + '\n' + entry_box.get() + '\n')
            entry_box.delete(0, END)
        else:
            tkinter.messagebox.showinfo('Warning', "No blank message allowed!")

    def key_event(self, event, entry_box, msg_field):
        if event.keysym == 'Return':
            self.send_msg(entry_box, msg_field)


# create GUI
def build_ui():
    root = Tk()
    root.title("Chat Server")

    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0, sticky='e')

    launch_btn = Button(frame, text="Start service", command=(lambda: start_server(msg_field, entry_box)))
    launch_btn.pack()

    frame1 = ttk.Frame(root, padding=10)
    frame1.grid(row=1, column=0, sticky='w')

    msg_field = Text(frame1)
    msg_field.size()
    msg_field.pack()

    frame2 = ttk.Frame(root, padding=10)
    frame2.grid(row=2, column=0, sticky='w')

    entry_box = ttk.Entry(frame2, width=86)
    entry_box.pack(side='left')

    send_btn = Button(frame2, text="Send", command=(lambda: ChatServer.send_msg(ChatServer, entry_box, msg_field)))
    send_btn.pack(side='left')

    root.mainloop()


def start_server(msg_field, entry_box):
    try:
        _thread.start_new_thread(ChatServer, (msg_field, entry_box,))
    except _thread.error:
        print('error: cannot create thread.')


def main():
    build_ui()


if __name__ == '__main__':
    main()
