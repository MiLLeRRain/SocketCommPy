import _thread
import socket
import threading
import time
import tkinter
from tkinter import *
from tkinter import ttk

# Socket setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
s.bind((host, 9999))
s.listen(5)
# array to hold connected clients
socs = []


def start_threads(_id, msg_field, stop):
    print('Waiting for connection...')
    print("I am thread", _id)
    while True:
        print("I am thread {} waiting for connection".format(_id))
        # accept a connection:
        sock, addr = s.accept()
        socs.append(sock)
        # Create a new Thread for new tcp-connection:
        t = threading.Thread(target=tcp_link, args=(sock, addr, msg_field))
        t.start()
        if stop():
            print("  Exiting main socket loop.")
            break
    print("Thread {}, signing off".format(_id))


def tcp_link(sock, addr, msg_field):
    print('Accept new connection from %s:%s...' % addr)
    sock.send('Welcome!'.encode())
    while True:
        data = sock.recv(1024)
        if len(data) > 0:
            msg_field.insert(tkinter.INSERT, '\nClient: ' + data.decode('UTF-8'))
        time.sleep(1)
        if data == 'exit' or not data:
            break
        # sock.send(('Hello, %s!' % data).encode())
    sock.close()
    print('Connection from %s:%s closed.' % addr)


def distribute_thread(msg_field):
    stop_threads = False
    workers = []
    for _id in range(1):
        tmp = threading.Thread(target=start_threads, args=(_id, msg_field, lambda: stop_threads))
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


class ChatServer(threading.Thread):

    def __init__(self, msg_field):
        distribute_thread(msg_field)


def send_msg(entry_box, msg_field):
    for soc in socs:
        soc.send(entry_box.get().encode())
    msg_field.insert(tkinter.INSERT, '\nServer:' + entry_box.get())
    entry_box.delete(0, END)


# create GUI
def build_ui():
    root = Tk()
    root.title("Chat Server")

    frame = ttk.Frame(root, padding=10)
    frame.grid()

    msg_field = Text(frame)
    msg_field.size()
    msg_field.grid()

    launch_btn = Button(frame, text="Start service", command=(lambda: start_server(msg_field)))
    launch_btn.grid()

    frame2 = ttk.Frame(root, padding=10)
    frame2.grid()

    entry_box = ttk.Entry(frame2, width=98)
    entry_box.grid()

    send_btn = Button(frame2, text="Send", command=(lambda: send_msg(entry_box, msg_field)))
    send_btn.grid()

    root.mainloop()


def main():
    build_ui()


def start_server(msg_field):
    try:
        _thread.start_new_thread(ChatServer, (msg_field,))
    except _thread.error:
        print('error: cannot create thread.')


if __name__ == '__main__':
    main()
