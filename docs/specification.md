System Requirements Specification (SRS)
Project: Banking Core MVP Version: 1.0 Status: MVP / Prototype

1. Introduction
1.1 Purpose
The purpose of the Banking Core MVP is to demonstrate a reliable, transactional backend system capable of handling user management and financial transfers with strict ACID compliance and data validation.

1.2 Scope
The system includes:

User Management: Creating clients with bank accounts.

Transaction Processing: Internal money transfers between users.

Analytics Module: A dashboard for liquidity monitoring and transaction history.

API Interface: RESTful API for external system integration.

2. Functional Requirements (FR)
FR-01: User Management
FR-01.1: The system must allow creating a new user via POST /users.

FR-01.2: The system must automatically generate a unique user_id (UUID) and 9-digit account_number.

FR-01.3: The system must prevent duplicate emails or phone numbers (Unique Constraint).

FR-01.4: New users must be initialized with a Welcome Bonus (default: 1000.00 currency units).

FR-02: Financial Transactions
FR-02.1: The system must allow transferring money between two existing users via POST /transfer.

FR-02.2: Validation Rule: The transfer amount must be strictly positive (amount > 0).

FR-02.3: Business Rule: The sender must have a sufficient balance (balance >= amount).

FR-02.4: Integrity: The transfer operation must be Atomic (ACID). If the credit or debit operation fails, the entire transaction must roll back.

FR-03: Analytics & Reporting
FR-03.1: The system must provide a dashboard displaying Total Liquidity, Transaction Volume, and Rich List.

FR-03.2: The analytics data must be real-time or near real-time.

3. Non-Functional Requirements (NFR)
NFR-01 (Data Integrity): The database must ensure referential integrity between Users and Transactions via Foreign Keys.

NFR-02 (Performance): API response time should be under 200ms for standard operations.

NFR-03 (Tech Stack): The system shall be built using Python (FastAPI) and SQLite.