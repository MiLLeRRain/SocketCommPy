import socket
import threading
import time
import tkinter
from tkinter import *
from tkinter import ttk

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = '127.0.0.1'
# port = 9999
# # Receiving 'Welcome':
# # Establish connection:
# s.connect(('127.0.0.1', 9999))
# print('Start talking to server:')
# while True:
#     # msg = input()
#     # # Send msg:
#     # s.send(str(msg).encode())
#     # if msg == 'exit':
#     #     break
#     data = s.recv(1024)
#     if len(data) > 0:
#         print('Server: ' + data.decode('UTF-8'))
# s.close()


# Start the socket connection
def start_thread(msg_field):

    # Establish connection:
    s.connect(('127.0.0.1', 9999))
    print('connected')

    while True:
        t = threading.Thread(target=tcp_link, args=(s, msg_field))
        t.start()

    # while True:
    #     data = s.recv(1024)
    #     if len(data) > 0:
    #         display(data.decode('UTF-8'), msg_field)
    #     if stop():
    #         break


def tcp_link(sock, msg_field):
    while True:
        data = sock.recv(1024)
        if len(data) > 0:
            display(data.decode('UTF-8'), msg_field)


# Connect the Server
def connect_server(msg_field):
    work = threading.Thread(target=start_thread, args=msg_field)
    work.start()
    print(str(work) + 'started')
    time.sleep(3)


# Display the msg got from the Server
def display(msg, msg_field):
    msg_field.insert(tkinter.INSERT, 'Server: ' + msg)


# Send msg to the Server
def send_msg(entry_box, msg_field):
    msg = entry_box.get()
    if msg == 'exit':
        s.close()
    s.send(msg.encode())
    display('\nI said: ' + msg, msg_field)
    entry_box.delete(0, END)


def build_ui():
    root = Tk()
    root.title("Chat Client")

    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0, sticky='e')

    launch_btn = Button(frame, text="Connect service", command=(lambda: connect_server(msg_field)))
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

    send_btn = Button(frame2, text="Send", command=(lambda: send_msg(entry_box, msg_field)))
    send_btn.pack(side='left')

    root.mainloop()


def main():
    build_ui()


if __name__ == '__main__':
    main()
