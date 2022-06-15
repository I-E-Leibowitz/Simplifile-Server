"""
Author: Johnathan Van-Doninck
Date: May 12th, 2022

Full server, implementing the request port and the upload/download port.
"""

from os import system
from sys import exit, path
path.append('./..')
from socketserver import ThreadingTCPServer
from threading import Thread
from request_port import RequestHandler
from database import interface

VERSION = "Simplifile Server Management Shell, Version b0.0.1"
HOST = '0.0.0.0'
PORT = 55445

def help():
    print("help - print this help message")
    print("clear - clear the screen")
    print("version - print the programme version")
    print("exit - shutdown the server and exit")
    print("users - show users")
    print()

def exit_server(server: ThreadingTCPServer):
    server.shutdown()
    exit()

def clear():
    system("clear")

def version():
    print(VERSION)

def get_users():
    for value in interface.get_users():
        print(' | '.join([str(i) for i in value ]))

def add_user(username, email, password):
    interface.add_to_table(username, email, password)

def add_admin(username, email, password):
    interface.add_user_simple(username, email, password)


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
            man_com = man_com.split(' ')
            if man_com[0] == "help": help()
            elif man_com[0] == "version": version()
            elif man_com[0] == "clear": clear()
            elif man_com[0] == "exit": exit_server(server)
            elif man_com[0] == "users": get_users()
            elif man_com[0] == "addUser" and len(man_com) == 4: add_user(man_com[1], man_com[2], man_com[3])
            # elif man_com[0] == "addAdmin" and len(man_com) == 4: add_admin(man_com[1], man_com[2], man_com[3])
            else: print("Unknown command.")

if __name__ == '__main__':
    main()