"""
Author: Johnathan Walter Van-Doninck
Date: April 25th, 2022

A service class that provides utilities to parse commands received by the server.
"""

from sys import path
path.append("/home/luciferin/Documents/Fuck my life/Simplifile-Server/")    # Temporary, neccessary for python to recognize the api package.
from simplifile_api import commands, exceptions

class Parser:
    class_map = {
        "upload":   commands.Upload,        # 0
        "download": commands.Download,      # 1
        "addusr":   commands.CreateUser,    # 2
        "delusr":   commands.DeleteUser,    # 3
        "chgpass":  commands.ChangePassword # 4
    }

    @staticmethod
    def _parser(cmd_list: list()):          # Used to parse into an object and validate it.
        try:
            command = Parser.class_map[ cmd_list[ 0 ] ](int(cmd_list[ 1 ]), cmd_list[ 0 ], cmd_list[2:])
            if command.validate() and command.validate_arguments():
                return command
            else:
                return exceptions.InvalidRequestError()

        except KeyError:
            return exceptions.InvalidRequestError()
        except TypeError:
            return exceptions.InvalidRequestError()

    @staticmethod
    def parser(command: str):   # Used to parse from raw text into manageable bits.
        if command[-1] != '\x04':
            return exceptions.InvalidRequestError()
        command_list = [ string.split(": ")[1] for string in command[:-1].split("\n") ]
        return Parser._parser(command_list)
        