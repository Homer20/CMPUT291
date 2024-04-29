SELECT m.email, COUNT(p.pid) AS total_penalties, SUM(CASE WHEN IFNULL(p.paid_amount,0) >= p.amount THEN 1 ELSE 0 END) AS paid_penalties, SUM(CASE WHEN IFNULL(p.paid_amount, 0) >= p.amount THEN p.amount ELSE 0 END) AS total_paid_amount
FROM members m
LEFT JOIN borrowings b ON m.email = b.member
LEFT JOIN penalties p ON b.bid = p.bid
GROUP BY m.email, m.name
HAVING total_penalties > 0;
