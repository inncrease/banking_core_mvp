# 🏦 Banking Core MVP

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-ACID-003B57?style=for-the-badge&logo=sqlite)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)
![Tests](https://img.shields.io/badge/Tests-Pytest-brightgreen?style=for-the-badge&logo=pytest)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Role:** System Analyst / Data Engineer / Python Developer
**Tech Stack:** Python, FastAPI, SQLite, Pydantic, Streamlit, Pandas, Plotly, Pytest.

## 📋 Project Overview
This project is a prototype of a **transactional banking core**. It demonstrates the end-to-end flow of financial data: from API design and validation to ACID-compliant database transactions and real-time analytics.

### Key Features
* **REST API (FastAPI):** User management and money transfers.
* **Data Integrity (ACID):** Atomic transactions with rollback mechanisms to prevent data loss.
* **Strict Validation (Pydantic):** Prevents logical errors (e.g., negative balance transfers).
* **Quality Assurance:** Covered by integration tests (`pytest`) to ensure reliability.
* **Analytics Dashboard (Streamlit):** Real-time monitoring of liquidity and user wealth.

---

## 🏗 System Architecture

### 1. Business Process: Money Transfer (BPMN)
Visualizes the logic flow including validation gates and error handling.
![BPMN Diagram](docs/images/bpmn_transfer.png)
*(Note: Full BPMN model available in `docs/models/`)*

### 2. Database Schema (UML Class Diagram)
Relational model designed for SQLite (easily scalable to PostgreSQL).
![UML Class Diagram](docs/images/uml_class.png)

### 3. API Sequence Diagram
Technical interaction between Client, API, and Database layers.
![Sequence Diagram](docs/images/uml_sequence.png)

---

## 📝 Use Case: P2P Money Transfer

| Field | Description |
| :--- | :--- |
| **Actor** | Authenticated User (Client) |
| **Pre-conditions** | 1. User is logged in.<br>2. Sender has positive balance.<br>3. Receiver account exists. |
| **Post-conditions** | 1. Sender balance decreased.<br>2. Receiver balance increased.<br>3. Transaction logged with Timestamp. |
| **Main Flow** | 1. User sends `POST /transfer` with `{receiver_id, amount}`.<br>2. System validates `amount > 0`.<br>3. System checks liquidity (`balance >= amount`).<br>4. System performs atomic update (ACID).<br>5. System returns `200 OK`. |
| **Alternative Flows** | **A1. Negative Amount:** System returns `422 Validation Error`.<br>**A2. Insufficient Funds:** System returns `400 Bad Request`. |

---

## 📂 Project Structure

```text
USER_SERVICE_PROJECT/
├── database/            # SQL Schema (DDL)
├── docs/                # Documentation & Images
│   └── images/          # Diagrams (BPMN, UML)
├── src/                 # Source Code
│   ├── main.py          # FastAPI Backend
│   ├── dashboard.py     # Streamlit Analytics
│   └── generated_data.py # ETL / Fake Data Generator
├── tests/               # Unit & Integration Tests
│   └── test_main.py
├── banking.db           # SQLite Database (Ignored by Git)
├── requirements.txt     # Python Dependencies
└── README.md            # Project Documentation

---

How to Run

1. Clone & Install

    git clone [https://github.com/YOUR_USERNAME/banking-core-mvp.git](https://github.com/YOUR_USERNAME/banking-core-mvp.git)

    cd banking-core-mvp

    pip install -r requirements.txt

2. Setup Database (ETL)

    Generate initial fake users and transactions:

    python src/generated_data.py

3. Run Tests (Quality Check) 

    Ensure everything works correctly:

    python -m pytest

4. Run API Server (Backend)

    Start the FastAPI server:

    python -m uvicorn src.main:app --reload

    Swagger UI: Open http://127.0.0.1:8000/docs to test API manually.

5. Run Analytics (Frontend)

    Launch the BI dashboard:

    python -m streamlit run src/dashboard.py