import sqlite3
import datetime

def book_search(filename, email):
    # The user should be able to enter a keyword and the system 
    # should retrieve all books in which the title or author contain the keyword.
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    keyword = input("\nSearch: ")

    # Sorted by title match
    c.execute('''SELECT b.book_id, title, author, pyear, IFNULL(AVG(r.rating), 'NA') as rating, (CASE WHEN (bo.book_id IS NOT NULL AND bo.end_date IS NULL) THEN 'Not available' ELSE 'Available' END) as availability
              FROM books b
              LEFT JOIN borrowings bo
              ON b.book_id = bo.book_id
              LEFT JOIN reviews r
              ON b.book_id = r.book_id
              WHERE LOWER(title) LIKE LOWER(?)
            GROUP BY b.book_id, title, author, pyear, bo.book_id, bo.end_date 

              ORDER BY b.title ASC;
              ''', ('%' + keyword +'%',))
    
    rows = c.fetchall()
    
    if rows: # If there are results
        print("\nTitle(s) matching:")
        for row in rows: # BID, title, author, pyear, avg rating, availability (has bid or not)
            if row[0] is not None:
            # case if (book_id in borrowings) then 1 else 0
                print("\nBook ID: {}\nTitle: {}\nAuthor: {}\nPublishing Year: {} \nRating: {} \nAvailability: {} ".format(row[0], row[1], row[2], row[3], row[4], row[5]))
    else: # No results
        print("\nNo titles matching.")

    # Sorted by author match
    c.execute('''SELECT b.book_id, title, author, pyear, IFNULL(AVG(r.rating), 'NA') as rating, (CASE WHEN (bo.book_id IS NOT NULL AND bo.end_date IS NULL) THEN 'Not available' ELSE 'Available' END) as availability
              FROM books b
              LEFT JOIN borrowings bo
              ON b.book_id = bo.book_id
              LEFT JOIN reviews r
              ON b.book_id = r.book_id
              WHERE LOWER(author) LIKE LOWER(?)
              GROUP BY b.book_id, title, author, pyear, bo.book_id, bo.end_date
              ORDER BY b.author ASC;
              ''', ('%' + keyword +'%',))
    # Include bo.book_id and bo.end_date to ensure CASE is applied correctly. Otherwise only one entry would appear, even if there were other valid entries.
    rows = c.fetchall()
    
    if rows: # There are results
        print("\n\nAuthor(s) matching:")
        for row in rows: # BID, title, author, pyear, avg rating, availability (has bid or not)
            # case if (book_id in borrowings) then 1 else 0
            if row[0] is not None:
                print("\nBook ID: {}\nTitle: {}\nAuthor: {}\nPublishing Year: {} \nRating: {} \nAvailability: {} ".format(row[0], row[1], row[2], row[3], row[4], row[5]))
    else: # There are no results
        print("\nNo authors matching.")

    #For each book, the system must display book id, title, author, publish year, average rating, 
    #and whether the book is available or on borrow. If a book is available, the user should be given an option
    # to borrow the book (As explained below).
        
     # Borrow a book
    bid_to_borrow = input("\nEnter the Book ID to borrow: ")

    # Check if book ID is valid
    c.execute('''SELECT COUNT(*) FROM books WHERE book_id = ?;''', (bid_to_borrow,))
    if c.fetchone()[0] == 0:
        print("Invalid Book ID. Please enter a valid Book ID.")
        return
    
    #check if the book is already borrowed
    c.execute('''SELECT COUNT(*) FROM borrowings WHERE book_id = ? AND end_date IS NULL AND member != ?;''', (bid_to_borrow, email))
    if c.fetchone()[0] > 0:
        print("This book is already borrowed.")
        return
    
    # Check if the book is already borrowed by the user
    c.execute('''SELECT COUNT(*) FROM borrowings WHERE book_id = ? AND member = ? AND end_date IS NULL;''', (bid_to_borrow, email))
    if c.fetchone()[0] > 0:
        print("You have already borrowed this book.")
        return
        
    #all errors are done

    c.execute('''SELECT MAX(bid) FROM borrowings;''')
    max_bid = c.fetchone()[0]
    bid = max_bid + 1 if max_bid is not None else 1

    #increments max bid to get a unique id

    start_date = datetime.date.today()
    end_date = None

    c.execute('''INSERT INTO borrowings (bid, member, book_id, start_date, end_date) VALUES (?, ?, ?, ?, ?);''', (bid, email, bid_to_borrow, start_date, end_date))
    print("Book borrowed successfully.")

    conn.commit()
    conn.close()
    




