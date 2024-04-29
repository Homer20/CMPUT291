import sqlite3
import datetime

def return_book(filename, email):
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    # Display user's current borrowings
    c.execute('''SELECT bid, title, start_date, date(start_date, '+20 days') as return_deadline
                 FROM borrowings JOIN books ON borrowings.book_id = books.book_id
                 WHERE member = ? AND end_date IS NULL;''', (email,))
    borrowings = c.fetchall()

    # Display borrowings to user
    for b in borrowings:
        print(f"Borrowing ID: {b[0]}, Book Title: {b[1]}, Borrowing Date: {b[2]}, Return Deadline: {b[3]}")

    # Select borrowing to return
    bid_to_return = input("Enter the borrowing ID of the book to return: ")

    # Record returning date as today's date
    returning_date = datetime.date.today()

    # Check if the selected borrowing ID is valid
    valid_bids = [b[0] for b in borrowings]
    try:
        if bid_to_return.lower() == 'q':
            return  # Return to the menu
        bid_to_return = int(bid_to_return)
        if bid_to_return not in valid_bids:
            print("Invalid borrowing ID. Please try again.")
            conn.close()
            return
    except ValueError:
        print("Invalid input. Please enter a valid borrowing ID.")
        conn.close()
        return
    #goes back to the main menu if anything is wrong
    #or if the user wants to go back they need to click q 
    #or a wrong answer

    # Calc and apply penalty for late return
    c.execute('''SELECT date(start_date, '+20 days') as return_deadline
                 FROM borrowings
                 WHERE bid = ?;''', (bid_to_return,))
    return_deadline_str = c.fetchone()[0]
    #compare
    return_deadline = datetime.datetime.strptime(return_deadline_str, '%Y-%m-%d').date()
    if returning_date > return_deadline:
        delayed_days = (returning_date - return_deadline).days
        penalty = delayed_days * 1  # $1 per delayed day
        c.execute('''INSERT INTO penalties (bid, amount, paid_amount)
                     VALUES (?, ?, ?);''', (bid_to_return, penalty, 0))

    # Record return date in borrowings table instead of null
    c.execute('''UPDATE borrowings
                 SET end_date = ?
                 WHERE bid = ?;''', (returning_date, bid_to_return))

    # review
    write_review = input("Would you like to write a review for this book? (y/n): ")
    if write_review.lower() == 'y':
        book_id = c.execute('''SELECT book_id
                                FROM borrowings
                                WHERE bid = ?;''', (bid_to_return,)).fetchone()[0]
        while True:
            try:
                rating = int(input("Enter your rating (1-5): "))
                if rating < 1 or rating > 5:
                    raise ValueError("Rating must be between 1 and 5")
                break
            except ValueError:
                print("Please enter a valid number.")
                
        review_text = input("Enter your review text: ")
        review_date = datetime.date.today()
        c.execute('''INSERT INTO reviews (book_id, member, rating, rtext, rdate)
                     VALUES (?, ?, ?, ?, ?);''', (book_id, email, rating, review_text, review_date))

    conn.commit()
    conn.close()
