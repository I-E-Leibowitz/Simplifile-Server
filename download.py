from socket import socket, AF_INET, SOCK_STREAM
from sys import argv

HOST = "10.100.102.8"
PORT = 55445
FILE_PORT = 55446
command = "command: {command}\nid: {id}\n{args}\x04"

def download_file(ip, port, filename):
    # Receive file size or rejection
    # Read file from socket 1 bit at a time
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind((ip, port))
        sock.listen()
        conn, addr = sock.accept()
        print("Connection established...")
        file = b''
        with open(filename, 'bw') as down:
            print("File opened...")
            while True:
                data = conn.recv(1)
                print(data.decode('ascii'), end='')
                if not data: break
                file += data
            down.write(file)
            down.close()
        sock.close()

def request(ip, port, command):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(command, 'ascii'))
        print("awaiting response.")
        # data = sock.recv(1024)
        # print(str(data))

if __name__ == '__main__':
        cmd = command.format(command='download',
                        id='1',
                        args=f'username: {argv[1]}\nfile: {argv[2]}')
        request(HOST, PORT, cmd)
        download_file(HOST, FILE_PORT, argv[2])