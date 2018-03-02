# import os

from flask import Flask, render_template, flash, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

# basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
SQLALCHEMY_DATABASE_URI = 'sqlite:///flasklogin.sqlite3'

app = Flask(__name__)
app.secret_key = "04dc6238-1d87-11e8-b2ed-e82aea18273e"
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)
db.init_app(app)

class Username(db.Model):
    __tablename__ = 'users'
    id = db.Column('usernames_id', db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(60))
    password = db.Column(db.String(50))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return render_template('index.html',user = username)


@app.route('/login', methods = ['GET', 'POST'] )
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        usernametocheck = request.form['username']
        passwordtocheck = request.form['password']

        # user = Username.query.filter_by(username=usernametocheck).first()
         user = Username.query.filter_by(username=usernametocheck).first()
        if user is None:
            return "Not Found"
        else:
            return "Found " + request.form['username']
        # session['username'] = usernametocheck

        return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        emailconfirm = request.form['emailconfirm']
        password = request.form['password']
        passwordconfirm = request.form['passwordconfirm']

        #flash ('username'+ username + 'email' + email + 'password' + password)
        newuser = Username(username, email, password)

        db.session.add(newuser)
        db.session.commit()


        return redirect(url_for('index'))
        # return redirect(url_for('index.html'))

@app.route('/logoff')
def logoff():
    if 'username' in session:
        session.pop('username',None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
