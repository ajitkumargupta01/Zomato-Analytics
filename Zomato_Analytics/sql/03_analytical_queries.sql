-- ============================================================
--   ZOMATO BUSINESS ANALYTICS — Analytical Queries
--   File: 03_analytical_queries.sql
-- ============================================================
USE zomato_db;

-- ============================================================
--  MODULE 1: RESTAURANT PERFORMANCE ANALYSIS
-- ============================================================

-- Q1: Top 10 restaurants by average rating
SELECT
    r.restaurant_id,
    r.restaurant_name,
    c.city_name,
    r.aggregate_rating,
    r.votes,
    r.avg_cost_for_two,
    r.price_range
FROM restaurants r
JOIN cities c ON r.city_id = c.city_id
ORDER BY r.aggregate_rating DESC, r.votes DESC
LIMIT 10;

-- Q2: Restaurant count and avg rating by city
SELECT
    c.city_name,
    COUNT(r.restaurant_id)        AS total_restaurants,
    ROUND(AVG(r.aggregate_rating),2) AS avg_city_rating,
    ROUND(AVG(r.avg_cost_for_two),0) AS avg_cost_for_two,
    SUM(r.has_online_delivery)    AS online_delivery_count,
    SUM(r.has_table_booking)      AS table_booking_count
FROM restaurants r
JOIN cities c ON r.city_id = c.city_id
GROUP BY c.city_name
ORDER BY total_restaurants DESC;

-- Q3: Price range distribution across cities
SELECT
    c.city_name,
    SUM(CASE WHEN r.price_range = 1 THEN 1 ELSE 0 END) AS budget,
    SUM(CASE WHEN r.price_range = 2 THEN 1 ELSE 0 END) AS mid_range,
    SUM(CASE WHEN r.price_range = 3 THEN 1 ELSE 0 END) AS premium,
    SUM(CASE WHEN r.price_range = 4 THEN 1 ELSE 0 END) AS luxury
FROM restaurants r
JOIN cities c ON r.city_id = c.city_id
GROUP BY c.city_name
ORDER BY c.city_name;

-- Q4: Most popular cuisines
SELECT
    cu.cuisine_name,
    COUNT(rc.restaurant_id) AS restaurant_count,
    ROUND(AVG(r.aggregate_rating),2) AS avg_rating
FROM cuisines cu
JOIN restaurant_cuisines rc ON cu.cuisine_id = rc.cuisine_id
JOIN restaurants r          ON rc.restaurant_id = r.restaurant_id
GROUP BY cu.cuisine_name
ORDER BY restaurant_count DESC;

-- Q5: Restaurants with high votes but low rating (needs improvement)
SELECT
    r.restaurant_name,
    c.city_name,
    r.aggregate_rating,
    r.votes
FROM restaurants r
JOIN cities c ON r.city_id = c.city_id
WHERE r.votes > 1000 AND r.aggregate_rating < 4.0
ORDER BY r.votes DESC;

-- ============================================================
--  MODULE 2: ORDER & REVENUE ANALYSIS
-- ============================================================

-- Q6: Monthly revenue trend
SELECT
    DATE_FORMAT(o.order_date,'%Y-%m') AS month,
    COUNT(o.order_id)                 AS total_orders,
    SUM(o.final_amount)               AS total_revenue,
    ROUND(AVG(o.final_amount),2)      AS avg_order_value,
    SUM(o.discount_amount)            AS total_discounts
FROM orders o
WHERE o.order_status = 'Delivered'
GROUP BY DATE_FORMAT(o.order_date,'%Y-%m')
ORDER BY month;

-- Q7: Revenue by city
SELECT
    c.city_name,
    COUNT(o.order_id)            AS total_orders,
    SUM(o.final_amount)          AS total_revenue,
    ROUND(AVG(o.final_amount),2) AS avg_order_value,
    ROUND(AVG(o.delivery_time),1) AS avg_delivery_time_mins
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
JOIN cities c      ON r.city_id = c.city_id
WHERE o.order_status = 'Delivered'
GROUP BY c.city_name
ORDER BY total_revenue DESC;

-- Q8: Payment method preferences
SELECT
    payment_method,
    COUNT(*)                              AS order_count,
    ROUND(COUNT(*)*100.0/SUM(COUNT(*)) OVER(),1) AS percentage,
    SUM(final_amount)                     AS total_revenue
FROM orders
WHERE order_status != 'Cancelled'
GROUP BY payment_method
ORDER BY order_count DESC;

