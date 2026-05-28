-- ============================================================================
-- SQLite Inventory Management System
-- ============================================================================
-- This script creates a complete inventory management database with
-- products, sales tracking, and automated inventory alerts.
-- ============================================================================


-- ============================================================================
-- 1. CREATE TABLES
-- ============================================================================

-- Products table: Main inventory storage
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    price REAL NOT NULL CHECK (price > 0),
    stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0),
    reorder_level INTEGER NOT NULL CHECK (reorder_level >= 1),
    supplier TEXT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sales table: Track all product sales
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL CHECK (quantity_sold > 0),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Create index on sales for faster queries
CREATE INDEX IF NOT EXISTS idx_sales_product_id ON sales(product_id);
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date);


-- ============================================================================
-- 2. INSERT SAMPLE DATA
-- ============================================================================

-- Clear existing data (if any) for fresh start
DELETE FROM sales;
DELETE FROM products;

-- Insert products across 3 categories
INSERT INTO products (name, category, price, stock_quantity, reorder_level, supplier, last_updated)
VALUES 
    ('Laptop Dell XPS 13', 'Electronics', 1299.99, 15, 5, 'Tech Suppliers Inc', CURRENT_TIMESTAMP),
    ('Wireless Mouse', 'Electronics', 29.99, 120, 20, 'Tech Suppliers Inc', CURRENT_TIMESTAMP),
    ('USB-C Cable', 'Electronics', 12.99, 250, 50, 'Tech Suppliers Inc', CURRENT_TIMESTAMP),
    ('Office Chair Pro', 'Furniture', 249.99, 8, 3, 'Furniture World', CURRENT_TIMESTAMP),
    ('Standing Desk', 'Furniture', 499.99, 5, 2, 'Furniture World', CURRENT_TIMESTAMP),
    ('Desk Lamp LED', 'Furniture', 39.99, 35, 10, 'Furniture World', CURRENT_TIMESTAMP),
    ('Notebook A4 (Pack)', 'Stationery', 5.99, 500, 100, 'Office Direct', CURRENT_TIMESTAMP),
    ('Ballpoint Pen (Box)', 'Stationery', 8.99, 300, 50, 'Office Direct', CURRENT_TIMESTAMP);

-- Insert sample sales transactions
INSERT INTO sales (product_id, quantity_sold, sale_date)
VALUES
    (1, 2, datetime('now', '-5 days')),      -- 2 Laptops sold 5 days ago
    (2, 15, datetime('now', '-4 days')),     -- 15 mice sold 4 days ago
    (4, 1, datetime('now', '-3 days')),      -- 1 chair sold 3 days ago
    (3, 50, datetime('now', '-2 days')),     -- 50 cables sold 2 days ago
    (5, 1, datetime('now', '-1 days')),      -- 1 desk sold yesterday
    (2, 20, datetime('now')),                -- 20 mice sold today
    (6, 8, datetime('now'));                 -- 8 lamps sold today


-- ============================================================================
-- 3. QUERY 1: LOW STOCK ALERT
-- ============================================================================
-- Find products where current stock is at or below reorder level
-- This helps identify which products need to be reordered soon

SELECT 
    id,
    name,
    category,
    stock_quantity,
    reorder_level,
    (reorder_level - stock_quantity) AS shortage,
    supplier
FROM products
WHERE stock_quantity <= reorder_level
ORDER BY shortage DESC;


-- ============================================================================
-- 4. QUERY 2: INVENTORY VALUE BY CATEGORY
-- ============================================================================
-- Calculate total inventory value (stock * price) grouped by category
-- Useful for understanding asset distribution

SELECT 
    category,
    COUNT(id) AS product_count,
    SUM(stock_quantity) AS total_units,
    ROUND(SUM(price * stock_quantity), 2) AS total_value,
    ROUND(AVG(price), 2) AS avg_price
FROM products
GROUP BY category
ORDER BY total_value DESC;


-- ============================================================================
-- 5. QUERY 3: TOP 3 SELLING PRODUCTS
-- ============================================================================
-- Identify best-selling products based on total quantity sold
-- Useful for understanding sales trends and stock management

SELECT 
    p.id,
    p.name,
    p.category,
    SUM(s.quantity_sold) AS total_sold,
    COUNT(s.id) AS number_of_sales,
    p.stock_quantity AS current_stock,
    ROUND(p.price * SUM(s.quantity_sold), 2) AS total_revenue
