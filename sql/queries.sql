SELECT id, name, phone FROM clients ORDER BY name;

SELECT id, name, specialization FROM designers ORDER BY name;

SELECT id, design_type, price, deadline FROM orders WHERE is_urgent = 1 ORDER BY deadline;

SELECT id, design_type, price FROM orders WHERE price >= ? ORDER BY price DESC;

SELECT o.id, o.design_type, o.price, c.name AS client_name, d.name AS designer_name
FROM orders o
JOIN clients c ON o.client_id = c.id
JOIN designers d ON o.designer_id = d.id
ORDER BY o.deadline;

SELECT o.id, o.design_type, d.name AS designer_name
FROM orders o
JOIN designers d ON o.designer_id = d.id
WHERE o.client_id = ?;

SELECT s.id, s.name AS stage_name, s.status, o.id AS order_id, o.design_type
FROM stages s
JOIN orders o ON s.order_id = o.id;

SELECT COUNT(*) AS orders_count FROM orders;

SELECT COUNT(*) AS urgent_count FROM orders WHERE is_urgent = 1;

SELECT d.name AS designer_name, COUNT(o.id) AS orders_count, SUM(o.price) AS total_price
FROM designers d
LEFT JOIN orders o ON o.designer_id = d.id
GROUP BY d.id, d.name
ORDER BY total_price DESC;

SELECT status, COUNT(*) AS stages_count FROM stages GROUP BY status;

SELECT d.name AS designer_name, COUNT(o.id) AS orders_count
FROM designers d
JOIN orders o ON o.designer_id = d.id
GROUP BY d.id, d.name
HAVING COUNT(o.id) > 1;