from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

try:
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'rohan@123',
        database = 'banking',      
    )
    message = 'Connected successfully!'
    print(message)
    cursor = conn.cursor()
    
except:
    results = ["*"]
    message = 'Database Not Connected'
    print(message)


# Track session ,currently inactive 
logged_in = 0 

# entry
@app.route("/")
def main():
    name = ''
    if name == '':
        return render_template('index.html',name = 'user')
    
    return render_template('index.html',name = name)

# show list of txns
@app.route("/transactions",methods=['GET'])
def transactions(name):
    return render_template('transaction.html',name = name)


def login_user(email,password):
    query = "SELECT customerID FROM banking.customer WHERE email = %s AND password = %s"
    values = (email,password)
    cursor.execute(query,values)
    result = cursor.fetchone()
    conn.commit()
    return result
    
@app.route("/login" , methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password']
        res = login_user(email,password)
        print("id :" , res[0])
        
        logged_in = 0
        
        if res[0]!='':
            logged_in = 1
        
        # get username 
        cursor.execute('SELECT customerID ,username FROM banking.customer where email = %s AND password = %s',(email,password))
        name = cursor.fetchone()
        
        # is logged in?
        if logged_in == 1:
            query = 'SELECT * FROM account as a , customer as c, transaction as d WHERE c.customerID= %s AND a.CustomerID = c.customerID AND a.AccountID = d.AccountID;'
            cursor.execute(query,[name[0]])
            res = cursor.fetchall()
            conn.commit()
            print(res)
            return transactions(res)
            
    return render_template('login.html')

# new_user add support
def add_new_user(name,username,phone_no,email,password):
    query = "INSERT INTO banking.customer (name,phone_no,email,password,username) VALUES (%s, %s, %s, %s, %s)"
    values= (name, phone_no, email, password, username)
    cursor.execute(query,values)
    print('added new user')
    conn.commit()
    
@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone_no = request.form['phone_no']
        username = request.form['username']
        # db opn
        add_new_user(name=name,username=username,phone_no=phone_no,email=email,password=password)
    return render_template('register.html')


# invalid endpoints
@app.errorhandler(404) 
def not_found(e):
    return render_template('error.html')



app.run(debug=True)