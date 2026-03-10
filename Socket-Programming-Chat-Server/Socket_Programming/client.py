# import socket
# import threading
# import tkinter as tk
# from tkinter import scrolledtext
# from tkinter import ttk
# from PIL import Image, ImageTk
# from tkinter import Tk, Canvas, PhotoImage
# from PIL import Image, ImageTk


# HEADER = 64
# PORT = 5050
# FORMAT = 'utf-8'
# DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = socket.gethostbyname(socket.gethostname())
# ADDR = (SERVER, PORT)

# class StartScreen:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Welcom to Wei's Chat Server ლ(╹◡╹ლ)")

#         # 設定窗口大小
#         self.root.geometry('570x335')
#         # 設定背景圖片
#         image = Image.open("start_background.png")
#         photo = ImageTk.PhotoImage(image)

#         # 使用 Canvas 來顯示背景圖片
#         canvas = tk.Canvas(root, width=image.width, height=image.height)
#         #canvas.pack(fill="both", expand=True)
#         canvas.create_image(0,0, anchor="nw",image=photo)
#         canvas.image = photo
#         canvas.pack()
    

#         # 開始聊天按鈕
#         global start_button
#         start_button = tk.Button(root, text="ฅ^•ﻌ•^ฅ", command=self.start_chat)
#         #start_button.pack(side="top", anchor="center", pady=20)
#         start_button.place(x=240,y=300)
#         start_button.config(bg='#DAA176', fg='black')
#         start_button.configure(font=("Courier New", 10))
        

#     def start_chat(self):
#         # 開啟聊天室視窗
#         chat_window = tk.Toplevel(self.root)
#         chat_gui = ClientGUI(chat_window)
#         start_button["state"]="disabled"

# class ClientGUI:
#     #初始化函數，建立客戶端GUI
#     def __init__(self, root):
#         self.root = root
#         self.root.title("~Wei's Chat Server~")
        
#         # 設定窗口大小
#         self.root.geometry('400x400')

#         #聊天室(可捲動)
#         self.chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=20)
#         self.chat_box.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

#         #輸入框
#         self.message_entry = tk.Entry(root, width=30)
#         self.message_entry.grid(row=1, column=0, padx=1, pady=5)
#         #send button
#         self.send_button = tk.Button(root, text="Send", command=self.send_message)
#         self.send_button.grid(row=1, column=1, padx=2, pady=5)

#         # 設定文本框、輸入框、按鈕的背景和前景顏色
#         # 修改背景顏色
#         self.root.configure(bg='#d0b595')
#         #self.chat_box.config(fg='#5f4b3b', highlightbackground='#5f4b3b', highlightcolor='#5f4b3b')
#         self.chat_box.config(bg='#e4d9ce',fg='#5f4b3b')
#         #self.chat_box.config(fg='#5f4b3b')
#         self.message_entry.config(bg='#e4d9ce',fg='#5f4b3b')
#         self.send_button.config(bg='#99674d', fg='white')

#         # 設定字型和字型大小
#         self.chat_box.configure(font=("Georgia", 10))
#         self.message_entry.configure(font=("Comic Sans MS", 10))
#         self.send_button.configure(font=("Courier New", 10))


#         #client端的socket
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.connect_to_server()

#         self.receive_thread = threading.Thread(target=self.receive_messages)
#         self.receive_thread.start()

#         # 定義一個變數用於存儲接收到的消息的字串
#         self.received_messages = ""

#         # 定期檢查是否有新消息
#         self.check_for_messages()

#     #與server連線
#     def connect_to_server(self):
#         try:
#             self.socket.connect(ADDR)
#         except Exception as e:
#             print(f"[ERROR] Unable to connect to the server: {e}")

#     def send_message(self):

#         message = self.message_entry.get()

