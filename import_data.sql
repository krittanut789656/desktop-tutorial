-- ============================================
-- SQL Import Script for MySQL Database
-- สคริปต์สำหรับ Import ข้อมูลเข้า MySQL
-- ============================================

-- ตั้งค่า Character Set เป็น UTF-8 เพื่อรองรับภาษาไทย
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- สร้างฐานข้อมูล (ถ้ายังไม่มี)
CREATE DATABASE IF NOT EXISTS `tutorial_db`
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- ใช้งานฐานข้อมูลที่สร้างขึ้น
USE `tutorial_db`;

-- ============================================
-- ตารางผู้ใช้งาน (Users)
-- ============================================
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `email` VARCHAR(100) NOT NULL UNIQUE,
  `full_name` VARCHAR(100) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `phone` VARCHAR(20),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_active` BOOLEAN DEFAULT TRUE,
  INDEX idx_email (`email`),
  INDEX idx_username (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert ข้อมูลผู้ใช้งานตัวอย่าง
INSERT INTO `users` (`username`, `email`, `full_name`, `password_hash`, `phone`) VALUES
('admin', 'admin@example.com', 'ผู้ดูแลระบบ', '$2y$10$abcdefghijklmnopqrstuvwxyz1234567890', '0812345678'),
('john_doe', 'john@example.com', 'John Doe', '$2y$10$abcdefghijklmnopqrstuvwxyz1234567891', '0823456789'),
('somchai', 'somchai@example.com', 'สมชาย ใจดี', '$2y$10$abcdefghijklmnopqrstuvwxyz1234567892', '0834567890'),
('mary_jane', 'mary@example.com', 'Mary Jane', '$2y$10$abcdefghijklmnopqrstuvwxyz1234567893', '0845678901'),
('somsri', 'somsri@example.com', 'สมศรี สวยงาม', '$2y$10$abcdefghijklmnopqrstuvwxyz1234567894', '0856789012');

-- ============================================
-- ตารางหมวดหมู่สินค้า (Categories)
-- ============================================
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `category_id` INT AUTO_INCREMENT PRIMARY KEY,
  `category_name` VARCHAR(100) NOT NULL,
  `description` TEXT,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert ข้อมูลหมวดหมู่สินค้า
INSERT INTO `categories` (`category_name`, `description`) VALUES
('อิเล็กทรอนิกส์', 'สินค้าอิเล็กทรอนิกส์และอุปกรณ์เทคโนโลยี'),
('เสื้อผ้า', 'เสื้อผ้าแฟชั่นและเครื่องแต่งกาย'),
('หนังสือ', 'หนังสือและสิ่งพิมพ์'),
('กีฬา', 'อุปกรณ์กีฬาและออกกำลังกาย'),
('ของใช้ในบ้าน', 'เครื่องใช้ไฟฟ้าและของใช้ภายในบ้าน');

-- ============================================
-- ตารางสินค้า (Products)
-- ============================================
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `product_id` INT AUTO_INCREMENT PRIMARY KEY,
  `product_name` VARCHAR(200) NOT NULL,
  `category_id` INT,
  `description` TEXT,
  `price` DECIMAL(10, 2) NOT NULL,
  `stock_quantity` INT DEFAULT 0,
  `sku` VARCHAR(50) UNIQUE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_available` BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (`category_id`) REFERENCES `categories`(`category_id`) ON DELETE SET NULL,
  INDEX idx_category (`category_id`),
  INDEX idx_sku (`sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert ข้อมูลสินค้า
INSERT INTO `products` (`product_name`, `category_id`, `description`, `price`, `stock_quantity`, `sku`) VALUES
('iPhone 15 Pro', 1, 'สมาร์ทโฟน Apple รุ่นล่าสุด', 42900.00, 50, 'ELEC-IP15P-001'),
('MacBook Air M2', 1, 'โน้ตบุ๊ก Apple ชิป M2', 39900.00, 30, 'ELEC-MBA-M2-001'),
('เสื้อยืดคอกลม', 2, 'เสื้อยืดผ้าฝ้าย 100%', 299.00, 200, 'CLTH-TSHIRT-001'),
('กางเกงยีนส์', 2, 'กางเกงยีนส์ขายาว', 890.00, 150, 'CLTH-JEANS-001'),
('หนังสือ Python Programming', 3, 'คู่มือเรียนรู้ Python', 450.00, 100, 'BOOK-PY-001'),
('หนังสือ JavaScript Guide', 3, 'คู่มือ JavaScript สำหรับผู้เริ่มต้น', 420.00, 80, 'BOOK-JS-001'),
('ดัมเบลล์ 5 kg', 4, 'ดัมเบลล์น้ำหนัก 5 กิโลกรัม', 699.00, 60, 'SPORT-DB-5KG-001'),
('เสื่อโยคะ', 4, 'เสื่อโยคะ พร้อมกระเป๋า', 590.00, 75, 'SPORT-YOGA-001'),
('หม้อหุงข้าวไฟฟ้า', 5, 'หม้อหุงข้าวดิจิตอล 1.8 ลิตร', 2490.00, 40, 'HOME-RC-18L-001'),
('เครื่องปั่นน้ำผลไม้', 5, 'เครื่องปั่นพกพา', 890.00, 55, 'HOME-BLND-001');

-- ============================================
-- ตารางคำสั่งซื้อ (Orders)
-- ============================================
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `order_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `order_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `total_amount` DECIMAL(10, 2) NOT NULL,
  `status` ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
  `shipping_address` TEXT,
  `payment_method` VARCHAR(50),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE,
  INDEX idx_user (`user_id`),
  INDEX idx_status (`status`),
  INDEX idx_order_date (`order_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert ข้อมูลคำสั่งซื้อ
INSERT INTO `orders` (`user_id`, `total_amount`, `status`, `shipping_address`, `payment_method`) VALUES
(2, 43790.00, 'delivered', '123 ถนนสุขุมวิท แขวงคลองเตย กรุงเทพฯ 10110', 'credit_card'),
(3, 1489.00, 'shipped', '456 ถนนพระราม 4 แขวงปทุมวัน กรุงเทพฯ 10330', 'bank_transfer'),
(4, 40320.00, 'processing', '789 ถนนเพชรบุรี แขวงราชเทวี กรุงเทพฯ 10400', 'credit_card'),
(5, 3579.00, 'pending', '321 ถนนลาดพร้าว แขวงจตุจักร กรุงเทพฯ 10900', 'cash_on_delivery');

-- ============================================
-- ตารางรายการสินค้าในคำสั่งซื้อ (Order Items)
-- ============================================
DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items` (
  `order_item_id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `quantity` INT NOT NULL,
  `unit_price` DECIMAL(10, 2) NOT NULL,
  `subtotal` DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`order_id`) ON DELETE CASCADE,
  FOREIGN KEY (`product_id`) REFERENCES `products`(`product_id`) ON DELETE RESTRICT,
  INDEX idx_order (`order_id`),
  INDEX idx_product (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert ข้อมูลรายการสินค้าในคำสั่งซื้อ
INSERT INTO `order_items` (`order_id`, `product_id`, `quantity`, `unit_price`, `subtotal`) VALUES
(1, 1, 1, 42900.00, 42900.00),
(1, 3, 3, 299.00, 897.00),
(2, 5, 1, 450.00, 450.00),
(2, 6, 1, 420.00, 420.00),
(2, 7, 1, 699.00, 699.00),
(3, 2, 1, 39900.00, 39900.00),
(3, 3, 1, 299.00, 299.00),
(4, 9, 1, 2490.00, 2490.00),
(4, 10, 1, 890.00, 890.00);

-- ============================================
-- ตารางรีวิวสินค้า (Product Reviews)
-- ============================================
DROP TABLE IF EXISTS `reviews`;
CREATE TABLE `reviews` (
  `review_id` INT AUTO_INCREMENT PRIMARY KEY,
  `product_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `rating` INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
  `comment` TEXT,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`product_id`) REFERENCES `products`(`product_id`) ON DELETE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE,
  INDEX idx_product (`product_id`),
  INDEX idx_user (`user_id`),
  INDEX idx_rating (`rating`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert ข้อมูลรีวิว
INSERT INTO `reviews` (`product_id`, `user_id`, `rating`, `comment`) VALUES
(1, 2, 5, 'สินค้าดีมาก ใช้งานลื่นไหล คุ้มค่าเงินที่จ่ายไป'),
(1, 3, 4, 'ดีครับ แต่ราคาค่อนข้างสูง'),
(2, 4, 5, 'MacBook Air M2 สุดยอดมาก เบา บาง ทำงานไว'),
(5, 3, 5, 'หนังสือดี เนื้อหาเข้าใจง่าย เหมาะสำหรับผู้เริ่มต้น'),
(7, 5, 4, 'ดัมเบลล์คุณภาพดี น้ำหนักตามที่ระบุ'),
(9, 5, 5, 'หม้อหุงข้าวดีมาก ข้าวสุกอร่อย ใช้งานง่าย');

-- ============================================
-- สรุปข้อมูลที่ Import
-- ============================================
-- แสดงจำนวนข้อมูลที่ถูก Insert
SELECT
    'Summary of Imported Data' AS 'สรุปข้อมูลที่นำเข้า',
    '========================' AS '========================';

SELECT 'Users' AS 'ตาราง', COUNT(*) AS 'จำนวนแถว' FROM `users`
UNION ALL
SELECT 'Categories', COUNT(*) FROM `categories`
UNION ALL
SELECT 'Products', COUNT(*) FROM `products`
UNION ALL
SELECT 'Orders', COUNT(*) FROM `orders`
UNION ALL
SELECT 'Order Items', COUNT(*) FROM `order_items`
UNION ALL
SELECT 'Reviews', COUNT(*) FROM `reviews`;

-- ============================================
-- คำแนะนำในการใช้งาน
-- ============================================
/*
การ Import ไฟล์นี้เข้า MySQL:

1. ผ่าน Command Line:
   mysql -u username -p < import_data.sql

2. ผ่าน MySQL Workbench:
   - File > Open SQL Script
   - เลือกไฟล์ import_data.sql
   - กด Execute (⚡)

3. ผ่าน phpMyAdmin:
   - เลือกฐานข้อมูล
   - ไปที่แท็บ Import
   - เลือกไฟล์และกด Go

หมายเหตุ:
- สคริปต์นี้จะสร้างฐานข้อมูล tutorial_db
- รองรับภาษาไทย (UTF-8)
- มีข้อมูลตัวอย่างครบทุกตาราง
- มี Foreign Keys เชื่อมโยงตารางต่างๆ
*/
