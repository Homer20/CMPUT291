CREATE VIEW book_info 
AS SELECT 
    b.book_id,
    b.title,
    COUNT(DISTINCT r.rid) AS revcnt,
    IFNULL(AVG(IFNULL(r.rating, 0)), 0) AS rating,
    IFNULL(AVG(CASE WHEN strftime('%Y', r.rdate) = '2023' THEN r.rating ELSE NULL END), 0.0) AS rating23,
    IFNULL(COUNT(DISTINCT br.bid), 0) + IFNULL(COUNT(DISTINCT wl.wid), 0) AS reqcnt
FROM books b
LEFT JOIN reviews r ON b.book_id = r.book_id
LEFT JOIN borrowings br ON b.book_id = br.book_id
LEFT JOIN waitlists wl ON b.book_id = wl.book_id
GROUP BY b.book_id, b.title;

SELECT * FROM book_info;
