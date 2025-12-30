DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    account_number INTEGER NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    balance DECIMAL(10, 2) DEFAULT 0.00 NOT NULL,
    role VARCHAR(20) DEFAULT 'user' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id TEXT PRIMARY KEY,
    sender_id TEXT NOT NULL,
    receiver_id TEXT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'success' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)

);
-- SEED DATA (Demo Users)
INSERT INTO users (id, account_number, first_name, last_name, phone_number, email, balance, role) VALUES 
('u_1001', 100000001, 'Samantha', 'Jones', '1111111111', 'sam@example.com', 1500.50, 'user'),
('u_1002', 100000002, 'Matthew', 'Smith', '2222222222', 'matt@example.com', 250.00, 'user'),
('u_1003', 100000003, 'Alex', 'Wong', '3333333333', 'alex@example.com', 50000.00, 'admin'),
('u_1004', 100000004, 'Emily', 'Clark', '4444444444', 'emily@example.com', 0.00, 'user'),
('u_1005', 100000005, 'John', 'Doe', '5555555555', 'john@example.com', 120.75, 'user');

-- SEED DATA (Demo Transactions)
INSERT INTO transactions (id, sender_id, receiver_id, amount, status) VALUES
('tx_001', 'u_1001', 'u_1002', 100.00, 'success'),
('tx_002', 'u_1003', 'u_1001', 500.00, 'success'),
('tx_003', 'u_1002', 'u_1004', 50.00, 'success');