FROM products p
LEFT JOIN sales s ON p.id = s.product_id
GROUP BY p.id, p.name, p.category, p.stock_quantity, p.price
ORDER BY total_sold DESC
LIMIT 3;


-- ============================================================================
-- 6. CREATE VIEW: LOW_STOCK_ALERT
-- ============================================================================
-- Create a reusable view for low stock alerts
-- This simplifies recurring queries and provides clean data interface

CREATE VIEW IF NOT EXISTS low_stock_alert AS
SELECT 
    p.id,
    p.name,
    p.category,
    p.stock_quantity,
    p.reorder_level,
    (p.reorder_level - p.stock_quantity) AS units_needed,
    p.supplier,
    (p.price * (p.reorder_level - p.stock_quantity)) AS reorder_cost,
    p.last_updated
FROM products p
WHERE p.stock_quantity <= p.reorder_level
ORDER BY (p.reorder_level - p.stock_quantity) DESC;


-- ============================================================================
-- 7. EXAMPLE QUERIES USING THE VIEW
-- ============================================================================
-- Query the low_stock_alert view
SELECT * FROM low_stock_alert;

-- Get total reorder cost for all low-stock items
SELECT 
    ROUND(SUM(reorder_cost), 2) AS total_reorder_cost,
    COUNT(*) AS items_needing_reorder
FROM low_stock_alert;


-- ============================================================================
-- 8. CREATE TRIGGER: AUTOMATIC LOW STOCK ALERT
-- ============================================================================
-- This trigger will log a message when stock drops below reorder level
-- In a real system, this could trigger email notifications or alerts

CREATE TABLE IF NOT EXISTS stock_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    alert_type TEXT NOT NULL,
    stock_quantity INTEGER NOT NULL,
    reorder_level INTEGER NOT NULL,
    alert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Trigger that fires when sales are recorded and stock drops below reorder level
CREATE TRIGGER IF NOT EXISTS trigger_low_stock_alert
AFTER UPDATE OF stock_quantity ON products
BEGIN
    INSERT INTO stock_alerts (product_id, product_name, alert_type, stock_quantity, reorder_level)
    SELECT 
        NEW.id,
        NEW.name,
        'LOW_STOCK',
        NEW.stock_quantity,
        NEW.reorder_level
    WHERE NEW.stock_quantity <= NEW.reorder_level;
END;


-- ============================================================================
-- 9. ADDITIONAL USEFUL QUERIES
-- ============================================================================

-- Sales summary by product
SELECT 
    p.id,
    p.name,
    p.category,
    COUNT(s.id) AS transaction_count,
    SUM(s.quantity_sold) AS total_quantity_sold,
    ROUND(AVG(s.quantity_sold), 2) AS avg_quantity_per_sale
FROM products p
LEFT JOIN sales s ON p.id = s.product_id
GROUP BY p.id, p.name, p.category
ORDER BY total_quantity_sold DESC NULLS LAST;


-- Products with no sales
SELECT 
    id,
    name,
    category,
    stock_quantity,
    price,
    ROUND(price * stock_quantity, 2) AS stock_value
FROM products
WHERE id NOT IN (SELECT DISTINCT product_id FROM sales)
ORDER BY stock_value DESC;


-- ============================================================================
-- 10. DATABASE STATISTICS AND SUMMARY
-- ============================================================================

-- Overall inventory summary
SELECT 
    COUNT(*) AS total_products,
    SUM(stock_quantity) AS total_units_in_stock,
    ROUND(SUM(price * stock_quantity), 2) AS total_inventory_value,
    ROUND(AVG(price), 2) AS average_product_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price,
    SUM(CASE WHEN stock_quantity <= reorder_level THEN 1 ELSE 0 END) AS low_stock_count
FROM products;


-- ============================================================================
-- 11. SAMPLE SIMULATION: Process a sale
-- ============================================================================
-- Uncomment and run these statements to simulate a real sale process

-- Step 1: Simulate a customer buying 5 USB-C Cables (product_id = 3)
-- INSERT INTO sales (product_id, quantity_sold) VALUES (3, 5);

-- Step 2: Update stock quantity for the product
-- UPDATE products SET stock_quantity = stock_quantity - 5, last_updated = CURRENT_TIMESTAMP WHERE id = 3;

-- Step 3: Check current inventory
-- SELECT * FROM products WHERE id = 3;

-- Step 4: Check low stock alerts if any were triggered
-- SELECT * FROM stock_alerts ORDER BY alert_date DESC LIMIT 1;

-- ============================================================================
-- END OF INVENTORY MANAGEMENT SYSTEM
-- ============================================================================
