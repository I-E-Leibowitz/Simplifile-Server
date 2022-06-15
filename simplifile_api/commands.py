"""
Author: Johnathan Van-Doninck
Date: November 28th, 2021

All commands will be stored here, and accessed through this module.
"""

# Imports
from socketserver import TCPServer
from os import system
from database import interface
from dataclasses import dataclass
from simplifile_api.exceptions import UsernameInUse, MailInUse
from file_transfer.file_recieve_port import FileRecieveHandler
from file_transfer.file_send_port import FileSendHandler
from socket import socket, AF_INET, SOCK_STREAM


@dataclass
class _Command:
    """
    A skeleton class that provides the base for all other command classes.
    """
    id: int
    command: str = None
    args: list = None

    def validate(self, ext_command: tuple) -> bool:
        """
        Returns true if the id and the command are the same as the ones fed through ext_command.
        """
        return (self.id, self.command) == ext_command

    def execute(self):
        """
        Passes the command to the server for handling. Is empty here.
        """
        pass

    def validate_arguments(self, num_of_args: int) -> bool:
        """
        Validates the arguents, ensuring they are valid for the specific function. Is empty here.
        """
        return len(self.args) == num_of_args
# ---

@dataclass
class Upload(_Command):
    def validate(self) -> bool:
        """
        Returns true if the id and the command match the valid ones for the upload command.
        """
        return super().validate((0, "upload"))

    def execute(self):
        """
        Passes the command to the server for handling. Currently WIP.

        args: (0) size of file (1) user to which the file belongs (2) file name
        """
        filename = self.args[2].split('/')[-1]
        with TCPServer(("0.0.0.0", 55446), FileRecieveHandler.Creator(int(self.args[0]), f"../server/{self.args[1]}/{filename}")) as server:
            server.handle_request()
            interface.add_file(self.args[1], self.args[2], self.args[0], self.args[3])

        
            
    def validate_arguments(self):
        """
        Validates the arguents, ensuring they are valid for the specific function. Is empty here.
        """ 
        return super().validate_arguments(4)
# ---

@dataclass
class Download(_Command):
    def validate(self) -> bool:
        """
        Returns true if the id and the command match the valid ones for the Download command.
        """
        return super().validate((1, "download"))
    
    def execute(self):
        """
        Passes the command to the server for handling. Currently WIP.
        """
        filename = self.args[1].split('/')[-1]
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(("10.100.102.8", 55446))
            with open(f"{self.args[0]}/{filename}", 'br') as file:
                data = b'/'
                while data != b'':
                    data = file.read(1)
                    sock.send(data)
                    print(data)
                # sock.sendall(bytes(f"{commands.Success()}", 'ascii'))
                print("Done")
    
    def validate_arguments(self):
        """
        Validates the arguents, ensuring they are valid for the specific function. Is empty here.
        """
        return super().validate_arguments(2)
# ---

@dataclass
class CreateUser(_Command):
    def validate(self) -> bool:
        """
        Returns true if the id and the command match the valid ones for the CreateUser command.
        """
        return super().validate((2, "addusr"))

    def execute(self):
        """
        Passes the command to the server for handling. Currently WIP
        All neccessary details (username: str, email: str, password: str)
        are passed through the self.args field, in a yet to be determined order.
        """
        user = interface.get_user(self.args[0], self.args[1])
        print(user)
        # if not userExist:
        #     return UsernameInUse
        # elif not mailExist:
        #     return MailInUse
        # else:
        interface.add_user(self.args[0], self.args[1], self.args[2])
        print("a")
        system(f"mkdir ./{self.args[0]}")   # INCREDIBLY INSECURE. Implement input checks.
        return Success

    def validate_arguments(self):
        """
        Validates the arguents, ensuring they are valid for the specific function. Is empty here.
        """
        return super().validate_arguments(3)
# ---

@dataclass
class DeleteUser(_Command):
    def validate(self) -> bool:
        """
        Returns true if the id and the command match the valid ones for the DeleteUser command.
        """
        return super().validate((3, "udelete"))

    def execute(self):
        """
        Passes the command to the server for handling. Currently WIP.
        All neccessary details (email:str, username: str, password: str)
        are passed through the self.args field
        """
        password = interface.findUsers(self.args[0], 'password')
        if password == self.args[2]:
            interface.delUser(self.args[0], self.args[1])
            system(f"rm -r ./{self.args[1]}")   # INCREDIBLY INSECURE. Implement input checks.
            return Success
        else:
            return Abort

    def validate_arguments(self):
        """
        Validates the arguents, ensuring they are valid for the specific function.
        """
        return super().validate_arguments(3)
# ---

@dataclass
class ChangePassword(_Command):
    def validate(self) -> bool:
        """
        All necessary details (email: str, password: str, new_pass: str)
        """
        return super().validate((4, "uchange"))

    def execute(self):
        """
        Passes the command to the server for handling. Currently WIP
        """
        if interface.findUsers(f'{self.args[0]}', 'password') == self.args[2]:
            interface.changeUsers(f'{self.args[0]}', 'password', value)
            return Success
        return Abort

    def validate_arguments(self):
        """
        Validates the arguents, ensuring they are valid for the specific function.
        """
        return super().validate_arguments(3)
# ---

@dataclass
class ValidateUser(_Command):
    def validate(self) -> bool:
        return super().validate((5, "uvalidate"))
    
    def execute(self):
        if interface.find_user(args[0]):
            return True
        else: return False
    
    def validate_arguments(self):
        return super().validate_arguments(2)
# ---
@dataclass
class Abort(_Command):
    """
    This class is unique - it tells the server to abort whatever operation it was meant to do.
    Only used in cases where the received command is invalid in one way or another (Invalid user ID,
    Invalid syntax, etc.)
    """
    def validate(self) -> bool:
        """
        Returns true if the id and the command match the valid ones for the Abort command.
        """
        return super().validate((-1, "abort"))
    
    def execute(self):
        """
        Passes the command to the server for handling. Currently WIP
        """
        return super().execute()

    def validate_arguments(self):
        """
        Validates the arguents, ensuring they are valid for the specific function. Is empty here.
        """
        return super().validate_arguments()
# ---

@dataclass
class Success(_Command):
    """
    Tells the client programme the operation was performed successfully, so that the user can be moved to the next screen.
    """
    def validate(self) -> bool:
        return super().validate((999, "success"))
    
    def execute(self):
        """
        Passes the command to the server for handling. Currently WIP
        """
        return super().execute()

    def validate_arguments(self):
        """
        Validates the arguents, ensuring they are valid for the specific function. Is empty here.
        """
        return super().validate_arguments()