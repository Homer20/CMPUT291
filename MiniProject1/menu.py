# Purpose: Main menu screen after login

import sqlite3
from view_profile import view_profile
from return_book import return_book
from book_search import book_search
from pay_penalty import pay_penalty

def menu(filename, email):

    while True:
        print("\nYou are now in the library database menu.\n")
        print("View Profile (1) \nReturn a Book (2) \nSearch for Books (3) \nPay a Penalty (4)")
        try:
            user_input = int(input("Please type an option from above: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if user_input == 1:
           view_profile(filename, email)
        elif user_input == 2:
            return_book(filename, email)
        elif user_input == 3:
            book_search(filename, email)
        elif user_input == 4:
            if pay_penalty(filename, email):
                break
        else:
            print("Sorry, invalid input. Please try again.")

# Add the following lines at the end of your script
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <database_filename>")
        sys.exit(1)
    filename = sys.argv[1]
    email = input("Enter your email: ")  # Assuming the user needs to enter their email to login
    menu(filename, email)
