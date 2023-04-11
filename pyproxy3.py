#!/usr/bin/env python3

# Nombre del Script: pyproxy3.py
# Descripción: Simple TCP Proxy - mirrors TCP traffic received on a port to two remote destinations
# Autor: Pablo Vargas <pvr.mza@gmail.com>
# Autor: ChatGPT <https://chat.openai.com>
# Fecha de Creación: 11 de Abril de 2023
# Versión: 1.0
# Licensed under the Apache License, Version 2.0 (the "License");

import socket
import threading
import argparse
import select
import time


def send_data(addr, data, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as dest_socket:
        max_attempts = 3
        attempt = 1
        while attempt <= max_attempts:
            try:
                dest_socket.connect((host, port))
                dest_socket.sendall(data)
                #print(f"Sending data from {addr} to {host}:{port}")
                break
            except Exception as e:
                print(f"Error sending data - Attempt: {attempt} - from {addr} to {host}:{port}: {e}")
                attempt += 1
                time.sleep(1)  # Pausa de 1 segundo entre intentos
            finally:
                dest_socket.close()

def handle_client(conn, addr, port, dest1, dest2):
    BUFFER_SIZE = 2048

    print(f"New connection from {addr}")

    data = conn.recv(BUFFER_SIZE)
    clients_data = bytearray()

    while data:
        clients_data += data
        data = conn.recv(BUFFER_SIZE)

    print(f"Received {len(clients_data)} bytes from {addr} - {clients_data}")

    threading.Thread(target=send_data, args=(addr, clients_data, dest1, port)).start()
    threading.Thread(target=send_data, args=(addr, clients_data, dest2, port)).start()

    conn.close()

def main(port, dest1, dest2):
    LISTEN_HOST = '0.0.0.0'
    LISTEN_PORT = port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((LISTEN_HOST, LISTEN_PORT))
        listen_socket.listen()

        print(f"Listening on {LISTEN_HOST}:{LISTEN_PORT}")

        while True:
            conn, addr = listen_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr, port, dest1, dest2)).start()

if __name__ == '__main__':
    # Define the argument parser
    parser = argparse.ArgumentParser(description='TCP forwarding server')
    parser.add_argument('port', type=int, help='Port number of destination 1')
    parser.add_argument('dest1_host', help='Hostname of destination 1')    
    parser.add_argument('dest2_host', help='Hostname of destination 2')
    

    # Parse the arguments
    args = parser.parse_args()
    main(args.port, args.dest1_host, args.dest2_host)