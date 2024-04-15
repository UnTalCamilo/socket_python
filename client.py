import socket, sys
from threading import Thread
import datetime

HOST = "localhost"
PORT = 65123

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

stop_thread = False
print('Waiting for connection response')

def message_handler():
    global stop_thread, s
    try:
        for message in iter(lambda: s.recv(1024).decode(), ''):
            if message == " ":
                pass
            else:
                print(f"\n{message}\n")
                
    except Exception as e:
        stop_thread = True
        return
    except KeyboardInterrupt:
        stop_thread = True
        return

def client_start():
    global s, stop_thread
    try:
        s.connect((HOST, PORT))
        name = input('Enter your name: ')
        s.sendall(str.encode(name))

        receive_thread = Thread(target=message_handler)
        receive_thread.start()
        
        while True:
            if stop_thread:
                break
            try:
                print
                message = input("Message:")
                curret_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"{curret_time}\n{message}"
                s.sendall(str.encode(message))
            except KeyboardInterrupt:
                stop_thread = True
                break
            except Exception as e:
                stop_thread = True
                break
    except Exception as e:
        return False

def exit():
    global s
    s.close()
    sys.exit()


    
if __name__ == "__main__":
    client_thread = Thread(target=client_start)
    client_thread.start()

    if stop_thread:
        exit()