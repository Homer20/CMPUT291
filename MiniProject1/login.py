# Purpose: Login page / Registration page
# Works for the most part, may need to add addtional requirements
# References: https://docs.python.org/3/library/msvcrt.html
# https://realpython.com/python-flush-print-output/

import sqlite3
import msvcrt

# This function replaces the typed password with *
def custom_getpass(prompt='Password: '):
    # Showing the password instantly by using flush
    print(prompt, end='', flush=True)
    password = ''

    # Loop that runs until the user presses enter
    while True:
        # Getting the character from the keyboard
        key = msvcrt.getch()
        # Converting the character from bytes to string
        key = key.decode('utf-8')

        # If the enter key is pressed then break out of the loop
        if key == '\r' or key == '\n':
            print('')
            break

        # Handling the case when the user presses backspace and removes a character
        elif key == '\x08': # Backspace
            if password:
                password = password[:-1]
                print('\b \b', end='', flush=True)

        # Replacing the entered characters with the astericks so the password appears hidden
        else:
            password += key
            print('*', end='', flush=True)

    return password


def login(db_file):
    # Connecting to the database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    while True:
        print("Welcome to the Library!")
        temp = input("Are you a registered user? (y/n): ")

        if temp.lower() == 'y':
            email = input("Enter email: ")
            passwd = custom_getpass("Enter password: ")
            c.execute('''SELECT * FROM members
            WHERE email = ? AND passwd = ?;''', (email, passwd))

            result = c.fetchone()

            if result:
                print("Welcome back!")
                return email
            else:
                print("Sorry, user not found. Please try again")

        elif temp.lower() == 'n':
            name = input("Enter your full name: ")
            byear = input("Enter your birth year: ")
            while True:
                try:
                    byear = int(byear)
                    break
                except ValueError:
                    byear = input("Enter a valid birth year: ")
            faculty = input("Enter your faculty: ")

            email = input("Please enter your email: ")
            while '@' not in email or '.' not in email:
                email = input("Please enter a valid email: ")

            passwd = custom_getpass("Enter password: ")

            c.execute('''INSERT INTO members VALUES
                    (?, ?, ?, ?, ?);''',
                    (email, passwd, name, byear, faculty))
            conn.commit()
            return email
        else:
            print("Sorry, invalid input. Please try again.")
