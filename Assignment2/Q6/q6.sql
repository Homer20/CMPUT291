SELECT b.book_id, b.title, COUNT(DISTINCT br.bid) AS borrow_count
FROM books b
JOIN borrowings br ON b.book_id = br.book_id
LEFT JOIN waitlists w ON b.book_id = w.book_id
WHERE b.pyear <= 2015
GROUP BY b.book_id, b.title
HAVING borrow_count >= 1
AND borrow_count >= 2 * COUNT(DISTINCT w.wid)
ORDER BY borrow_count DESC;
