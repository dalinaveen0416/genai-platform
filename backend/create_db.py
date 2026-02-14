import sqlite3
import os
import time

def create_sample_database():
    """Create or recreate the sample database"""
    os.makedirs("data", exist_ok=True)
    db_path = "data/sample.db"
    
    # Remove corrupted database if it exists
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            conn.close()
            if tables:  # Database is valid, don't recreate
                return db_path
        except:
            # Database is corrupted, try to remove it
            try:
                conn.close()
            except:
                pass
            
            # Try to remove the file
            for attempt in range(3):
                try:
                    os.remove(db_path)
                    break
                except PermissionError:
                    if attempt < 2:
                        time.sleep(0.5)
                    else:
                        # If we can't delete it, just skip and let it be overwritten
                        pass
    
    # Create fresh database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TEXT
    )
    """)
    
    # Create emails table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        subject TEXT,
        body TEXT,
        sent_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    # Check if tables have data
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count == 0:
        # Insert sample data
        cursor.executemany(
            "INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)",
            [
                ("John Doe", "john@example.com", "2024-01-01"),
                ("Jane Smith", "jane@example.com", "2024-01-02")
            ]
        )
        
        cursor.executemany(
            "INSERT INTO emails (user_id, subject, body, sent_at) VALUES (?, ?, ?, ?)",
            [
                (1, "Hello", "This is a test email", "2024-01-10"),
                (2, "Welcome", "Welcome to our platform", "2024-01-15")
            ]
        )
    
    conn.commit()
    conn.close()
    return db_path

if __name__ == "__main__":
    create_sample_database()
