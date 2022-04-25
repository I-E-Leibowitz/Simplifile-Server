"""
Author: Johnathan Walter Van-Doninck
Date: April 25th, 2022

A service class that provides utilities to parse commands received by the server.
"""

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
    def _parser(cmd_list):              # Used to parse into an object and validate it.
        try:
            command = class_map[ cmd_list[ 0 ] ](cmd_list[ 1 ], cmd_list[ 0 ], cmd_list[2])
            if command.validate() and command.validate_arguments():
                return command
            else:
                return exceptions.InvalidRequestError()

        except KeyError:
            return exceptions.InvalidRequestError()

    @staticmethod
    def parser(command: str):   # Used to parse from raw text into manageable bits.
        if command[-1] != '\x04':
            return exceptions.InvalidRequestError()
        command_list = [ string.split(": ")[1] for string in command.split("\n") ]
        return _parser(command_list)
        
