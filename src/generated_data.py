import sqlite3
import uuid
import random
from faker import Faker

# Configuration
DB_NAME = "banking.db"
SCHEMA_FILE = "database/schema.sql"  # Path to your SQL schema file
NUM_USERS = 10

fake = Faker()

def create_connection():
    """Create a database connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def init_db(conn):
    """Initialize the database using the schema.sql file."""
    try:
        with open(SCHEMA_FILE, 'r') as f:
            schema_script = f.read()
        conn.executescript(schema_script)
        print("Database initialized (tables created).")
    except FileNotFoundError:
        print(f"Error: File '{SCHEMA_FILE}' not found. Please check the path.")
    except Exception as e:
        print(f"Error initializing database: {e}")

def generate_fake_data(conn):
    """Populate the users table with fake data including account numbers."""
    cursor = conn.cursor()
    print("Generating fake data...")

    users = []
    # Set to ensure account numbers are unique within this batch
    existing_accounts = set()

    for _ in range(NUM_USERS):
        # 1. Generate UUID (Internal ID)
        user_id = str(uuid.uuid4())
        
        # 2. Generate Unique 9-digit Account Number (Public ID)
        while True:
            # Random int between 100,000,000 and 999,999,999
            acc_num = random.randint(100000000, 999999999)
            if acc_num not in existing_accounts:
                existing_accounts.add(acc_num)
                break
        
        # 3. Generate other fields
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone = fake.phone_number()[:20] # Truncate to fit VARCHAR(20)
        email = fake.email()

        # Note: 'balance', 'role', and 'created_at' have DEFAULT values
        balance = round(random.uniform(1000.00, 10000.00), 2)

        users.append((user_id, acc_num, first_name, last_name, phone, email, balance))


    try:
        # Inserting data including the new account_number
        cursor.executemany(
            "INSERT INTO users (id, account_number, first_name, last_name, phone_number, email, balance) VALUES (?, ?, ?, ?, ?, ?, ?)", 
            users
        )
        conn.commit()
        print(f"Successfully added {NUM_USERS} users with account numbers.")
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")

def main():
    conn = create_connection()
    if conn:
        init_db(conn)            # Create/Reset tables
        generate_fake_data(conn) # Insert data
        conn.close()
        print("Done. Connection closed.")

if __name__ == "__main__":
    main()