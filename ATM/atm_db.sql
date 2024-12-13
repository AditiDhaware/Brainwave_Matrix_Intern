
CREATE DATABASE IF NOT EXISTS atm_db;

USE atm_db;

CREATE TABLE IF NOT EXISTS accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    pin VARCHAR(10) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00
);


CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_type ENUM('Deposit', 'Withdraw') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);


INSERT INTO accounts (username, pin, balance)
VALUES ('Aditi', '1234', 5000),
       ('Rahul', '5678', 3000),
       ('Priya', '4321', 8000);

INSERT INTO transactions (account_id, transaction_type, amount)
VALUES (1, 'Deposit', 500),
       (1, 'Withdraw', 1000),
       (1, 'Deposit', 2000);
