USE text_to_sql_db;

-- Insert customers
INSERT INTO customers (name, email, city, country)
VALUES
('Aarav Sharma', 'aarav@gmail.com', 'Chandigarh', 'India'),
('Priya Verma', 'priya@gmail.com', 'Delhi', 'India'),
('Rahul Singh', 'rahul@gmail.com', 'Ludhiana', 'India'),
('Simran Kaur', 'simran@gmail.com', 'Amritsar', 'India'),
('Arjun Mehta', 'arjun@gmail.com', 'Mumbai', 'India'),
('Neha Kapoor', 'neha@gmail.com', 'Bangalore', 'India'),
('Rohan Gupta', 'rohan@gmail.com', 'Chandigarh', 'India'),
('Ananya Sharma', 'ananya@gmail.com', 'Delhi', 'India'),
('Karan Malhotra', 'karan@gmail.com', 'Pune', 'India'),
('Ishita Jain', 'ishita@gmail.com', 'Jaipur', 'India');


-- Insert products
INSERT INTO products (product_name, category, price)
VALUES
('Laptop Pro 14', 'Electronics', 85000.00),
('Wireless Mouse', 'Electronics', 1500.00),
('Mechanical Keyboard', 'Electronics', 4500.00),
('Office Chair', 'Furniture', 12000.00),
('Standing Desk', 'Furniture', 25000.00),
('Running Shoes', 'Sports', 5500.00),
('Yoga Mat', 'Sports', 1200.00),
('Backpack', 'Accessories', 2500.00),
('Smart Watch', 'Electronics', 15000.00),
('Water Bottle', 'Accessories', 800.00);


-- Insert orders
INSERT INTO orders
(customer_id, product_id, quantity, order_date, total_amount)
VALUES
(1, 1, 1, '2026-01-10', 85000.00),
(2, 2, 2, '2026-01-12', 3000.00),
(3, 3, 1, '2026-01-15', 4500.00),
(4, 6, 1, '2026-01-20', 5500.00),
(5, 4, 1, '2026-02-02', 12000.00),
(6, 9, 1, '2026-02-10', 15000.00),
(7, 5, 1, '2026-02-15', 25000.00),
(8, 8, 2, '2026-03-01', 5000.00),
(9, 1, 1, '2026-03-05', 85000.00),
(10, 7, 2, '2026-03-12', 2400.00),
(1, 9, 1, '2026-04-02', 15000.00),
(2, 6, 2, '2026-04-10', 11000.00),
(3, 10, 3, '2026-05-01', 2400.00),
(4, 2, 1, '2026-05-15', 1500.00),
(5, 3, 2, '2026-06-01', 9000.00);