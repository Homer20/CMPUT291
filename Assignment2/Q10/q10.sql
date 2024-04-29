SELECT DISTINCT m.email
FROM borrowings b
JOIN book_info bi ON b.book_id = bi.book_id
JOIN members m ON b.member = m.email
WHERE bi.rating > 3.5 AND bi.reqcnt > (SELECT AVG(reqcnt) FROM book_info)
AND b.book_id NOT IN (
    SELECT book_id FROM book_info WHERE rating <= 3.5 OR reqcnt <= (SELECT AVG(reqcnt) FROM book_info)
);
