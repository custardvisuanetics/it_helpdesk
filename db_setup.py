import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("helpdesk.db")
c = conn.cursor()

# Tickets table
c.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        priority TEXT,
        status TEXT DEFAULT 'Open',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Users table
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'technician',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    )
''')

# Create default admin user
hashed_password = generate_password_hash("admin123")
try:
    conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", hashed_password, "admin"))
except sqlite3.IntegrityError:
    pass  # user already exists

conn.commit()
conn.close()
print("✅ Database and default user ready.")
