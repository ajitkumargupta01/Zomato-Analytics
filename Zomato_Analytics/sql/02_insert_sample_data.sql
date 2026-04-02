-- ============================================================
--   ZOMATO BUSINESS ANALYTICS — Sample Data
--   File: 02_insert_sample_data.sql
-- ============================================================
USE zomato_db;

-- CITIES
INSERT INTO cities (city_name, state) VALUES
('Mumbai', 'Maharashtra'), ('Delhi', 'Delhi'), ('Bangalore', 'Karnataka'),
('Hyderabad', 'Telangana'), ('Chennai', 'Tamil Nadu'), ('Kolkata', 'West Bengal'),
('Pune', 'Maharashtra'), ('Ahmedabad', 'Gujarat'), ('Jaipur', 'Rajasthan'),
('Lucknow', 'Uttar Pradesh');

-- CUISINES
INSERT INTO cuisines (cuisine_name) VALUES
('North Indian'), ('South Indian'), ('Chinese'), ('Italian'), ('Continental'),
('Fast Food'), ('Biryani'), ('Pizza'), ('Mughlai'), ('Street Food'),
('Bengali'), ('Rajasthani'), ('Seafood'), ('Desserts'), ('Cafe');

-- RESTAURANTS
INSERT INTO restaurants
  (restaurant_name, city_id, locality, avg_cost_for_two, has_table_booking,
   has_online_delivery, price_range, aggregate_rating, rating_text, votes)
VALUES
('Spice Garden',          1,'Bandra',          800, 1,1,2, 4.2,'Very Good', 3200),
('Biryani House',         2,'Connaught Place', 600, 0,1,2, 4.5,'Excellent',  5600),
('The Pasta Place',       3,'Koramangala',    1200, 1,1,3, 4.0,'Good',       1800),
('Royal Mughlai',         4,'Jubilee Hills',   900, 1,1,3, 4.3,'Very Good',  2900),
('Dosa Corner',           5,'T. Nagar',        350, 0,1,1, 4.1,'Good',       4100),
('Kolkata Kitchen',       6,'Park Street',     700, 1,1,2, 3.8,'Good',       1500),
('Pune Treats',           7,'Koregaon Park',   650, 0,1,2, 4.0,'Good',       2200),
('Gujarat Dhaba',         8,'CG Road',         450, 0,1,1, 3.9,'Good',       1800),
('Rajasthani Thali',      9,'MI Road',         500, 1,0,1, 4.4,'Excellent',  3300),
('Awadhi Delights',      10,'Hazratganj',      550, 1,1,2, 4.2,'Very Good',  2700),
('Burger Bytes',          1,'Andheri',         400, 0,1,1, 3.7,'Good',       890),
('Pizza Republic',        2,'Lajpat Nagar',    700, 0,1,2, 4.0,'Good',       1200),
('The Sushi Bar',         3,'Indiranagar',    1800, 1,0,4, 4.6,'Excellent',  2100),
('Seafood Paradise',      4,'Banjara Hills', 1500, 1,1,3, 4.3,'Very Good',  1600),
('Filter Coffee Club',    5,'Adyar',           300, 0,1,1, 4.5,'Excellent',  5500);

-- RESTAURANT-CUISINE MAPPING
INSERT INTO restaurant_cuisines (restaurant_id, cuisine_id) VALUES
(1,1),(1,10),(2,7),(2,9),(3,4),(3,5),(4,9),(4,1),(5,2),(5,10),
(6,11),(6,1),(7,3),(7,6),(8,12),(8,1),(9,12),(9,1),(10,1),(10,9),
(11,6),(12,8),(13,3),(14,13),(15,2),(15,15);

-- CUSTOMERS (30 sample customers)
INSERT INTO customers (full_name, email, phone, city_id, signup_date) VALUES
('Rahul Sharma',    'rahul.s@email.com',  '9876543210', 1, '2022-01-15'),
('Priya Patel',     'priya.p@email.com',  '9876543211', 2, '2022-02-20'),
('Amit Kumar',      'amit.k@email.com',   '9876543212', 3, '2022-03-10'),
('Sneha Reddy',     'sneha.r@email.com',  '9876543213', 4, '2022-04-05'),
('Karan Singh',     'karan.s@email.com',  '9876543214', 5, '2022-05-12'),
('Meera Nair',      'meera.n@email.com',  '9876543215', 6, '2022-06-18'),
('Vikram Joshi',    'vikram.j@email.com', '9876543216', 7, '2022-07-22'),
('Ananya Gupta',    'ananya.g@email.com', '9876543217', 8, '2022-08-30'),
('Rohit Verma',     'rohit.v@email.com',  '9876543218', 9, '2022-09-14'),
('Divya Agarwal',   'divya.a@email.com',  '9876543219',10, '2022-10-08'),
('Saurabh Mishra',  'saurabh.m@email.com','9876543220', 1, '2022-11-01'),
('Tanvi Shah',      'tanvi.s@email.com',  '9876543221', 2, '2022-12-15'),
('Nikhil Rao',      'nikhil.r@email.com', '9876543222', 3, '2023-01-10'),
('Pooja Chopra',    'pooja.c@email.com',  '9876543223', 4, '2023-02-25'),
('Arjun Das',       'arjun.d@email.com',  '9876543224', 5, '2023-03-18');

