"""
Author: Johnathan Van-Doninck
Date: April 25th, 2022

A file containing all self made exceptions for parsing, permission,
and validation errors.
"""

class InvalidRequestError(Exception):
    def __init__(self, message = "Error: Invalid request. See documentation."):
        self.message = message
        super().__init__(message)

class UsernameInUse(Exception):
    def __init__(self, message = "Error: Username already in use."):
        self.message = message
        super().__init__(message)

class MailInUse(Exception):
    def __init__(self, message = "Error: Email address already in use."):
        self.message = message
        super().__init__(message)