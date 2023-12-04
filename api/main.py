from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import os

app = Flask(__name__)

#database_path = os.path.join(app.root_path, 'instance', 'users.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://default:ZFu7KC3xYhUg@ep-red-sun-42046104.us-east-1.postgres.vercel-storage.com:5432/verceldb'
#psql "postgres://default:ZFu7KC3xYhUg@ep-red-sun-42046104.us-east-1.postgres.vercel-storage.com:5432/verceldb"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:iCYTEGcgJBNSqJP0ZumXxkT@localhost/our_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = "my super secret key"

db = SQLAlchemy(app)
app.app_context().push()

class Users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(100), nullable=False, unique=True)
  date_added = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<Name %r>' % self.name

#Form
class UserForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  email = StringField("Email", validators=[DataRequired()])
  submit = SubmitField("Submit")

class NameForm(FlaskForm):
	name = StringField("What's Your Name", validators=[DataRequired()])
	submit = SubmitField("Submit")

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
  name = None
  form = UserForm()
  if form.validate_on_submit():
    user = Users.query.filter_by(email=form.email.data).first()
    if user is None:
      user = Users(name=form.name.data, email=form.email.data)
      db.session.add(user)
      db.session.commit()
    name = form.name.data
    form.name.data = ''
    form.email.data = ''
    flash("User Added Successfully!")
  our_users = Users.query.order_by(Users.date_added)
  return render_template("add_user.html", form=form, name=name, our_users=our_users)

@app.route('/')
def index():
  first_name = "Rowdy"
  return render_template("index.html", first_name=first_name)

@app.route('/user/<name>')

def user(name):
  return render_template("user.html", username=name)

#Error Pages
@app.errorhandler(404)
def page_not_found(e):
  return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
  return render_template("500.html"), 500

@app.route('/name', methods=['GET', 'POST'])
def name():
  name = None
  form = NameForm()
  if form.validate_on_submit():
    name = form.name.data
    form.name.data = ''
    flash("Form Submitted Successfully!")

  return render_template("name.html", name=name, form=form)