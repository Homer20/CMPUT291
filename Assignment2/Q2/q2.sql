SELECT borrowings.bid, member, end_date
FROM borrowings, members, books
WHERE borrowings.member = members.email
AND borrowings.book_id = books.book_id
AND members.faculty == "CS"
AND (LOWER(books.author) = LOWER("John") OR LOWER(books.author) = LOWER("Marry"));