-- ORDERS (sample orders)
INSERT INTO orders
  (customer_id, restaurant_id, order_date, delivery_time, order_status,
   payment_method, total_amount, discount_amount, final_amount, is_first_order)
VALUES
(1, 1,  '2024-01-05 12:30:00', 35, 'Delivered', 'UPI',   850.00, 50.00,  800.00, 0),
(2, 2,  '2024-01-06 13:00:00', 42, 'Delivered', 'Card',  620.00,  0.00,  620.00, 0),
(3, 3,  '2024-01-07 19:15:00', 28, 'Delivered', 'UPI',  1300.00,100.00, 1200.00, 0),
(4, 4,  '2024-01-08 20:00:00', 55, 'Delivered', 'Cash',  950.00,  0.00,  950.00, 0),
(5, 5,  '2024-01-09 11:45:00', 22, 'Delivered', 'UPI',   380.00, 30.00,  350.00, 0),
(6, 6,  '2024-01-10 18:30:00', 38, 'Delivered', 'Wallet',740.00,  0.00,  740.00, 0),
(7, 7,  '2024-01-11 20:30:00', 31, 'Delivered', 'UPI',   690.00, 50.00,  640.00, 0),
(8, 8,  '2024-01-12 14:00:00', 25, 'Delivered', 'Card',  480.00,  0.00,  480.00, 0),
(9, 9,  '2024-01-13 12:15:00', 44, 'Delivered', 'Cash',  530.00,  0.00,  530.00, 0),
(10,10, '2024-01-14 21:00:00', 33, 'Delivered', 'UPI',   580.00, 40.00,  540.00, 0),
(1, 2,  '2024-01-15 13:30:00', 48, 'Delivered', 'Card',  650.00,  0.00,  650.00, 0),
(2, 11, '2024-01-16 19:45:00', 20, 'Delivered', 'UPI',   410.00, 20.00,  390.00, 0),
(3, 12, '2024-01-17 20:15:00', 35, 'Delivered', 'UPI',   720.00,  0.00,  720.00, 0),
(4, 13, '2024-01-18 21:30:00', 50, 'Cancelled', 'Card', 1900.00,  0.00, 1900.00, 0),
(5, 14, '2024-01-19 12:00:00', 40, 'Delivered', 'UPI',  1550.00,100.00, 1450.00, 0),
(11,1,  '2024-02-01 13:00:00', 30, 'Delivered', 'UPI',   860.00, 86.00,  774.00, 1),
(12,3,  '2024-02-02 20:00:00', 27, 'Delivered', 'Card', 1250.00, 125.00,1125.00, 1),
(13,5,  '2024-02-03 12:30:00', 18, 'Delivered', 'UPI',   395.00, 50.00,  345.00, 1),
(14,7,  '2024-02-04 21:00:00', 35, 'Delivered', 'Wallet',700.00,  0.00,  700.00, 1),
(15,9,  '2024-02-05 11:30:00', 28, 'Delivered', 'UPI',   510.00, 51.00,  459.00, 1);

-- ORDER ITEMS
INSERT INTO order_items (order_id, item_name, category, quantity, unit_price, total_price)
VALUES
(1,'Butter Chicken',    'Main Course', 1, 380.00, 380.00),
(1,'Garlic Naan',       'Bread',       2,  60.00, 120.00),
(1,'Raita',             'Side',        1,  80.00,  80.00),
(2,'Chicken Biryani',   'Main Course', 2, 280.00, 560.00),
(2,'Raita',             'Side',        1,  60.00,  60.00),
(3,'Pasta Arrabbiata',  'Main Course', 1, 450.00, 450.00),
(3,'Garlic Bread',      'Starter',     1, 180.00, 180.00),
(3,'Tiramisu',          'Dessert',     1, 250.00, 250.00),
(5,'Masala Dosa',       'Main Course', 2, 120.00, 240.00),
(5,'Filter Coffee',     'Beverage',    2,  70.00, 140.00);

-- REVIEWS
INSERT INTO reviews (customer_id, restaurant_id, order_id, rating, review_text, review_date)
VALUES
(1,1,1, 4.5,'Amazing food! Butter chicken was perfect. Fast delivery too.',  '2024-01-05 14:00:00'),
(2,2,2, 4.0,'Biryani was flavorful but slightly oily. Good portion size.',   '2024-01-06 15:30:00'),
(3,3,3, 4.2,'Pasta was authentic Italian taste. Tiramisu was outstanding!',  '2024-01-07 21:00:00'),
(5,5,5, 5.0,'Best dosa in Chennai. Always consistent quality. Love it!',     '2024-01-09 13:00:00'),
(7,7,7, 3.8,'Food was decent but delivery took longer than expected.',        '2024-01-11 22:30:00'),
(10,10,10,4.3,'Awadhi cuisine done right. Nihari was exceptional.',           '2024-01-14 23:00:00');

SELECT 'Sample data inserted successfully!' AS status;
SELECT COUNT(*) AS total_restaurants FROM restaurants;
SELECT COUNT(*) AS total_customers   FROM customers;
SELECT COUNT(*) AS total_orders      FROM orders;