-- Q9: Cancellation rate by restaurant
SELECT
    r.restaurant_name,
    COUNT(o.order_id)                          AS total_orders,
    SUM(CASE WHEN o.order_status='Cancelled' THEN 1 ELSE 0 END) AS cancelled,
    ROUND(SUM(CASE WHEN o.order_status='Cancelled' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS cancel_rate_pct
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_name
HAVING total_orders > 1
ORDER BY cancel_rate_pct DESC;

-- Q10: Peak ordering hours
SELECT
    HOUR(order_date) AS hour_of_day,
    COUNT(*)          AS total_orders,
    ROUND(AVG(final_amount),2) AS avg_order_value
FROM orders
WHERE order_status = 'Delivered'
GROUP BY HOUR(order_date)
ORDER BY hour_of_day;

-- ============================================================
--  MODULE 3: CUSTOMER BEHAVIOR ANALYSIS
-- ============================================================

-- Q11: Customer segmentation by order count (RFM style)
SELECT
    customer_id,
    total_orders,
    total_spend,
    avg_order_value,
    CASE
        WHEN total_orders >= 10 THEN 'Champion'
        WHEN total_orders >= 5  THEN 'Loyal'
        WHEN total_orders >= 2  THEN 'Regular'
        ELSE                         'New'
    END AS customer_segment
FROM (
    SELECT
        c.customer_id,
        COUNT(o.order_id)             AS total_orders,
        SUM(o.final_amount)           AS total_spend,
        ROUND(AVG(o.final_amount),2)  AS avg_order_value
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
      AND o.order_status = 'Delivered'
    GROUP BY c.customer_id
) seg
ORDER BY total_spend DESC;

-- Q12: Customer retention — repeat vs new
SELECT
    DATE_FORMAT(order_date,'%Y-%m') AS month,
    SUM(is_first_order)             AS new_customers,
    COUNT(*) - SUM(is_first_order)  AS repeat_customers
FROM orders
WHERE order_status = 'Delivered'
GROUP BY DATE_FORMAT(order_date,'%Y-%m')
ORDER BY month;

-- Q13: Top 10 customers by lifetime value
SELECT
    c.full_name,
    c.email,
    ci.city_name,
    COUNT(o.order_id)    AS total_orders,
    SUM(o.final_amount)  AS lifetime_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
  AND o.order_status = 'Delivered'
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
JOIN cities ci     ON r.city_id = ci.city_id
GROUP BY c.customer_id, c.full_name, c.email, ci.city_name
ORDER BY lifetime_value DESC
LIMIT 10;

-- ============================================================
--  MODULE 4: REVIEW SENTIMENT ANALYSIS (SQL Side)
-- ============================================================

-- Q14: Average rating by restaurant
SELECT
    r.restaurant_name,
    COUNT(rv.review_id)           AS review_count,
    ROUND(AVG(rv.rating),2)       AS avg_review_rating,
    r.aggregate_rating            AS platform_rating
FROM restaurants r
LEFT JOIN reviews rv ON r.restaurant_id = rv.restaurant_id
GROUP BY r.restaurant_id, r.restaurant_name, r.aggregate_rating
ORDER BY avg_review_rating DESC;

-- Q15: Rating distribution
SELECT
    rating,
    COUNT(*) AS reviews
FROM reviews
GROUP BY rating
ORDER BY rating DESC;

-- ============================================================
--  MODULE 5: DELIVERY PERFORMANCE
-- ============================================================

-- Q16: Delivery time analysis
SELECT
    c.city_name,
    ROUND(AVG(o.delivery_time),1)  AS avg_delivery_mins,
    MIN(o.delivery_time)           AS min_delivery_mins,
    MAX(o.delivery_time)           AS max_delivery_mins,
    SUM(CASE WHEN o.delivery_time > 45 THEN 1 ELSE 0 END) AS late_deliveries
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
JOIN cities c      ON r.city_id = c.city_id
WHERE o.order_status = 'Delivered'
GROUP BY c.city_name
ORDER BY avg_delivery_mins;

-- ============================================================
--  MODULE 6: ADVANCED WINDOW FUNCTIONS
-- ============================================================

-- Q17: Restaurant rank within each city by rating
SELECT
    c.city_name,
    r.restaurant_name,
    r.aggregate_rating,
    RANK() OVER (PARTITION BY c.city_id ORDER BY r.aggregate_rating DESC) AS city_rank,
    DENSE_RANK() OVER (PARTITION BY c.city_id ORDER BY r.aggregate_rating DESC) AS city_dense_rank
FROM restaurants r
JOIN cities c ON r.city_id = c.city_id;

-- Q18: Running revenue total by month
SELECT
    DATE_FORMAT(order_date,'%Y-%m') AS month,
    SUM(final_amount)               AS monthly_revenue,
    SUM(SUM(final_amount)) OVER (ORDER BY DATE_FORMAT(order_date,'%Y-%m')) AS cumulative_revenue
FROM orders
WHERE order_status = 'Delivered'
GROUP BY DATE_FORMAT(order_date,'%Y-%m')
ORDER BY month;

-- Q19: Month-over-month growth
SELECT
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month))
        / LAG(monthly_revenue) OVER (ORDER BY month) * 100, 2
    ) AS mom_growth_pct
FROM (
    SELECT
        DATE_FORMAT(order_date,'%Y-%m') AS month,
        SUM(final_amount)               AS monthly_revenue
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY DATE_FORMAT(order_date,'%Y-%m')
) monthly;