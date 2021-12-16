import threading
from tkinter import *
import _thread


class App(threading.Thread):

    def __init__(self, root, my_param2, my_param3):
        # Creare GUI
        self.root = root

        # Your code here

    def method1(self):


# Your code here


def main():
    # Create GUI
    root = Tk(className='MyApp')

    # Create 2 threads
    num_threads = 2
    for t in range(num_threads):

        try:
            _thread.start_new_thread(App, (root, my_param2, my_param3,))

        except:
            print('Error: can not create a thread')

    # tkinter main loop
    root.mainloop()

    print('You don\'t see this message')


if __name__ == "__main__":
    main()
