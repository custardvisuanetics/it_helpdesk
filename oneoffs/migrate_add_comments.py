import sqlite3

conn = sqlite3.connect("helpdesk.db")
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    author TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id)
)
''')

conn.commit()
conn.close()
print("✅ Comment table created.")
