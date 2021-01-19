'''
On your PC, create a SQL database by the name of 'sdlproject'. In that database, create a table by the name of
'logininfo' with (id, name, email, password) as its fields respectively. Make sure that id is auto-incremented.
On line number 15, reset the password to the one on your machine.
'''

from flask import Flask, render_template, redirect, session, url_for, request
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.secret_key = "12345"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "sqlakshit"
app.config["MYSQL_DB"] = "sdlproject"

db = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from sdlproject.logininfo where email = %s and password = %s", (username, password))
            info = cursor.fetchone()
            if info is not None:
                if info['email'] == username and info['password'] == password:
                    session['loginsuccess'] = True
                    return redirect(url_for('profile'))
            else:
                return redirect(url_for('index'))
    return render_template("login.html")


@app.route('/new', methods=['GET', 'POST'])
def new_user():
    if request.method == "POST":
        if "one" in request.form and "two" in request.form and "three" in request.form:
            username = request.form['one']
            email = request.form['two']
            password = request.form['three']
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("insert into sdlproject.logininfo(name, password, email) values (%s, %s, %s)",
                        (username, password, email))
            db.connection.commit()
            return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/new/profile')
def profile():
    if session['loginsuccess']:
        return render_template("profile.html")


@app.route('/new/logout')
def logout():
    session.pop('loginsuccess', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
