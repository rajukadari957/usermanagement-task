from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database setup
def init_sqlite_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, phone TEXT, email TEXT, address TEXT)')
    conn.close()

init_sqlite_db()

# Home - Read operation (View all users)
@app.route('/')
def index():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('index.html', users=users)

# Create operation (Create new user)
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        
        # Validation
        if not first_name or not last_name or not phone or not email:
            flash('Please fill out all required fields!')
            return redirect(url_for('create'))
        
        conn = sqlite3.connect('users.db')
        conn.execute('INSERT INTO users (first_name, last_name, phone, email, address) VALUES (?, ?, ?, ?, ?)', 
                     (first_name, last_name, phone, email, address))
        conn.commit()
        conn.close()
        flash('User created successfully!')
        return redirect(url_for('index'))
    
    return render_template('create.html')

# Update operation (Edit user)
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('SELECT * FROM users WHERE id=?', (id,))
    user = cursor.fetchone()
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        
        # Validation
        if not first_name or not last_name or not phone or not email:
            flash('Please fill out all required fields!')
            return redirect(url_for('update', id=id))
        
        conn.execute('UPDATE users SET first_name=?, last_name=?, phone=?, email=?, address=? WHERE id=?', 
                     (first_name, last_name, phone, email, address, id))
        conn.commit()
        conn.close()
        flash('User updated successfully!')
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('update.html', user=user)

# Delete operation (Delete user)
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('users.db')
    conn.execute('DELETE FROM users WHERE id=?', (id,))
    conn.commit()
    conn.close()
    flash('User deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
