from socket import socket, AF_INET, SOCK_STREAM
from os import path
from sys import argv
from time import sleep

HOST = "127.0.0.1"
PORT = 55445
FILE_PORT = 55446
command = "command: {command}\nid: {id}\n{args}\x04"


def client(command: str):
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(bytes(command, 'ascii'))
            print("awaiting response.")
            # data = sock.recv(1024)
            # print(str(data))

def upload_file(ip, port, file, size):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((ip, port))

        with open(file, 'br') as up:
            while True:
                try:
                    sleep(0.5)
                    data = up.read(size)
                    print(f"data: {data}\n{len(data)}\n---")
                    if not data: break
                    sock.send(data)
                except BrokenPipeError:
                    pass
            sock.send(b"")
            up.close()
            print(f"Recieved: {sock.recv(1024)}")

if __name__ == '__main__':
    size = path.getsize(argv[2])
    cmd = command.format(command='upload',
                        id='0',
                        args=f'Size: {size}\nUsername: {argv[1]}\nFilename: {argv[2]}\nHash: N/A')
    print(cmd)
    client(cmd)
    sleep(1)
    print("Sending file...")
    upload_file(HOST, FILE_PORT, argv[2], size)
