import sqlite3

def view_profile(filename, email):

    conn = sqlite3.connect(filename)
    c = conn.cursor()

    while True:
        print("\nPersonal Information (1)\nNumber of Books Borrowed \ Returned (2)\nPenalty Information (3)\nMain Menu(4)")
        # To handle NULL cases and other non-valid input
        try:
            user_input = int(input("Please type an option from above: "))
        except ValueError:
            print("\nPlease enter a valid option")
            continue
        if user_input == 1:
            # personal info: name, email byear
            c.execute('SELECT name, email, byear FROM members WHERE email=?;', (email,)) # trailing tupule
            rows = c.fetchall()
            print("\nName: {}\nEmail: {}\nBirthyear: {}".format(rows[0][0], rows[0][1], rows[0][2])) # Each row is structured like: [Name, Email, Byear]
        elif user_input == 2:
            # borrowing info
            # All borrowings where member = email, borrowing history
            # Sum of current borrowings: end_date IS NULL
            # Sum of current borrowings where it has been >= 20 days from start date
            c.execute('''
                      SELECT COUNT(*) as borrowed, SUM(CASE WHEN end_date IS NULL THEN 1 ELSE 0 END) as current,
                      SUM(CASE WHEN julianday('now') - julianday(start_date)> 20 AND end_date IS NULL THEN 1 ELSE 0 END) as overdue
                      FROM borrowings
                      WHERE member=?;''', (email,))
            rows = c.fetchall()
            print("\nTotal borrowings: {}\nCurrent borrowings: {}\nOverdue borrowings: {}".format(rows[0][0], rows[0][1], rows[0][2]))
        elif user_input == 3:
            # penalty info
            # Total # of active penalties (where paid < penalty)
            # Debt that the member still owes (penalty-paid)
            c.execute('''
                      SELECT SUM(CASE WHEN (paid_amount < amount) THEN 1 ELSE 0 END) as active, SUM(CASE WHEN (paid_amount < amount) THEN (amount-paid_amount) ELSE 0 END) as debt
                      FROM penalties p
                      JOIN borrowings b
                      ON p.bid = b.bid
                      WHERE member=?;''', (email,))
            rows = c.fetchall()
            print("\nActive penalties: {}\nUnpaid debts: {}".format(rows[0][0], rows[0][1]))
        elif user_input == 4:
            break # Return to Menu
        else:
            print("Sorry, invalid input. Please try again.")