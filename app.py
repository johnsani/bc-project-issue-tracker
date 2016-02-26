from flask import Flask, render_template, url_for
from flask import request, redirect
from flask import session, g
import sqlite3

app = Flask(__name__)
#Secret key to make sure the session is secure.
app.secret_key = '\xc36\x87F\xd9\xa2\x83\x9a\xa1Q1lg3\xe8\x118D\xbe\xae%\xa9^$'

@app.before_request
#Connects to the database after every request.
def before_request():
    g.db = sqlite3.connect("issuetracker.db")
@app.teardown_request
#Closes the databse after each request
def teardown_request(exception):
    if (hasattr(g, 'db')):
        g.db.close()

@app.route('/')
#Route to the index page
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
#Create new user
def signup():
    if request.method == 'POST':
        try:
            firstname = request.form['fname']
            lastname = request.form['lname']
            email = request.form['email']
            password = request.form['password']
            department = request.form['department']
            g.db.execute("INSERT INTO users \
                (fname, lname, email, department, password)VALUES (?,?,?,?,?)",
                (firstname, lastname, email, department, password))
            g.db.commit()
            msg = "Account created successfully!"
            return render_template('signup.html', msg=msg)
        except:
            msg = "error while creating account!"
            return render_template('signup.html', msg=msg)
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
#Logs a user in and returns the user tempalate
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db_email = g.db.execute("SELECT email FROM users")
        db_pass = g.db.execute("SELECT password FROM users")
        if email in db_email and password in db_pass:
            return redirect(url_for('user'))
        else:
            msg = "Invalid login details!"
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')

@app.route('/logout')
#Logs a user out
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.route('/admin', methods=['GET', 'POST'])
#returns template for the admin
def admin():
    return render_template('admin.html')


@app.route('/user', methods=['GET', 'POST'])
#Takes the user to the user page when logged in
def user():
    message = "Welcome "
    return render_template('user.html', message=message)

@app.route('/create', methods=['GET', 'POST'])
#Function for reporting new issues
def create():
    return render_template('create.html')


@app.route('/reports', methods=['GET', 'POST'])
#Retuns issues reported from the database
def reports():
    return render_template('reports.html')

if __name__ == '__main__':
    app.run(debug=True)
