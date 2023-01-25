import socket, sys
from threading import Thread
import datetime

HOST = "localhost"
PORT = 65123

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

stop_thread = False
print('Waiting for connection response')

def receive_and_print():
    global stop_thread
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


s.connect((HOST, PORT))
name = input('Enter your name: ')
s.sendall(str.encode(name))
res = s.recv(1024)
print(res.decode('utf-8'))
    

message_thread = Thread(target=receive_and_print)
message_thread.start()

while True:
    try:
        message = input()
        curret_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"{curret_time}\n{message}"
        s.sendall(str.encode(message))
    except KeyboardInterrupt:
        stop_thread = True
        break
    except Exception as e:
        stop_thread = True
        break


s.close()
sys.exit()