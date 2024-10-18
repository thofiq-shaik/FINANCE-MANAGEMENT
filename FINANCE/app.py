from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 type TEXT, amount REAL, description TEXT)''')
    conn.commit()
    conn.close()

# Home route with form to add transactions
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        transaction_type = request.form['type']
        amount = float(request.form['amount'])
        description = request.form['description']
        add_transaction(transaction_type, amount, description)
        return redirect(url_for('dashboard'))

    return render_template_string(index_html)

# Add transaction to the database
def add_transaction(transaction_type, amount, description):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (type, amount, description) VALUES (?, ?, ?)",
              (transaction_type, amount, description))
    conn.commit()
    conn.close()

# Dashboard to show income, expense summary, and available balance
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()

    # Calculate total income and expenses
    income = sum([t[2] for t in transactions if t[1] == 'Income'])
    expenses = sum([t[2] for t in transactions if t[1] == 'Expense'])
    available_balance = income - expenses  # Calculate available balance
    conn.close()

    return render_template_string(dashboard_html, transactions=transactions, income=income, expenses=expenses, available_balance=available_balance)

# HTML and CSS for the homepage (index)
index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Finance Management System</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            background-color: #f4f4f4; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
        }
        .container {
            max-width: 500px;
            width: 100%;
            padding: 20px;
            background-color: #fff; 
            border-radius: 8px; 
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1, h2 { color: #333; text-align: center; }
        form { margin-top: 20px; }
        form label { display: block; margin-bottom: 8px; color: #555; }
        form input, select { width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 5px; border: 1px solid #ddd; }
        form button { padding: 10px 15px; background-color: #28a745; color: #fff; border: none; border-radius: 5px; cursor: pointer; width: 100%; }
        form button:hover { background-color: #218838; }
        a { display: inline-block; margin-top: 20px; padding: 10px 15px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px; text-align: center; width: 100%; }
        a:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Finance Management System</h1>
        <form action="/" method="POST">
            <label for="type">Type:</label>
            <select name="type" required>
                <option value="Income">Income</option>
                <option value="Expense">Expense</option>
            </select>
            <label for="amount">Amount:</label>
            <input type="number" name="amount" step="0.01" required>
            <label for="description">Description:</label>
            <input type="text" name="description" required>
            <button type="submit">Add Transaction</button>
        </form>

        <a href="/dashboard">Go to Dashboard</a>
    </div>
</body>
</html>
'''

# HTML and CSS for the dashboard
dashboard_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Finance Dashboard</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            background-color: #f4f4f4; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
        }
        .container {
            max-width: 800px;
            width: 100%;
            padding: 20px;
            background-color: #fff; 
            border-radius: 8px; 
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1, h2 { color: #333; text-align: center; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        table, th, td { border: 1px solid #ddd; }
        th, td { padding: 12px; text-align: left; }
        th { background-color: #007bff; color: white; }
        td { background-color: #fff; }
        a { display: inline-block; margin-top: 20px; padding: 10px 15px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px; text-align: center; width: 100%; }
        a:hover { background-color: #0056b3; }
        p { font-size: 1.2em; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Dashboard</h1>

        <h2>Summary</h2>
        <p>Total Income: ₹{{ income }}</p>
        <p>Total Expenses: ₹{{ expenses }}</p>
        <p>Available Balance: ₹{{ available_balance }}</p> <!-- Display available balance -->

        <h2>Transactions</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Type</th>
                <th>Amount</th>
                <th>Description</th>
            </tr>
            {% for transaction in transactions %}
            <tr>
                <td>{{ transaction[0] }}</td>
                <td>{{ transaction[1] }}</td>
                <td>₹{{ transaction[2] }}</td>
                <td>{{ transaction[3] }}</td>
            </tr>
            {% endfor %}
        </table>

        <a href="/">Add another transaction</a>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
