"""
Author: Johnathan Van-Doninck
Date: May 23rd, 2022

A set of functions for communicating with the database.
"""

import sqlite3

def add_file(username, filename, file_size, file_hash):
    db = sqlite3.connect("/home/luciferin/Documents/FML/Simplifile-Server/database/simplifile.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO Files VALUES (?, ?, ?, ?)", (username, filename, file_size, file_hash))
    db.commit()

def remove_from_table(table: str, field: str, key: str) -> bool:
    db = sqlite3.connect("/home/luciferin/Documents/FML/Simplifile-Server/database/simplifile.db")
    cursor = db.cursor()
    cursor.execute("DELETE FROM (?) WHERE (?)=(?);", (table, field, key))
    db.commit()

def get_user(username, password):
    db = sqlite3.connect("/home/luciferin/Documents/FML/Simplifile-Server/database/simplifile.db")
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Users\nWHERE Username=(?) AND Password=(?)', (username, password))

def add_user(username: str, email: str, password: str):
    db = sqlite3.connect("/home/luciferin/Documents/FML/Simplifile-Server/database/simplifile.db")
    cursor = db.cursor()
    cursor.execute('INSERT INTO Users\n VALUES ((?), (?), (?), 1)', (username, email, password))
    db.commit()

def add_user_simple(username: str, email: str, password: str):
    db = sqlite3.connect("/home/luciferin/Documents/FML/Simplifile-Server/database/simplifile.db")
    cursor = db.cursor()

    db.commit()

def get_users():
    db = sqlite3.connect("/home/luciferin/Documents/FML/Simplifile-Server/database/simplifile.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users")
    return cursor.fetchall()