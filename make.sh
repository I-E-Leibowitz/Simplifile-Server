#!/bin/bash

# Author - Johnathan Van-Doninck
# Date - May 7th, 2022
# Make script for setting up project dependencies, such as
# the API, the database, the root of the server, etc.
#
# Positional arguments: 
# $1 - server root, defaults to /home/{user}/simplifile/
# $2 - database file name, defaults to /home/{user}/simplifile/Simplifile

# Function definitions
verify_exists() {       # Verifies a given program exists on the computer.
    whereis_out=$(whereis $1)
    if [[ "$1:" = "$whereis_out" ]]
    then
        return 0
    else
        return 1
    fi
}
verify_requirements() {
    verify_exists $1
    if [[ $? -eq 0 ]]
    then
        echo "error: dependency $1 could not be located. Please resolve issue and try again."
        reqs_met=0
        let GLOBAL error_code+=1
    fi
}
test_fun() {
    echo $@
}
# ---
# Positional argument parsing
error_code=0
if [[ $1 -eq 0 ]]       # Checks if positional argument 1 is used, defaults if not.
then
    user = whoami
    root_path="/home/$user/simplifile/"
else
    root_path=$1
fi
if [[ $2 -eq 0 ]]       # Checks if positional argument 2 is used, defaults if not.
then
    db_path="~/simplifile/Simplifile"
else
    db_path=$1
fi
# ---
# Requirement verification
reqs_met=1
verify_requirements "python3"
verify_requirements "sqlite3"
# ---
# Environment setup
if [[ reqs_met -eq 1 ]]
then
    echo "Working..."
    mkdir root_path
    mv ./ $root_path
    cd $root_path
    echo "Created server root..."
    echo "export PATH=$PATH:\"$root_path/simplifile_api\"" > /home/$user/.bashrc
    echo "Added API to PATH variable..."
    # TODO: Create database
    exec 
    # TODO: Add server files to server root
    source "~/.bashrc"

else
    echo "Exiting with error code $error_code"
fi