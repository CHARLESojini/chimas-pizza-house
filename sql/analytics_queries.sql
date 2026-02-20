-- Query 1: Total sales revenue per store
SELECT 
    s.store_id,
    s.address,
    s.city,
    SUM(o.total_amount) AS total_revenue
FROM Orders o
INNER JOIN Stores s ON o.store_id = s.store_id
GROUP BY s.store_id, s.address, s.city
ORDER BY total_revenue DESC;

-- Query 2: Top 10 most valuable customers by spending
SELECT
    c.first_name,
    c.last_name,
    c.email,
    SUM(o.total_amount) AS total_spent
FROM Orders o
INNER JOIN Customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email
ORDER BY total_spent DESC
LIMIT 10;

-- Query 3: Most popular menu item by sold 
SELECT
    m.item_id,
    m.name,
    SUM(oi.quantity) AS quantity_sold
FROM Order_Items oi
INNER JOIN Menu_Items m ON oi.item_id = m.item_id
GROUP BY m.item_id, m.name
ORDER BY quantity_sold DESC
LIMIT 1;

-- Query 4: Average order value
SELECT
    AVG(total_amount) AS average_order_value
FROM Orders;

-- Query 5: Busiest hours of the day
SELECT
    EXTRACT(HOUR FROM order_timestamp) AS order_hour,
    COUNT(*) AS total_orders
FROM Orders
GROUP BY order_hour
ORDER BY total_orders DESC;





