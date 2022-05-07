"""
Author: Johnathan Van-Doninck
Date: May 2nd, 2022

Send files to client
"""

from socketserver import BaseRequestHandler

class FileSendHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server, file_name, file_size, client_name):
        self.file_name = file_name
        self.file_size = file_size
        self.client_name = client_name
    
    @classmethod
    def creator(cls, *args, **kwargs):
        def _handler_creator(request, client, address, server):
            cls(request, client_address, server, *args, **kwargs)
        return _handler_creator

    def handle(self):
        data = b''
        with open(f'./{self.client_name}/{self.file_name}', 'rb') as file:
            data = file.read(self.file_size)
            self.request.sendall(data)
        