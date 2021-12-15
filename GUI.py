from tkinter import *


class GUI:

    def __init__(self, master):
        self.master = master
        master.title("ChatServer")

        self.label = Label(master, text="Chat Server")
        self.label.pack()

        self.msgField = Text(master)
        self.msgField.size()
        self.msgField.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print('Nothing here')


root = Tk()
my_gui = GUI(root)
root.mainloop()
