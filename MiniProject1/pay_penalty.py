import sqlite3


def pay_penalty(filename, email):

    # Connecting to the database
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    
    # This loop runs until the user is done paying
    while True:
        # Query finds the unpaid penalties
        c.execute('''
                        SELECT pid, amount, paid_amount
                        FROM penalties p
                        JOIN borrowings b
                        ON p.bid = b.bid
                        WHERE member=? AND paid_amount < amount;''', (email,))
        unpaid_penalties = c.fetchall()
        
        # Return if the user has no penalties
        if not unpaid_penalties:
            print("\n")
            print("You have no unpaid penalties. Thank you for returning your books on time!")
            conn.close()
            return False
        else:
            print("\n")
            print("Unpaid Penalties:")

            # Listing all of the penalties the user has
            for penalty in unpaid_penalties:
                print("Penalty ID: {}, Amount owed: {}, Paid amount: {}".format(penalty[0], penalty[1], penalty[2]))
            
            # Loop is for error checking the user input
            # User selects which penalty they want to pay
            while True:
                try:
                    penalty_id = int(input("Enter the penalty ID you want to pay (or enter 0 to go back to the menu): "))
                    if penalty_id == 0:
                        conn.close()
                        return False
                    
                    # Error checking
                    if penalty_id not in [p[0] for p in unpaid_penalties]:
                        raise ValueError
                    break
                except ValueError:
                    print("Enter a valid penalty ID.")

            # Query to show the remaining amount they have to pay
            c.execute('''
                    SELECT amount - paid_amount
                    FROM penalties
                    WHERE pid = ?''', (penalty_id,))
            remaining_amount = c.fetchone()[0]

            # This loop is for error checking the user input
            while True:
                try:
                    payment_amount = float(input("Enter the payment amount: "))
                    if payment_amount <= 0:
                        raise ValueError("Payment amount must be a greater than zero!")
                    if payment_amount > remaining_amount:
                        raise ValueError("Payment amount exceeds the remaining debt!")
                    break
                except ValueError:
                    print("Please enter a valid amount")

            # Query to process the payment and update the database accordingly
            c.execute('''
                    UPDATE penalties
                    SET paid_amount = paid_amount + ?
                    WHERE pid = ? AND bid IN (
                        SELECT bid
                    FROM borrowings
                    WHERE member = ?
                    )
                    ''', (payment_amount, penalty_id, email))
            conn.commit()
            print("Payment successful.")

            # Calculate the remaining amount they have to pay
            remaining_amount -= payment_amount
            print("Remaining penalty amount for Penalty ID {}: {}".format(penalty_id, max(0, remaining_amount)))

            # If the user pays the amount fully, return them to menu
            if remaining_amount == 0:
                print("Thank you for your payment. Have a nice day!")
                conn.close()
                return False

            # Prompting the user to pay again
            pay_again = input('Do you want to pay again? Y/N: ').lower()

            if pay_again != "yes" and pay_again != "y":
                conn.close()
                return False
                