#         if message:
#             try:
#                 msg = message.encode(FORMAT)
#                 msg_length = len(msg)
#                 send_length = str(msg_length).encode(FORMAT)
#                 send_length += b' ' * (HEADER - len(send_length))
#                 self.socket.send(send_length)
#                 self.socket.send(msg)
#                 self.message_entry.delete(0, tk.END)
#             except Exception as e:
#                 print(f"[ERROR] Error sending message: {e}")
            
#             # 在這裡只印出伺服器的回應，而不將其添加到 received_messages 中
#             response = self.socket.recv(2048).decode(FORMAT)
#             print(response)


#     def receive_messages(self):
#         while True:
#             try:
#                 # 接收伺服器發送的消息
#                 message = self.socket.recv(1024).decode(FORMAT)
#                 if not message:
#                     break  # 如果沒有新消息，跳出迴圈

#                 print(f"[SERVER] {message}")
#                 # 將消息添加到 received_messages 變數中
#                 self.received_messages += f"[SERVER] {message}\n"
#             except Exception as e:
#                 print(f"[ERROR] Error receiving message: {e}")
#                 break

    
#     def check_for_messages(self):
#         # 如果有新消息，則將其添加到聊天框中
#         if self.received_messages:
#             self.chat_box.insert(tk.END, self.received_messages)
#             # 滾動至最新消息
#             self.chat_box.yview(tk.END)  
#             # 清空 received_messages 變數
#             self.received_messages = ""

#         # 之後再次定期檢查，只有在有新消息時才調用
#         self.root.after(100, self.check_for_messages)




# #啟動GUI
# if __name__ == "__main__":
#     root = tk.Tk()
#     start_screen = StartScreen(root)
#     root.mainloop()




# import socket
# import threading
# import tkinter as tk
# from tkinter import scrolledtext
# from tkinter import ttk
# from PIL import Image, ImageTk
# from tkinter import Tk, Canvas, PhotoImage
# from PIL import Image, ImageTk


# HEADER = 64
# PORT = 5050
# FORMAT = 'utf-8'
# DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = socket.gethostbyname(socket.gethostname())
# ADDR = (SERVER, PORT)

# class StartScreen:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Welcom to Wei's Chat Server ლ(╹◡╹ლ)")

#         # 設定窗口大小
#         self.root.geometry('570x335')
#         # 設定背景圖片
#         image = Image.open("start_background.png")
#         photo = ImageTk.PhotoImage(image)

#         # 使用 Canvas 來顯示背景圖片
#         canvas = tk.Canvas(root, width=image.width, height=image.height)
#         #canvas.pack(fill="both", expand=True)
#         canvas.create_image(0,0, anchor="nw",image=photo)
#         canvas.image = photo
#         canvas.pack()
    

#         # 開始聊天按鈕
#         global start_button
#         start_button = tk.Button(root, text="ฅ^•ﻌ•^ฅ", command=self.start_chat)
#         #start_button.pack(side="top", anchor="center", pady=20)
#         start_button.place(x=240,y=300)
#         start_button.config(bg='#DAA176', fg='black')
#         start_button.configure(font=("Courier New", 10))
        

#     def start_chat(self):
#         # 開啟聊天室視窗
#         chat_window = tk.Toplevel(self.root)
#         chat_gui = ClientGUI(chat_window)
#         start_button["state"]="disabled"

# class ClientGUI:
#     #初始化函數，建立客戶端GUI
#     def __init__(self, root):
#         self.root = root
#         self.root.title("~Wei's Chat Server~")
        
#         # 設定窗口大小
#         self.root.geometry('400x400')

#         #聊天室(可捲動)
#         self.chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=20)
#         self.chat_box.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

#         #輸入框
#         self.message_entry = tk.Entry(root, width=30)
#         self.message_entry.grid(row=1, column=0, padx=1, pady=5)
#         #send button
#         self.send_button = tk.Button(root, text="Send", command=self.send_message)
#         self.send_button.grid(row=1, column=1, padx=2, pady=5)

