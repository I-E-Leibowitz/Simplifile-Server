"""
Author: Johnathan Van-Doninck
Date: April 26th, 2022

The port that receives all requests from clients and handles them accordingly.
"""

from sys import path
path.append("/home/luciferin/Documents/Fuck my life/Simplifile-Server")
from socketserver import BaseRequestHandler, TCPServer
from simplifile_api import exceptions, commands, parser

BUFFER = 1024

class RequestHandler(BaseRequestHandler):
    def handle(self):
        command_raw = ""
        print(f"Receiving command from {self.client_address}")
        while len(command_raw) < BUFFER:
            data = self.request.recv(1).decode('ascii')
            print(data, end='')
            command_raw += data
            if data == '\x04':
                break
        print(command_raw)
        command = parser.parser(command_raw)
        print(command)
        if command is commands._Command:
            command.execute()
            self.request.send("Operation Successful.")
        else:
            self.request.send(bytes(f'{command}', 'ascii'))


if __name__ == '__main__':
    # For testing purposes only, remove once server is fully implemented.
    host = "127.0.0.1"
    port = 55445
    with TCPServer((host, port), RequestHandler) as server:
        print("Server Started...")
        server.serve_forever()