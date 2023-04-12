#!/usr/bin/env python3

# Nombre del Script: pyproxy3.py
# Descripción: Simple TCP Proxy - mirrors TCP traffic received on a port to two remote destinations
# Autor: Pablo Vargas <pvr.mza@gmail.com>
# Autor: ChatGPT <https://chat.openai.com>
# Fecha de Creación: 11 de Abril de 2023
# Versión: 1.0
# Licensed under the Apache License, Version 2.0 (the "License");


import argparse
import socket
import threading

# send data from conn_orign to conn_dest
def handle_client(conn_orign, addr, conn_dest):
    with conn_orign:
        while True:
            data = conn_orign.recv(2048)
            if not data:
                print(f" - Disconnected {addr}")
                break
            #
            try:
                conn_dest.sendall(data)
            except Exception as e:
                print(f" - Failed to send to {dest.getpeername()}: {e}")

# send data from conn_orign to multiple conn_dest
def handle_clients(conn_orign, addr, conn_dests):
    with conn_orign:
        print(f" - Connected by {addr}")
        while True:
            data = conn_orign.recv(2048)
            if not data:
                print(f" - Disconnected {addr}")
                break
            for dest in conn_dests:
                try:
                    dest.sendall(data)
                except Exception as e:
                    print(f" - Failed to send to {dest.getpeername()}: {e}")



def start_destinations(port, dest1, dest2):
    print(f" - check destinations...")
    destinations = []
    # 
    try:
        dest1_addr, dest1_port = dest1.split(':')
        dest1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest1_socket.connect((dest1_addr, int(dest1_port)))
        destinations.append(dest1_socket)
        print(f"   - Connected to {dest1}")
    except Exception as e:
        print(f"   ---> Failed to connect to {dest1}: {e}")
    # 
    try:
        dest2_addr, dest2_port = dest2.split(':')
        dest2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest2_socket.connect((dest2_addr, int(dest2_port)))
        destinations.append(dest2_socket)
        print(f"   - Connected to {dest2}")
    except Exception as e:
        print(f"   ---> Failed to connect to {dest2}: {e}")

    return destinations

def start_server(port, dest1, dest2):
    print(f"Start server...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen()

        print(f" - Listening on port {port} ")

        while True:
            conn, addr = server_socket.accept()
            destinations=start_destinations(port, dest1, dest2)
            if isinstance(destinations, list) and len(destinations) > 0:
                threading.Thread(target=handle_client, args=(destinations[0], addr, conn)).start()
                threading.Thread(target=handle_clients, args=(conn, addr, destinations)).start()

            else:
                print(f" - Disconnected {addr}")
                conn.close()
            

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='TCP traffic reflector with dual destinations')
    parser.add_argument('port', type=int, help='port to listen on')
    parser.add_argument('dest1', type=str, help='destination 1 (IP:port)')
    parser.add_argument('dest2', type=str, help='destination 2 (IP:port)')
    args = parser.parse_args()

    start_server(args.port, args.dest1, args.dest2)
