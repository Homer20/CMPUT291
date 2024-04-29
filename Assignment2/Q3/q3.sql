SELECT borrowings.bid, borrowings.member
FROM borrowings, waitlists
WHERE julianday(end_date) - julianday(start_date) > 14
AND waitlists.priority < "5"
