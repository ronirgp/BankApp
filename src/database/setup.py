import sqlite3
import os

def initialize_database():
    """Initialize the bank database with all required tables."""
    
    # Create database directory
    db_dir = "data/db"
    os.makedirs(db_dir, exist_ok=True)
    
    db_path = os.path.join(db_dir, "bank.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table with created_date column
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        balance REAL DEFAULT 0,
        created_date DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        date TEXT NOT NULL,
        transaction_type TEXT NOT NULL,
        amount REAL NOT NULL,
        receiver TEXT
    )
    """)
    
    # Create login_history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        login_time TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
