from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('finance.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create the database and table if they don't exist
def init_db():
    if not os.path.exists('finance.db'):
        # Create the database file and table if not exists
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT CHECK(type IN ('income', 'expense')) NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("Database and table created successfully!")
    else:
        print("Database already exists.")

# Initialize the database before the app runs
init_db()

# Route to show all transactions
@app.route('/')
def index():
    conn = get_db_connection()
    transactions = conn.execute("SELECT * FROM transactions ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("index.html", transactions=transactions)

# Route to add a new transaction
@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        date = request.form["date"]
        type_ = request.form["type"]
        category = request.form["category"]
        amount = request.form["amount"]
        description = request.form["description"]

        if not date or not type_ or not category or not amount:
            flash("All fields are required!")
            return redirect(url_for("add"))

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO transactions (date, type, category, amount, description) VALUES (?, ?, ?, ?, ?)",
            (date, type_, category, amount, description),
        )
        conn.commit()
        conn.close()
        flash("Transaction added successfully!")
        return redirect(url_for("index"))

    return render_template("add.html")

# Route to edit a transaction
@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    conn = get_db_connection()
    transaction = conn.execute("SELECT * FROM transactions WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        date = request.form["date"]
        type_ = request.form["type"]
        category = request.form["category"]
        amount = request.form["amount"]
        description = request.form["description"]

        if not date or not type_ or not category or not amount:
            flash("All fields are required!")
            return redirect(url_for("edit", id=id))

        conn.execute(
            "UPDATE transactions SET date = ?, type = ?, category = ?, amount = ?, description = ? WHERE id = ?",
            (date, type_, category, amount, description, id),
        )
        conn.commit()
        conn.close()
        flash("Transaction updated successfully!")
        return redirect(url_for("index"))

    conn.close()
    return render_template("edit.html", transaction=transaction)

# Route to delete a transaction
@app.route('/delete/<int:id>', methods=["POST"])
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM transactions WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Transaction deleted successfully!")
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
