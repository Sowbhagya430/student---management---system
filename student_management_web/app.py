from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize database
def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()
    return render_template('home.html', students=data)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        course = request.form['course']

        # your code to insert into DB
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, roll, course) VALUES (?, ?, ?)", (name, roll, course))
        conn.commit()
        conn.close()

        flash("✅ Student added successfully!")  # <-- ADD THIS LINE
        return redirect(url_for('home'))

    return render_template('add_student.html')

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    flash("🗑️ Student deleted.")  # <-- ADD THIS LINE
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        course = request.form['course']

        cursor.execute("UPDATE students SET name=?, roll=?, course=? WHERE id=?", (name, roll, course, id))
        conn.commit()
        conn.close()

        flash("✏️ Student updated.")  # <-- ADD THIS LINE
        return redirect(url_for('home'))

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit_student.html', student=student)

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit_student.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)