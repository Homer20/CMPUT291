SELECT b.book_id, b.title, b.pyear AS publish_year
FROM books b
JOIN (SELECT book_id,
RANK() OVER (ORDER BY COUNT(*) DESC) AS borrow_rank
FROM borrowings
GROUP BY book_id) 
AS ranked_books
ON b.book_id = ranked_books.book_id
WHERE ranked_books.borrow_rank <= 3;
