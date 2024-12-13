CREATE DATABASE IF NOT EXISTS inventory_system;

USE inventory_system;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL,
    supplier VARCHAR(255)
);

INSERT INTO users (username, password, role) VALUES
('admin', 'admin', 'admin'),
('user1', 'password123', 'user');

INSERT INTO products (product_name, description, price, stock_quantity, supplier) VALUES
('Laptop', 'Dell Inspiron 15', 55000.00, 20, 'Dell'),
('Keyboard', 'Wireless Mechanical Keyboard', 3000.00, 50, 'Logitech'),
('Mouse', 'Wireless Mouse', 1500.00, 100, 'Logitech'),
('Monitor', '24-inch LED Monitor', 8000.00, 15, 'Samsung');
