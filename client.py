from socket import *
import tkinter as tk
import tkinter.scrolledtext as tst
import time
import tkinter.messagebox
import threading


# 定義輸入服務器ip地址的類
class inputIPdialog(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.ipInput = tk.Text(self, width=30, height=5)
        self.ipInput.grid(row=0, column=0, columnspan=3)
        self.okbtn = tk.Button(self, text='確定', command=self.setIP).grid(row=1, column=3)
        self.grid()

    def setIP(self):
        # 這個global變量作爲類變量的話沒有效果，原因不知
        global servername
        servername = self.ipInput.get('1.0', 'end-1c')
        # 銷燬窗口
        ipRootFrame.destroy()


class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # 顯示聊天窗口
        self.textEdit = tst.ScrolledText(self, width=50, height=15)
        self.textEdit.grid(row=0, column=0, rowspan=1, columnspan=4)
        self.textEdit.config(state='disabled')
        # 定義標籤，改變字體顏色
        self.textEdit.tag_config('server', foreground='red')
        self.textEdit.tag_config('guest', foreground='blue')

        # 編輯窗口
        self.inputText = tk.Text(self, width=40, height=5)
        self.inputText.grid(row=1, column=0, columnspan=1)
        # 定義快捷鍵，按下回車即可發送消息
        self.inputText.bind("<KeyPress-Return>", self.textSendReturn)

        # 發送按鈕
        self.btnSend = tk.Button(self, text='send', command=self.textSend)
        self.btnSend.grid(row=1, column=3)

        # 開啓一個線程用於接收消息並顯示在聊天窗口
        t = threading.Thread(target=self.getInfo)
        t.start()

    def textSend(self):
        # 獲取Text的所有內容
        # https://stackoverflow.com/questions/14824163/how-to-get-the-input-from-the-tkinter-text-box-widget
        str = self.inputText.get('1.0', 'end-1c')
        if str != "" and str != None:
            # 顯示發送時間和發送消息
            timemsg = '客戶端' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n'
            # 通過設置state屬性設置textEdit可編輯
            self.textEdit.config(state='normal')

            self.textEdit.insert(tk.INSERT, timemsg, 'guest')
            self.textEdit.insert(tk.INSERT, str + '\n')

            # 將滾動條拉到最後顯示最新消息
            self.textEdit.see(tk.END)
            # 通過設置state屬性設置textEdit不可編輯
            self.textEdit.config(state='disabled')
            self.inputText.delete(0.0, tk.END)  # 刪除輸入框的內容
            # 發送數據到服務端
            sendMessage = bytes(str, encoding='utf8')
            # 發送輸入的數據，與UDP有點不同，使用的是send方法，不需要指定服務器和端口，因爲已經建立了一條tcp連接
            clientSocket.send(sendMessage)
        else:
            tk.messagebox.showinfo('警告', "不能發送空白信息！")

    def getInfo(self):
        global clientSocket
        while True:
            # 接收數據,1024指定緩存長度，使用的是recv方法
            recMessage = clientSocket.recv(1024).decode("utf8") + '\n'
            # 接受時間和接收的數據
            recTime = '服務端' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n'
            self.textEdit.config(state='normal')
            # server作爲標籤,改變字體顏色
            self.textEdit.insert(tk.END, recTime, 'server')
            self.textEdit.insert(tk.END, recMessage)
            # 將滾動條拉到最後顯示最新消息
            self.textEdit.see(tk.END)
            self.textEdit.config(state='disabled')

    def textSendReturn(self, event):
        if event.keysym == "Return":
            self.textSend()


# 指定服務器地址，端口
servername = ''
serverport = 9999
ipRootFrame = tk.Tk()
ipRootFrame.title('輸入服務器ip')
ipDialog = inputIPdialog(ipRootFrame)
ipDialog.mainloop()
# socket第一個參數指定使用IPV4協議，第二個參數指定這是一個TCP套接字
clientSocket = None

try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
except:
    tk.messagebox.showinfo('未知錯誤', '檢查服務器地址是否錯誤！')

# tcp連接需要先經過握手建立連接
clientSocket.connect((servername, serverport))
root = tk.Tk()
root.title('客戶端')

app = Application(master=root)
app.mainloop()
