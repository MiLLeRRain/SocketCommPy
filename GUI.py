import threading
from tkinter import *
import chat_server

class GUI:

    def __init__(self, master):
        self.master = master
        master.title("ChatServer")

        self.label = Label(master, text="Chat Server")
        self.label.pack()

        self.msgField = Text(master)
        self.msgField.size()
        self.msgField.pack()

        self.greet_button = Button(master, text="Start", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print('Starting server')
        server_thread = threading.Thread(chat_server.main())
        server_thread.start()


root = Tk()
my_gui = GUI(root)
root.mainloop()
