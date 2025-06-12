from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this!

DB = "helpdesk.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.before_request
def load_user():
    g.user = session.get('user')
    g.role = session.get('role')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            session['role'] = user['role']
            conn.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = ?", (username,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        return "❌ Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    conn = get_db()
    tickets = conn.execute('SELECT * FROM tickets ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', tickets=tickets, user=g.user)

@app.route('/create', methods=['GET', 'POST'])
@login_required
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
@login_required
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

@app.route('/delete/<int:ticket_id>', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    if g.role != 'admin':
        return "⛔ Access denied. Only admins can delete tickets.", 403
    conn = get_db()
    conn.execute('DELETE FROM tickets WHERE id = ?', (ticket_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, hashed_password, 'technician'))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "❌ Username already exists"
        conn.close()

        session['user'] = username  # auto-login
        session['role'] = 'technician'  # <-- Important!
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/users')
@login_required
def manage_users():
    if g.role != 'admin':
        return "⛔ Access denied. Admins only.", 403

    conn = get_db()
    users = conn.execute("SELECT id, username, role, created_at, last_login FROM users ORDER BY username").fetchall()
    conn.close()
    return render_template("manage_users.html", users=users)

@app.route('/change_role/<int:user_id>', methods=['POST'])
@login_required
def change_role(user_id):
    if g.role != 'admin':
        return "⛔ Access denied.", 403

    new_role = request.form['role']
    conn = get_db()
    conn.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_users'))

if __name__ == '__main__':
    app.run(debug=True)
