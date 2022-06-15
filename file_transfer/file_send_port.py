"""
Author: Johnathan Van-Doninck
Date: May 2nd, 2022

Send files to client
"""

from socketserver import BaseRequestHandler

class FileSendHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server, file_name):
        self.file_name = file_name
    
    @classmethod
    def creator(cls, *args, **kwargs):
        def _handler_creator(request, client, address, server):
            cls(request, client_address, server, *args, **kwargs)
        return _handler_creator

    def handle(self):
        with open(self.file_name, 'br') as file:
            data = b''
            while data != '':
                data = file.read(self.file_size)
                self.request.send(data)
                print(data)
            self.request.sendall(bytes(f"{commands.Success()}", 'ascii'))
            print("Done")
        