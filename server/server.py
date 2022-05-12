"""
Author: Johnathan Van-Doninck
Date: May 12th, 2022

Full server, implementing the request port and the upload/download port.
"""

from socketserver import ThreadingTCPServer
from threading import Thread
from request_port import RequestHandler
from os import system
from sys import exit

VERSION = "Simplifile Server Management Shell, Version b0.0.1"

def help():
    print("help - print this help message")
    print("clear - clear the screen")
    print("version - print the programme version")
    print("exit - shutdown the server and exit")


def clear():
    system("clear")

def version():
    print(VERSION)

def main():
    with ThreadingTCPServer((HOST, PORT), RequestHandler) as server:
        server_thread = Thread(target=server.serve_forever)
        print("Server thread created...")
        server_thread.daemon = True
        print("Thread daemonized...")
        server_thread.start()
        print(f"Server started on thread {server_thread.name}")
        print("Enter 'help' for more information.")
        while True:
            man_com = input("# ")
            if man_com == "help": help()
            elif man_com == "version": version()
            elif man_com == "clear": clear()
            elif man_com == "exit": exit()
            else: print("Unknown command.")