#         # 設定文本框、輸入框、按鈕的背景和前景顏色
#         # 修改背景顏色
#         self.root.configure(bg='#d0b595')
#         #self.chat_box.config(fg='#5f4b3b', highlightbackground='#5f4b3b', highlightcolor='#5f4b3b')
#         self.chat_box.config(bg='#e4d9ce',fg='#5f4b3b')
#         #self.chat_box.config(fg='#5f4b3b')
#         self.message_entry.config(bg='#e4d9ce',fg='#5f4b3b')
#         self.send_button.config(bg='#99674d', fg='white')

#         # 設定字型和字型大小
#         self.chat_box.configure(font=("Georgia", 10))
#         self.message_entry.configure(font=("Comic Sans MS", 10))
#         self.send_button.configure(font=("Courier New", 10))


#         #client端的socket
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.connect_to_server()

#         self.receive_thread = threading.Thread(target=self.receive_messages)
#         self.receive_thread.start()

#         # 定義一個變數用於存儲接收到的消息的字串
#         self.received_messages = ""

#         # 定期檢查是否有新消息
#         self.check_for_messages()

#     #與server連線
#     def connect_to_server(self):
#         try:
#             self.socket.connect(ADDR)
#         except Exception as e:
#             print(f"[ERROR] Unable to connect to the server: {e}")

#     def send_message(self):
#         # 獲取使用者輸入的消息
#         message = self.message_entry.get()

#         if message:
#             try:
#                 # 將消息編碼並發送給伺服器
#                 msg = message.encode(FORMAT)
#                 msg_length = len(msg)
#                 send_length = str(msg_length).encode(FORMAT)
#                 send_length += b' ' * (HEADER - len(send_length))
#                 self.socket.send(send_length)
#                 #送出給server消息
#                 self.socket.send(msg)
#                 # 清空輸入框
#                 self.message_entry.delete(0, tk.END)

#             except Exception as e:
#                 print(f"[ERROR] Error sending message: {e}")

#                 # 在接收消息的執行緒中處理伺服器的回應
#                 response = self.socket.recv(2048).decode(FORMAT)
#                 print(response)

#     def receive_messages(self):
#         while True:
#             try:
#                 # 接收伺服器發送的消息
#                 message = self.socket.recv(1024).decode(FORMAT)
#                 print(f"[SERVER] {message}")
#                 # 將消息添加到 received_messages 變數中
#                 self.received_messages += f"[SERVER] {message}\n"
#             except Exception as e:
#                 print(f"[ERROR] Error receiving message: {e}")
#                 break
    
#     def check_for_messages(self):
#         # 每100毫秒檢查一次是否有新消息
#         self.chat_box.delete(1.0, tk.END)  # 清空聊天框
#         self.chat_box.insert(tk.END, self.received_messages)  # 將接收到的消息添加到聊天框中
#         # 滾動至最新消息
#         self.chat_box.yview(tk.END)  

#         # 之後再次定期檢查
#         self.root.after(100, self.check_for_messages)

# #果該檔案是被引用，其值會是模組名稱；但若該檔案是(透過命令列)直接執行，其值會是 __main__；
# #啟動GUI
# if __name__ == "__main__":
#     root = tk.Tk()
#     start_screen = StartScreen(root)
#     root.mainloop()



import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import Tk, Canvas, PhotoImage
from PIL import Image, ImageTk


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcom to Wei's Chat Server ლ(╹◡╹ლ)")

        # 設定窗口大小
        self.root.geometry('570x335')
        # 設定背景圖片
        image = Image.open("start_background.png")
        photo = ImageTk.PhotoImage(image)

        # 使用 Canvas 來顯示背景圖片
        canvas = tk.Canvas(root, width=image.width, height=image.height)
        #canvas.pack(fill="both", expand=True)
        canvas.create_image(0,0, anchor="nw",image=photo)
        canvas.image = photo
        canvas.pack()
    

        # 開始聊天按鈕
        global start_button
        start_button = tk.Button(root, text="ฅ^•ﻌ•^ฅ", command=self.start_chat)
        #start_button.pack(side="top", anchor="center", pady=20)
        start_button.place(x=240,y=300)
        start_button.config(bg='#DAA176', fg='black')
        start_button.configure(font=("Courier New", 10))
        

    def start_chat(self):
        # 開啟聊天室視窗
        chat_window = tk.Toplevel(self.root)
        chat_gui = ClientGUI(chat_window)
        start_button["state"]="disabled"

