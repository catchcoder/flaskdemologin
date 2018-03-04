import os
import uuid
import yaml

from flask import Flask, render_template, flash, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_mail import Mail, Message
from urllib import parse

# Load yaml file with config setting
# basedir = os.getcwd()
# with open(os.path.join(basedir, 'config.yml'), 'r') as ymlfile:'
with open('config.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

# Flask app and secret
app = Flask(__name__)
app.secret_key = "04dc6238-1d87-11e8-b2ed-e82aea18273e"

#Mailer
mail=Mail(app)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER= cfg['mail']['MAIL_SERVER'],
	MAIL_PORT= cfg['mail']['MAIL_PORT'],
	MAIL_USE_SSL=True,
	MAIL_USERNAME = cfg['mail']['MAIL_USERNAME'],
	MAIL_PASSWORD = cfg['mail']['MAIL_PASSWORD']
)

mail=Mail(app)


# Database connectiona and table
app.config['SQLALCHEMY_DATABASE_URI'] = cfg['database']['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all()
db.init_app(app)

class Username(db.Model):
    __tablename__ = 'users'
    id = db.Column('usernames_id', db.Integer, primary_key = True)
    username = db.Column('username', db.String(100))
    email = db.Column('email', db.String(60))
    password = db.Column('password', db.String(50))
    accountlive = db.Column('accountlive', db.Boolean, nullable=False, default=False)
    emailcheckcode = db.Column('emailcheckcode', db.String(36))


    def __init__(self, username, email, password, accountlive, emailcheckcode):
        self.username = username
        self.email = email
        self.password = password
        self.accountlive = accountlive
        self.emailcheckcode = emailcheckcode

# Routes
@app.route('/')
def index():
    if 'email' in session:
        email = session['email']
    else:
        email = None
    return render_template('index.html',email = email)


@app.route('/login', methods = ['GET', 'POST'] )
def login():
    if request.method == 'GET':
        id = request.args.get('login')

        return render_template('login.html',id = id)
    elif request.method == 'POST':
        emailtocheck = request.form['email']
        passwordtocheck = request.form['password']

        # user = Username.query.filter_by(username=usernametocheck).first()
        user = Username.query.filter_by(email=emailtocheck).first()
        if user is None:
            return redirect(url_for('login', login='failed'))
        if not user.accountlive:
            return redirect(url_for('login', login='emailnotverified'))
        if passwordtocheck == user.password:
            session['email'] = emailtocheck
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login',login='failed'))
        # session['username'] = usernametocheck

        return redirect(url_for('login', login='failed'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        id = request.args.get('id')
        return render_template('register.html', id=id)
    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        #emailconfirm = request.form['emailconfirm']
        password = request.form['password']
        #passwordconfirm = request.form['passwordconfirm']
        emailcheckcode = str(uuid.uuid1())

        user = Username.query.filter_by(email=email).first()
        if user is None:
            #flash ('username'+ username + 'email' + email + 'password' + password)
            newuser = Username(username, email, password, False, emailcheckcode)
            db.session.add(newuser)
            db.session.commit()

            confirmurl = "http://localhost/" + parse.quote(email) + "/" + emailcheckcode

            msg = Message(subject="FlaskLogin confirm registation",
                          body= confirmurl,
                          sender="Register@flasklogin.com",
                          recipients=[email])

            mail.send(msg)

            return redirect(url_for('login', id='emailsent'))
        else:
            return redirect(url_for('register', id='emailexist'))
        # return redirect(url_for('index.html'))r

@app.route('/logoff')
def logoff():
    if 'username' in session:
        session.pop('username',None)
    return redirect(url_for('index'))


@app.route('/<email>/<authcheck>')
def authcheck(email, authcheck):

    user = Username.query.filter_by(email=email).first()
    if user is None:
        return ('not in db')

    if user.emailcheckcode == authcheck:
        user.accountlive = True
        db.session.commit()
        return ('yes it checked out')

    else:
        return ('sadly it doesn\'t match')



    return ("email {} \br authcode {}".format(emailaddress,authcode))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
