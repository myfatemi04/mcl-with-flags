import socket
from threading import Thread

client = socket.socket()
client.connect(('localhost', 20202))

def receive_data():
    while True:
        data = client.recv(4096)

        if data == b'':
            print("Connection broke")
            break

        packs = data.split(b"\n")
        
        for pack in packs:
            if pack == b"pressure_warning":
                print("ALERT: THE ROCKET'S GONNA BLOW UP (PRESSURE'S FAULT)")
            elif pack == b"aborting":
                print("ALERT: Rocket is aborting launch")
            elif len(pack) > 0:
                print("Read data:", pack)

def console():
    command = ''
    while command != 'exit':
        command = input()
        client.send(bytes(command,'utf-8'))

if __name__ == "__main__":
    receive_data_thread = Thread(target=receive_data, daemon=True)
    receive_data_thread.start()

    console_thread = Thread(target=console)
    console_thread.start()