from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0211'
app.config['MYSQL_DB'] = 'mydatabase'

# Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO users (name) VALUES (%s)', [name])
    mysql.connection.commit()
    flash('User added successfully!')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_user(id):
    name = request.form['name']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE users SET name = %s WHERE id = %s', [name, id])
    mysql.connection.commit()
    flash('User updated successfully!')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', [id])
    mysql.connection.commit()
    flash('User deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
