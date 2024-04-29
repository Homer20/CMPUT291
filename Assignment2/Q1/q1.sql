SELECT DISTINCT members.name, waitlists.member
FROM waitlists, borrowings, members
WHERE waitlists.book_id = borrowings.book_id 
AND waitlists.member = borrowings.member 
AND waitlists.member = members.email;