class ClientGUI:
    #初始化函數，建立客戶端GUI
    def __init__(self, root):
        self.root = root
        self.root.title("~Wei's Chat Server~")
        
        # 設定窗口大小
        self.root.geometry('400x400')

        #聊天室(可捲動)
        self.chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=20)
        self.chat_box.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        #輸入框
        self.message_entry = tk.Entry(root, width=30)
        self.message_entry.grid(row=1, column=0, padx=1, pady=5)
        #send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=2, pady=5)

        # 設定文本框、輸入框、按鈕的背景和前景顏色
        # 修改背景顏色
        self.root.configure(bg='#d0b595')
        #self.chat_box.config(fg='#5f4b3b', highlightbackground='#5f4b3b', highlightcolor='#5f4b3b')
        self.chat_box.config(bg='#e4d9ce',fg='#5f4b3b')
        #self.chat_box.config(fg='#5f4b3b')
        self.message_entry.config(bg='#e4d9ce',fg='#5f4b3b')
        self.send_button.config(bg='#99674d', fg='white')

        # 設定字型和字型大小
        self.chat_box.configure(font=("Georgia", 10))
        self.message_entry.configure(font=("Comic Sans MS", 10))
        self.send_button.configure(font=("Courier New", 10))


        #client端的socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

        # 定義一個變數用於存儲接收到的消息的字串
        self.received_messages = ""

        # 定期檢查是否有新消息
        self.check_for_messages()

    #與server連線
    def connect_to_server(self):
        try:
            self.socket.connect(ADDR)
        except Exception as e:
            print(f"[ERROR] Unable to connect to the server: {e}")

    def send_message(self):
        # 獲取使用者輸入的消息
        message = self.message_entry.get()

        if message:
            try:
                # 將消息添加到聊天框
                self.chat_box.insert(tk.END, f"[You] {message}\n")
                # 滾動至最新消息
                self.chat_box.yview(tk.END)

                # 將消息編碼並發送給伺服器
                msg = message.encode(FORMAT)
                msg_length = len(msg)
                send_length = str(msg_length).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                self.socket.send(send_length)
                #送出給server消息
                self.socket.send(msg)
                # 清空輸入框
                self.message_entry.delete(0, tk.END)

            except Exception as e:
                print(f"[ERROR] Error sending message: {e}")

                # 在接收消息的執行緒中處理伺服器的回應
                response = self.socket.recv(2048).decode(FORMAT)
                print(response)

    def receive_messages(self):
        while True:
            try:
                # 接收伺服器發送的消息
                message = self.socket.recv(1024).decode(FORMAT)
                print(message)

                # 判斷是否為實際聊天消息
                if not message.startswith("[SERVER]"):
                    # 將消息添加到聊天框
                    self.chat_box.insert(tk.END, f"{message}\n")
                    # 滾動至最新消息
                    self.chat_box.yview(tk.END)

            except Exception as e:
                print(f"[ERROR] Error receiving message: {e}")
                break

    
    def check_for_messages(self):
        # 將接收到的消息添加到聊天框中
        self.chat_box.insert(tk.END, self.received_messages)
        # 滾動至最新消息
        self.chat_box.yview(tk.END)  

        # 清空 received_messages 變數，準備接收下一批新消息
        self.received_messages = ""

        # 之後再次定期檢查
        self.root.after(100, self.check_for_messages)


#果該檔案是被引用，其值會是模組名稱；但若該檔案是(透過命令列)直接執行，其值會是 __main__；
#啟動GUI
if __name__ == "__main__":
    root = tk.Tk()
    start_screen = StartScreen(root)
    root.mainloop()
