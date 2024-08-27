from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = ' key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rohan@123'
app.config['MYSQL_DB'] = 'banking'


# Intialize MySQL
mysql = MySQL(app)

@app.route("/home")
def hello_world():
    return render_template('transaction.html')

@app.route("/login" , methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        email= request.form['email']
        password = request.form['password']
        app.logger('account logged in! '+ email + password)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE Email = %s AND Password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)
            
    return render_template('login.html')


@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST' and request.form == 'name'  and 'username' in request.form and 'phone_no' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form['name']
        email = request.form['username']
        password = request.form['password']
        phone_no = request.form['phone_no']
        username = request.form['username']
        app.logger(email+username+phone_no+name)
        # cursor.execute('INSERT INTO customer (Name, Phone_Number, Email, Password, Username) VALUES (%s,%s , %s ,%s, %s)',(name,username,phone_no,email,password))
        app.logger('db save!')
    return render_template('register.html')

@app.errorhandler(404) 
def not_found(e):
    return render_template('error.html')


app.run(debug=True)