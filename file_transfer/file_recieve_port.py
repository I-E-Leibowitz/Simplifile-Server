"""
Author: Johnathan Van-Doninck
Date: May 2nd, 2022

Receives files from client
"""

from socketserver import BaseRequestHandler, TCPServer
from os import system
import time

class FileRecieveHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server, file_size, file_path):
        self.file_size = file_size
        self.file_path = file_path
        super().__init__(request, client_address, server)

    @classmethod
    def Creator(cls, *args, **kwargs):
        """
        Used to create a handler class with the required parameters to facilitate file transfer.
        """
        def _HandlerCreator(request, client_address, server):
            cls(request, client_address, server, *args, **kwargs)
        return _HandlerCreator
    
    def handle(self):
        print("In Handle")
        timer = time.time()
        try:
            with open(self.file_path, 'bw') as file:
                print("Awaiting file...")
                time.sleep(0.01)
                data = b''
                while True:
                    print("Running.")
                    data = self.request.recv(self.file_size)
                    print(data)
                    if not data: break
                    file.write(data)
                print(time.time() - timer)
                print("Done.")
        except Exception as e:
            print(e)
            system(f"rm -r {self.file_path}")

if __name__ == '__main__':
    with TCPServer(("localhost", 55446), FileRecieveHandler.Creator(114, './README.md')) as server:
        server.serve_forever()