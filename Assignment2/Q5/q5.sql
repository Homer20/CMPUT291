SELECT b.book_id, b.title, AVG(r.rating) AS avg_review_rating
FROM books b
JOIN reviews r ON b.book_id = r.book_id
GROUP BY b.book_id, b.title
HAVING COUNT(r.rid) >= 2
ORDER BY avg_review_rating DESC
LIMIT 3;
