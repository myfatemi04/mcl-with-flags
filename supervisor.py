import socket

import config
import sensor_task
import pressure_control
from flags import flags
from registry import registry
from threading import Thread
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 20202))
s.listen()
conn, addr = s.accept()

def listen():
    while True:
        data = conn.recv(4096)

        if data == b'':
            print("Connection broke")
            break

        packs = data.split(b"\n")
        for pack in packs:
            if pack == b'actuate':
                print("Received request to ACTUATE")
                flags.actuate = True

            elif pack == b'abort':
                print("Received request to ABORT!")
                flags.abort = True

def read_control_actuate():
    print("Started R/C/A loop")

    while True:
        sensor_task.read()
        sensor_value = registry.sensor_reading
        conn.send(b"sensor:" + bytes(str(sensor_value), 'utf-8') + b"\n")

        pressure_control.control()
        if flags.send_warning:
            flags.send_warning = False
            conn.send(b"pressure_warning\n")

        if flags.abort:
            flags.abort = False
            conn.send(b"aborting\n")
            break

        sensor_task.actuate()
        time.sleep(1)

if __name__ == "__main__":
    listener_thread = Thread(target=listen, daemon=True)
    listener_thread.start()
    
    rca_thread = Thread(target=read_control_actuate, daemon=False)
    rca_thread.start()
