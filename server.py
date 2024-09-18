from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import eventlet

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# Simulated account balance
account_balance = 1000.0

@app.route('/')
def index():
    return "Banking Transaction System"

# Route to handle deposits
@app.route('/deposit', methods=['POST'])
def deposit():
    global account_balance
    amount = float(request.json.get('amount'))
    account_balance += amount
    # Broadcast to all subscribers about the updated balance
    socketio.emit('transaction', {'type': 'deposit', 'amount': amount, 'balance': account_balance})
    return jsonify({"status": "Deposit successful", "balance": account_balance})

# Route to handle withdrawals
@app.route('/withdraw', methods=['POST'])
def withdraw():
    global account_balance
    amount = float(request.json.get('amount'))
    if amount > account_balance:
        return jsonify({"status": "Insufficient funds", "balance": account_balance}), 400
    
    account_balance -= amount
    # Broadcast to all subscribers about the updated balance
    socketio.emit('transaction', {'type': 'withdraw', 'amount': amount, 'balance': account_balance})
    return jsonify({"status": "Withdrawal successful", "balance": account_balance})

# Socket connection handler
@socketio.on('connect')
def on_connect():
    print("Client connected")
    # Send the current balance to the client upon connection
    emit('balance', {'balance': account_balance})

@socketio.on('disconnect')
def on_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, debug=True)
