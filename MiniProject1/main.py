# Purpose: Main file
import sqlite3
import sys

# # from setup import setup_new_db # testing purposes
#from setup import setup_db # actual func.
from login import login
import sys
from menu import menu

def main():
    if len(sys.argv) < 2:
        print("Please provide the database filename as an argument.")
        return
    
    filename = sys.argv[1]
    email = login(filename)
    if email:
        menu(filename, email)

if __name__ == "__main__":
    main()