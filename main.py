from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Customer, Account, Transaction

app = Flask(__name__)

# Create the tables if they don't exist
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route("/")
def main():
    return render_template('index.html', name='user')

@app.route("/transactions")
def transactions():
    return render_template('transaction.html', name='user')

@app.route("/api/add_transaction", methods=['POST'])
def add_transaction():
    data = request.json
    AccountID = data.get('AccountID')
    type = data.get('type')
    Amount = data.get('Amount')

    if not all([AccountID, type, Amount]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        db = next(get_db())
        transaction = Transaction(
            TransactionID='generated-uuid',  # You should generate UUID here
            AccountID=AccountID,
            type=type,
            Amount=Amount
        )
        db.add(transaction)
        db.commit()
        return jsonify({"status": "success", "message": "Transaction added successfully"})
    except Exception as e:
        db.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = next(get_db())
        user = db.query(Customer).filter(Customer.email == email, Customer.password == password).first()
        print(f"user:{user.name}")
        if user:
            # Fetch transactions
            accounts = db.query(Account).filter(Account.CustomerID == user.customerID).all()
            print("Accounts found:")
            for account in accounts:
                print(f"AccountID: {account.AccountID}, Balance: {account.Balance}")

            transactions = db.query(Transaction).filter(Transaction.AccountID.in_([acc.AccountID for acc in accounts])).all()
            print("Transactions found:")
            for transaction in transactions:
                print(f"TransactionID: {transaction.TransactionID}, AccountID: {transaction.AccountID}, Type: {transaction.type}, Amount: {transaction.Amount}, Timestamp: {transaction.Timestamp}")
            data = {
                    'transactions': transactions,
                    'accounts': accounts
                }
            return render_template('transaction.html', name=data,user=user)
        
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone_no = request.form['phone_no']
        username = request.form['username']
        db = next(get_db())
        new_user = Customer(name=name, email=email, password=password, phone_no=phone_no, username=username)
        db.add(new_user)
        db.commit()
    return render_template('register.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html')

@app.route("/no_txns")
def no_elements():
    return render_template('empty_list.html')
