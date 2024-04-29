SELECT books.book_id, books.title, books.author, COUNT(borrowings.book_id) AS num_borrowings, MAX(borrowings.start_date) AS recent_date
FROM books
LEFT JOIN borrowings ON books.book_id = borrowings.book_id
WHERE books.pyear > 2001
GROUP BY books.title
