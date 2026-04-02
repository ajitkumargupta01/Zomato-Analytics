-- ============================================================
--   ZOMATO BUSINESS ANALYTICS — Stored Procedures & Views
--   File: 04_stored_procedures.sql
-- ============================================================
USE zomato_db;

DELIMITER $$

-- -------------------------------------------------------
-- SP 1: Get restaurant performance summary
-- -------------------------------------------------------
CREATE PROCEDURE GetRestaurantSummary(IN p_city_name VARCHAR(100))
BEGIN
    SELECT
        r.restaurant_name,
        r.aggregate_rating,
        r.votes,
        r.avg_cost_for_two,
        COUNT(o.order_id)            AS total_orders,
        SUM(o.final_amount)          AS total_revenue,
        ROUND(AVG(o.delivery_time),1) AS avg_delivery_mins
    FROM restaurants r
    JOIN cities c      ON r.city_id = c.city_id
    LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id
      AND o.order_status = 'Delivered'
    WHERE c.city_name = p_city_name
    GROUP BY r.restaurant_id, r.restaurant_name, r.aggregate_rating,
             r.votes, r.avg_cost_for_two
    ORDER BY r.aggregate_rating DESC;
END$$

-- -------------------------------------------------------
-- SP 2: Get customer order history
-- -------------------------------------------------------
CREATE PROCEDURE GetCustomerHistory(IN p_customer_id INT)
BEGIN
    SELECT
        o.order_id,
        o.order_date,
        r.restaurant_name,
        c.city_name,
        o.final_amount,
        o.order_status,
        o.payment_method,
        o.delivery_time
    FROM orders o
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id
    JOIN cities c      ON r.city_id = c.city_id
    WHERE o.customer_id = p_customer_id
    ORDER BY o.order_date DESC;
END$$

-- -------------------------------------------------------
-- SP 3: Monthly business report
-- -------------------------------------------------------
CREATE PROCEDURE MonthlyReport(IN p_year INT, IN p_month INT)
BEGIN
    DECLARE start_date DATE;
    DECLARE end_date   DATE;
    SET start_date = MAKEDATE(p_year, 1) + INTERVAL (p_month-1) MONTH;
    SET end_date   = start_date + INTERVAL 1 MONTH - INTERVAL 1 DAY;

    SELECT 'Summary' AS report_section,
        COUNT(*)                     AS total_orders,
        SUM(final_amount)            AS total_revenue,
        AVG(final_amount)            AS avg_order_value,
        SUM(discount_amount)         AS total_discounts,
        SUM(is_first_order)          AS new_customers,
        SUM(CASE WHEN order_status='Cancelled' THEN 1 ELSE 0 END) AS cancellations
    FROM orders
    WHERE DATE(order_date) BETWEEN start_date AND end_date;
END$$

DELIMITER ;

-- ============================================================
--   VIEWS for Power BI / Excel connections
-- ============================================================

-- View 1: Restaurant Full Profile (for Power BI)
CREATE OR REPLACE VIEW vw_restaurant_profile AS
SELECT
    r.restaurant_id,
    r.restaurant_name,
    c.city_name,
    c.state,
    r.locality,
    r.avg_cost_for_two,
    r.price_range,
    CASE r.price_range
        WHEN 1 THEN 'Budget'
        WHEN 2 THEN 'Mid Range'
        WHEN 3 THEN 'Premium'
        WHEN 4 THEN 'Luxury'
    END AS price_label,
    r.aggregate_rating,
    r.rating_text,
    r.votes,
    r.has_online_delivery,
    r.has_table_booking,
    GROUP_CONCAT(cu.cuisine_name ORDER BY cu.cuisine_name SEPARATOR ', ') AS cuisines
FROM restaurants r
JOIN cities c ON r.city_id = c.city_id
LEFT JOIN restaurant_cuisines rc ON r.restaurant_id = rc.restaurant_id
LEFT JOIN cuisines cu            ON rc.cuisine_id = cu.cuisine_id
GROUP BY r.restaurant_id, r.restaurant_name, c.city_name, c.state,
         r.locality, r.avg_cost_for_two, r.price_range, r.aggregate_rating,
         r.rating_text, r.votes, r.has_online_delivery, r.has_table_booking;

-- View 2: Order Details (for Power BI and Excel)
CREATE OR REPLACE VIEW vw_order_details AS
SELECT
    o.order_id,
    o.order_date,
    DAYNAME(o.order_date)              AS day_name,
    HOUR(o.order_date)                 AS order_hour,
    DATE_FORMAT(o.order_date,'%Y-%m')  AS year_month,
    c.full_name    AS customer_name,
    ci.city_name,
    r.restaurant_name,
    o.order_status,
    o.payment_method,
    o.total_amount,
    o.discount_amount,
    o.final_amount,
    o.delivery_time,
    o.is_first_order
FROM orders o
JOIN customers c   ON o.customer_id   = c.customer_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
JOIN cities ci     ON r.city_id       = ci.city_id;

-- View 3: KPI Summary (for dashboards)
CREATE OR REPLACE VIEW vw_kpi_summary AS
SELECT
    COUNT(DISTINCT r.restaurant_id)                           AS total_restaurants,
    COUNT(DISTINCT c.customer_id)                             AS total_customers,
    COUNT(DISTINCT o.order_id)                                AS total_orders,
    SUM(o.final_amount)                                       AS total_revenue,
    ROUND(AVG(o.final_amount),2)                              AS avg_order_value,
    ROUND(AVG(r.aggregate_rating),2)                          AS avg_platform_rating,
    ROUND(SUM(CASE WHEN o.order_status='Cancelled' THEN 1 ELSE 0 END)*100.0/COUNT(o.order_id),1) AS cancellation_rate_pct
FROM restaurants r
CROSS JOIN customers c
LEFT JOIN orders o ON o.order_id IS NOT NULL
WHERE o.order_status IS NOT NULL;

-- Usage examples:
-- CALL GetRestaurantSummary('Mumbai');
-- CALL GetCustomerHistory(1);
-- CALL MonthlyReport(2024, 1);
-- SELECT * FROM vw_restaurant_profile;
-- SELECT * FROM vw_order_details;
SELECT 'Stored procedures and views created!' AS status;