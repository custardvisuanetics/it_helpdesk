from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "helpdesk.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    tickets = conn.execute('SELECT * FROM tickets ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', tickets=tickets)

@app.route('/create', methods=['GET', 'POST'])
def create_ticket():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        priority = request.form['priority']
        conn = get_db()
        conn.execute('INSERT INTO tickets (title, description, category, priority) VALUES (?, ?, ?, ?)',
                     (title, description, category, priority))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create_ticket.html')

@app.route('/update/<int:ticket_id>', methods=['GET', 'POST'])
def update_ticket(ticket_id):
    conn = get_db()
    ticket = conn.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()

    if request.method == 'POST':
        new_status = request.form['status']
        conn.execute('UPDATE tickets SET status = ? WHERE id = ?', (new_status, ticket_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('update_ticket.html', ticket=ticket)

if __name__ == '__main__':
    app.run(debug=True)
