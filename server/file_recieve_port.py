"""
Author: Johnathan Van-Doninck
Date: May 2nd, 2022

Receives files from client
"""

from socketserver import BaseRequestHandler
from simplifile_api import commands, exceptions

class FileRecieveHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server, file_size, file_name, client_name):
        self.file_size = file_size
        self.file_name = file_name

    @classmethod
    def creator(cls, *args, **kwargs):
        """
        Used to create a handler class with the required parameters to facilitate file transfer.
        """
        def _handler_creator(request, client_address, server):
            cls(request, client_address, server, *args, **kwargs)
        return _handler_creator
    
    def handle(self):
        data = b''
        with open(f"./{self.client_name}/{self.file_name}", 'wb') as file:
            data = self.request.recv(file_size)
            file.write(data)
        self.request.send(f"{commands.Success()}".encode('ascii'))
