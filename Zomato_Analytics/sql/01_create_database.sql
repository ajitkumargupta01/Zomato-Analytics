-- ============================================================
--   ZOMATO BUSINESS ANALYTICS — MySQL Database
--   File: 01_create_database.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS zomato_db;
USE zomato_db;

-- 1. CITIES TABLE
CREATE TABLE cities (
    city_id   INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    state     VARCHAR(100),
    country   VARCHAR(50) DEFAULT 'India'
);

-- 2. CUISINES TABLE
CREATE TABLE cuisines (
    cuisine_id   INT AUTO_INCREMENT PRIMARY KEY,
    cuisine_name VARCHAR(100) NOT NULL
);

-- 3. RESTAURANTS TABLE
CREATE TABLE restaurants (
    restaurant_id   INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_name VARCHAR(200) NOT NULL,
    city_id         INT,
    address         VARCHAR(300),
    locality        VARCHAR(150),
    latitude        DECIMAL(9,6),
    longitude       DECIMAL(9,6),
    avg_cost_for_two INT,           -- in INR
    currency        VARCHAR(10) DEFAULT 'INR',
    has_table_booking   TINYINT(1) DEFAULT 0,
    has_online_delivery TINYINT(1) DEFAULT 0,
    is_delivering_now   TINYINT(1) DEFAULT 0,
    price_range     TINYINT CHECK (price_range BETWEEN 1 AND 4),
    aggregate_rating DECIMAL(3,1),
    rating_color    VARCHAR(20),
    rating_text     VARCHAR(20),
    votes           INT DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

-- 4. RESTAURANT_CUISINES (many-to-many)
CREATE TABLE restaurant_cuisines (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT,
    cuisine_id    INT,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
    FOREIGN KEY (cuisine_id)    REFERENCES cuisines(cuisine_id)
);

-- 5. CUSTOMERS TABLE
CREATE TABLE customers (
    customer_id   INT AUTO_INCREMENT PRIMARY KEY,
    full_name     VARCHAR(150) NOT NULL,
    email         VARCHAR(150) UNIQUE,
    phone         VARCHAR(20),
    city_id       INT,
    signup_date   DATE,
    is_active     TINYINT(1) DEFAULT 1,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

-- 6. ORDERS TABLE
CREATE TABLE orders (
    order_id        INT AUTO_INCREMENT PRIMARY KEY,
    customer_id     INT,
    restaurant_id   INT,
    order_date      DATETIME,
    delivery_time   INT,          -- minutes
    order_status    ENUM('Placed','Confirmed','Preparing','Out for Delivery','Delivered','Cancelled') DEFAULT 'Placed',
    payment_method  ENUM('Cash','Card','UPI','Wallet') DEFAULT 'UPI',
    total_amount    DECIMAL(10,2),
    discount_amount DECIMAL(10,2) DEFAULT 0,
    final_amount    DECIMAL(10,2),
    is_first_order  TINYINT(1) DEFAULT 0,
    FOREIGN KEY (customer_id)   REFERENCES customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

-- 7. ORDER_ITEMS TABLE
CREATE TABLE order_items (
    item_id       INT AUTO_INCREMENT PRIMARY KEY,
    order_id      INT,
    item_name     VARCHAR(200),
    category      VARCHAR(100),
    quantity      INT DEFAULT 1,
    unit_price    DECIMAL(8,2),
    total_price   DECIMAL(8,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- 8. REVIEWS TABLE
CREATE TABLE reviews (
    review_id     INT AUTO_INCREMENT PRIMARY KEY,
    customer_id   INT,
    restaurant_id INT,
    order_id      INT,
    rating        DECIMAL(2,1) CHECK (rating BETWEEN 1.0 AND 5.0),
    review_text   TEXT,
    review_date   DATETIME DEFAULT CURRENT_TIMESTAMP,
    helpful_votes INT DEFAULT 0,
    FOREIGN KEY (customer_id)   REFERENCES customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
    FOREIGN KEY (order_id)      REFERENCES orders(order_id)
);

-- 9. DELIVERY_PARTNERS TABLE
CREATE TABLE delivery_partners (
    partner_id   INT AUTO_INCREMENT PRIMARY KEY,
    full_name    VARCHAR(150),
    city_id      INT,
    rating       DECIMAL(3,2),
    total_orders INT DEFAULT 0,
    is_active    TINYINT(1) DEFAULT 1,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

-- ============================================================
--   INDEXES for performance
-- ============================================================
CREATE INDEX idx_restaurants_city   ON restaurants(city_id);
CREATE INDEX idx_restaurants_rating ON restaurants(aggregate_rating);
CREATE INDEX idx_orders_date        ON orders(order_date);
CREATE INDEX idx_orders_customer    ON orders(customer_id);
CREATE INDEX idx_orders_restaurant  ON orders(restaurant_id);
CREATE INDEX idx_reviews_restaurant ON reviews(restaurant_id);

SELECT 'Database and tables created successfully!' AS status;