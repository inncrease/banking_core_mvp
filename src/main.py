import sqlite3
import uuid
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
DB_NAME = "banking.db"

# --- PYDANTIC MODELS (Data Validation) ---

# Model for creating a new user
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str

# Model for transferring money
class TransferRequest(BaseModel):
    sender_id: str      # UUID of the sender
    receiver_id: str    # UUID of the receiver
    amount: float = Field(..., gt=0, description="The amount must be positive")      # Amount to transfer

# --- DATABASE HELPER ---

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    # This allows accessing columns by name (e.g., row['email'])
    conn.row_factory = sqlite3.Row 
    return conn

# --- API ENDPOINTS ---

@app.get("/")
def read_root():
    """Root endpoint to check service status."""
    return {"message": "Banking Core is Running"}

@app.get("/users")
def get_users():
    """Fetch all users from the database to see balances and IDs."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return {"users": users}

@app.post("/users")
def create_user(user: UserCreate):
    """
    Creates a new user.
    Automatically generates UUID, Account Number, and sets initial Balance to 0.00.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Generate internal system ID (UUID)
    user_id = str(uuid.uuid4())
    
    # Generate public 9-digit account number
    account_number = random.randint(100000000, 999999999)
    
    try:
        # Insert new user with 0.00 balance
        cursor.execute(
            """
            INSERT INTO users (id, account_number, first_name, last_name, phone_number, email, balance) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, account_number, user.first_name, user.last_name, user.phone_number, user.email, 0.00)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # Handle duplicate email or phone number
        conn.close()
        raise HTTPException(status_code=400, detail="User with this email or phone number already exists")
    
    conn.close()
    return {
        "message": "User created successfully", 
        "user_id": user_id, 
        "account_number": account_number
    }

# --- MONEY TRANSFER ENDPOINT (ACID Transaction) ---

@app.post("/transfer")
def make_transfer(transfer: TransferRequest):
    """
    Transfers money from one user to another safely.
    Uses database transactions to ensure Atomicity (all or nothing).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Check sender's balance and existence
        cursor.execute("SELECT balance FROM users WHERE id = ?", (transfer.sender_id,))
        sender = cursor.fetchone()
        
        if not sender:
            raise HTTPException(status_code=404, detail="Sender not found")
        
        if sender["balance"] < transfer.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        # 2. START TRANSACTION
        # SQLite starts a transaction automatically when we execute UPDATE/INSERT statements.
        
        # Step A: Deduct money from sender
        cursor.execute(
            "UPDATE users SET balance = balance - ? WHERE id = ?", 
            (transfer.amount, transfer.sender_id)
        )
        
        # Step B: Add money to receiver
        cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE id = ?", 
            (transfer.amount, transfer.receiver_id)
        )
        
        # Step C: Record the transaction log
        transaction_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO transactions (id, sender_id, receiver_id, amount) VALUES (?, ?, ?, ?)",
            (transaction_id, transfer.sender_id, transfer.receiver_id, transfer.amount)
        )

        # 3. COMMIT (Save changes)
        # If we reached this point without errors, save everything.
        conn.commit()
        
    except Exception as e:
        # 4. ROLLBACK (Undo changes)
        # If ANY error occurred (even a code error), undo all SQL commands in this block.
        conn.rollback()
        conn.close()
        
        # If it was our specific error (e.g., Insufficient funds), re-raise it
        if isinstance(e, HTTPException):
            raise e
        
        # If it was a database error, return 500
        raise HTTPException(status_code=500, detail=str(e))

    conn.close()
    return {"message": "Transfer successful", "transaction_id": transaction_id}
@app.get("/transactions")
def get_transactions():
    """
    Fetch the complete history of all money transfers.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all transactions ordered by time (newest first)
    cursor.execute("SELECT * FROM transactions ORDER BY created_at DESC")
    transactions = cursor.fetchall()
    
    conn.close()
    return {"transactions": transactions}