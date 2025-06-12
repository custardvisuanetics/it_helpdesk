import sqlite3

conn = sqlite3.connect("helpdesk.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    print("✅ created_at added")
except sqlite3.OperationalError as e:
    print("⚠️ created_at may already exist:", e)

try:
    c.execute("ALTER TABLE users ADD COLUMN last_login TIMESTAMP")
    print("✅ last_login added")
except sqlite3.OperationalError as e:
    print("⚠️ last_login may already exist:", e)

conn.commit()
conn.close()
