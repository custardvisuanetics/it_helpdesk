import sqlite3

conn = sqlite3.connect("helpdesk.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE users ADD COLUMN display_name TEXT")
    print("✅ display_name column added")
except sqlite3.OperationalError as e:
    print("⚠️ display_name may already exist:", e)

conn.commit()
conn.close()
