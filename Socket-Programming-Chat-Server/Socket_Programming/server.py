# import socket
# import selectors
# import threading

# HEADER = 64
# PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
# ADDR = (SERVER, PORT)
# FORMAT = 'utf-8'
# DISCONNECT_MESSAGE = "!DISCONNECT"

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(ADDR)
# server.setblocking(False)

# sel = selectors.DefaultSelector()
# sel.register(server, selectors.EVENT_READ, data=None)

# clients = {}


# def accept_wrapper(sock):
#     conn, addr = sock.accept()
#     print(f"[NEW CONNECTION] {addr} connected.")
#     conn.setblocking(False)  # 設定為非阻塞
#     sel.register(conn, selectors.EVENT_READ, data=conn)

# # 在程式開始時創建一個鎖
# clients_lock = threading.Lock()

# # 在 handle_client 函數中使用鎖
# def handle_client(conn, addr):
#     print(f"[NEW CONNECTION] {addr} connected.")

#     connected = True
#     while connected:
#         try:
#             msg_length = conn.recv(HEADER).decode(FORMAT)
#             if msg_length:
#                 msg_length = int(msg_length)
#                 msg = conn.recv(msg_length).decode(FORMAT)

#                 if msg == DISCONNECT_MESSAGE:
#                     connected = False

#                 for client_conn in clients.values():
#                     if client_conn != conn:
#                         try:
#                             client_conn.send(f"[{addr}] {msg}".encode(FORMAT))
#                         except Exception as e:
#                             print(f"[ERROR] Error sending message to a client: {e}")

#                 print(f"[{addr}] {msg}")
#                 conn.send("Message has been sent to Wei's server.".encode(FORMAT))
#         except Exception as e:
#             print(f"[ERROR] Error handling client connection: {e}")
#             connected = False

#     with clients_lock:
#         # 關閉連接
#         try:
#             sel.unregister(conn)
#         except Exception as e:
#             print(f"[ERROR] Error unregistering connection: {e}")

#         del clients[addr]
#         conn.close()
#         print(f"[DISCONNECTED] {addr} disconnected. Active connections: {len(clients)}")



# def start_server():
#     server.listen()
#     print(f"[LISTENING] Server is listening on {SERVER}")

#     while True:
#         events = sel.select(timeout=None)
#         for key, mask in events:
#             if key.data is None:
#                 accept_wrapper(key.fileobj)
#             else:
#                 client_conn = key.fileobj
#                 addr = client_conn.getpeername()
#                 data = key.data
#                 thread = threading.Thread(target=handle_client, args=(client_conn, addr))
#                 thread.start()
#                 clients[addr] = client_conn


# print("[STARTING] server is starting...")
# start_server()




import socket
import threading


#伺服器基本設定
HEADER = 64
#we need to pick a port -> 我們要跑的
PORT = 5050
#取得IPv4 位址 -> local network
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT='utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


#make a new socket
#server->the family of socket (pick the type(over the internet),pick the method(sock string))
#Ipv4位址及TCP協定
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#bound this socket to ADDR這個位址和port
server.bind(ADDR)

#用來儲存所有client端連接的字典
#以客戶端位址 addr 為鍵，對應conn為值
clients = {}

#接收客戶端的socket和addr
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        try:
            # 接收消息的長度
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                # 接收實際的消息
                msg = conn.recv(msg_length).decode(FORMAT)

                #處理斷線請求
                if msg == DISCONNECT_MESSAGE:
                    connected = False

                #將消息發送給所有其他客戶端
                for client_conn in clients.values():
                    if client_conn != conn:
                        try:
                            client_conn.send(f"[{addr}] {msg}".encode(FORMAT))
                        except Exception as e:
                            print(f"[ERROR] Error sending message to a client: {e}")
                
                print(f"[{addr}] {msg}")
                #conn.send("Message has been sent to Wei's server.".encode(FORMAT))
        except Exception as e:
            print(f"[ERROR] Error handling client connection: {e}")
            connected = False

    # 關閉連接
    del clients[addr]
    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected. Active connections: {len(clients)}")

#server啟動
def start_server():
    #listening for the new connection
    server.listen()
    print(f"[LISTENING] Server is listenning on {SERVER}")
    #持續listen till 不想聽了
    while True:
        #聽到新的請求
        conn , addr = server.accept()
        clients[addr] = conn
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {len(clients)}")


print("[STARING] server is starting...")
start_server()



# import socket
# import threading
# import selectors

# HEADER = 64
# PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
# ADDR = (SERVER, PORT)
# FORMAT = 'utf-8'
# DISCONNECT_MESSAGE = "!DISCONNECT"

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(ADDR)
# server.setblocking(False)  # 設定為non-blocking

# sel = selectors.DefaultSelector()
# sel.register(server, selectors.EVENT_READ, data=None)

# clients = {}


# def accept_wrapper(sock):
#     conn, addr = sock.accept()  # 建立連接
#     print(f"[NEW CONNECTION] {addr} connected.")
#     conn.setblocking(False)  # 設定為non-blocking
#     sel.register(conn, selectors.EVENT_READ, data=conn)


# def handle_client(conn, addr):
#     print(f"[NEW CONNECTION] {addr} connected.")

#     connected = True
#     while connected:
#         try:
#             # 接收消息的長度
#             msg_length = conn.recv(HEADER).decode(FORMAT)
#             if msg_length:
#                 msg_length = int(msg_length)
#                 # 接收實際的消息
#                 msg = conn.recv(msg_length).decode(FORMAT)

#                 if msg == DISCONNECT_MESSAGE:
#                     connected = False

#                 for client_conn in clients.values():
#                     if client_conn != conn:
#                         try:
#                             client_conn.send(f"[{addr}] {msg}".encode(FORMAT))
#                         except Exception as e:
#                             print(f"[ERROR] Error sending message to a client: {e}")

#                 print(f"[{addr}] {msg}")
#                 conn.send("Message has been sent to Wei's server.".encode(FORMAT))
#         except Exception as e:
#             print(f"[ERROR] Error handling client connection: {e}")
#             connected = False

#     del clients[addr]
#     conn.close()
#     sel.unregister(conn)
#     print(f"[DISCONNECTED] {addr} disconnected. Active connections: {len(clients)}")


# def start_server():
#     server.listen()
#     print(f"[LISTENING] Server is listenning on {SERVER}")

#     while True:
#         events = sel.select(timeout=None)
#         for key, mask in events:
#             if key.data is None:
#                 accept_wrapper(key.fileobj)
#             else:
#                 client_conn = key.fileobj
#                 addr = client_conn.getpeername()
#                 data = key.data
#                 thread = threading.Thread(target=handle_client, args=(client_conn, addr))
#                 thread.start()
#                 clients[addr] = client_conn


# print("[STARING] server is starting...")
# start_server()
