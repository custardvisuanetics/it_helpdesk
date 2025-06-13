import sqlite3

conn = sqlite3.connect("helpdesk.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE tickets ADD COLUMN created_by TEXT")
    print("✅ created_by column added.")
except sqlite3.OperationalError as e:
    print("⚠️ Might already exist:", e)

conn.commit()
conn.close()
