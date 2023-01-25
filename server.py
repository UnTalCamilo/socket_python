import socket, sys
from threading import Thread

HOST = "localhost"
PORT = 65123

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



CONNECTION_LIST = {}


stop_thread = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def accept_connections():
    global s, stop_thread
    while True:
        if stop_thread:
            break
        try:

            connection, addr = s.accept()
            uname = connection.recv(1024).decode("utf-8")
            CONNECTION_LIST[addr] = [uname, connection]
            connection.sendall(str.encode("Welcome to the server "+uname))
            print(f"{uname} has connected to the server")

            broadcast_thread = Thread(target=broadcast_usr, args=( connection, addr ))
            broadcast_thread.start()
            print("Broadcast thread started")
        except Exception as e:
            stop_thread = True
            break
        except KeyboardInterrupt:
            stop_thread = True
            break
    


def broadcast_usr(connection, addr):
    global s, stop_thread
    while True:
        if stop_thread:
            break
        try:
            data = connection.recv(1024)
            msg = f"{CONNECTION_LIST[addr][0]}: " + data.decode("utf-8")
            if not data:
                pass
            if len(CONNECTION_LIST) == 1:
                connection.sendall(str.encode("You are the only one connected"))
            else:
                for id, client in CONNECTION_LIST.items():
                    if id != addr:
                        client[1].sendall(str.encode(msg))
                connection.sendall(str.encode(" "))

        except socket.error as e:
            print(CONNECTION_LIST.keys())
            CONNECTION_LIST.pop(addr)
            print(CONNECTION_LIST.keys())
            break
        except Exception as e:
            stop_thread = True
            break
        except KeyboardInterrupt:
            stop_thread = True
            break
        
    connection.close()

def exit():
    global s
    print("Closing the server")
    s.close()
    sys.exit(0)

    

if __name__ == "__main__":
    s.bind((HOST, PORT))
    s.listen(3)
    print(f"Server started on {HOST}:{PORT}")

    accept_thread = Thread(target=accept_connections)
    accept_thread.start()

    while True:
        print("Main thread")
        try:
            print("If you want to exit type 'exit' at any time\n")
            msg = input()
            if msg.lower() == "exit":
                stop_thread = True
                break

        except Exception as e:
            stop_thread = True
            break
        except KeyboardInterrupt:
            stop_thread = True
            break
    exit()
    
    

