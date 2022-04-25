"""
Author: Johnathan Van-Doninck
Date: November 28th, 2021

All commands will be stored here, and accessed through this module.
"""

# Imports
from os import system
from database import db_interface
from dataclasses import dataclass
from exceptions import UsernameInUse, MailInUse
from server.transfer_port import *


@dataclass
class _Command:
    """
    A skeleton class that provides the base for all other command classes.
    """
    id: int
    command: str = None
    args: str = None

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

        args: (0) location on server (1) size of file (2) user to which the file belongs
        """
        
            
    def validate_arguments(self):
        """
        Validates the arguents, ensuring they are valid for the specific function. Is empty here.
        """ 
        return super().validate_arguments(3)
# ---

@dataclass
class Download(_Command):
    def validate(self) -> bool:
        """
        Returns true if the id and the command match the valid ones for the Download command.
        """
        return super().validate((1, "download"))
    
    def execute(self, data):
        """
        Passes the command to the server for handling. Currently WIP.
        """
        return super().execute()
    
    def validate_arguments(self):
        """
        Validates the arguents, ensuring they are valid for the specific function. Is empty here.
        """
        return super().validate_arguments(3)
# ---

@dataclass
class CreateUser(_Command):
    def validate(self) -> bool:
        """
        Returns true if the id and the command match the valid ones for the CreateUser command.
        """
        return super().validate((2, "ucreate"))

    def execute(self):
        """
        Passes the command to the server for handling. Currently WIP
        All neccessary details (email: str, username: str, password: str)
        are passed through the self.args field, in a yet to be determined order.
        """
        user = db_interface.findUsers(self.args[0], 'username')
        mail = db_interface.findUsers(self.args[0], 'email')
        print(user)
        print(mail)
        userExist = user == self.args[1]
        mailExist = mail == self.args[0]
        print(mailExist)
        print(userExist)
        if not userExist:
            return UsernameInUse
        elif not mailExist:
            return MailInUse
        else:
            db_interface.addUser(self.args[0], self.args[1], self.args[2])
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
        password = db_interface.findUsers(self.args[0], 'password')
        if password == self.args[2]:
            db_interface.delUser(self.args[0], self.args[1])
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
        if db_interface.findUsers(f'{self.args[0]}', 'password') == self.args[2]:
            db_interface.changeUsers(f'{self.args[0]}', 'password', value)
            return Success
        return Abort

    def validate_arguments(self):
        """
        Validates the arguents, ensuring they are valid for the specific function.
        """
        return super().validate_arguments(3)
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