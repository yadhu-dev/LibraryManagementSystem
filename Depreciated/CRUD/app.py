from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your generated secret key

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="lms"
)

@app.route('/')
def index():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM details')
    users = cursor.fetchall()
    cursor.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    if not name:
        flash('Name is required!')
        return redirect(url_for('index'))
    cursor = mydb.cursor()
    cursor.execute('INSERT INTO details (name) VALUES (%s)', (name,))
    mydb.commit()
    cursor.close()
    flash('User added successfully!')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_user(id):
    name = request.form['name']
    if not name:
        flash('Name is required!')
        return redirect(url_for('index'))
    cursor = mydb.cursor()
    cursor.execute('UPDATE details SET name = %s WHERE id = %s', (name, id))
    mydb.commit()
    cursor.close()
    flash('User updated successfully!')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_user(id):
    cursor = mydb.cursor()
    cursor.execute('DELETE FROM details WHERE id = %s', (id,))
    mydb.commit()
    cursor.close()
    flash('User deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
