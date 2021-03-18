from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/raghav/Desktop/kitab_app/share_kitab.db'
db = SQLAlchemy(app)


class Book(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(50), nullable=False)
	title = db.Column(db.String(50), nullable=False)
	category = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(200), nullable=False)
	phone = db.Column(db.Integer, nullable=False)
	address = db.Column(db.String(100), nullable=False)
	location = db.Column(db.String(50), nullable=False)
	createdOn = db.Column(db.DateTime, default=datetime.datetime.utcnow)

	def __repr__(self):
		return '<User %r>' % self.username


@app.route('/')
def home():

	def helper(s):
		return "" if(s=="" or s=="-Select-" or s=="" or s==None) else s

	location = helper(request.args.get('form-location'))
	email = helper(request.args.get('form-email'))
	category = helper(request.args.get('form-category'))
	
	if(location=="" and category=="" and email==""):
		books = Book.query.all()
	elif(location=="" and email==""):
		books = Book.query.filter_by(category=category)
	elif(category=="" and email==""):
		books = Book.query.filter_by(location=location)
	elif(category=="" and location==""):
		books = Book.query.filter_by(email=email)
	elif(email==""):
		books = Book.query.filter_by(location=location, category = category)
	elif(location==""):
		books = Book.query.filter_by(email=email, category = category)
	elif(category==""):
		books = Book.query.filter_by(location=location, email = email)
	else:
		books = Book.query.filter_by(location=location, email=email, category = category)
	print(books)
	return render_template('index.html', books = books)

@app.route('/donate-book')
def donate_bool():
	return render_template('donate_book.html')

@app.route('/about-us')
def about_us():
	return render_template('about_us.html')

@app.route('/donation-form', methods=['POST'])
def donation_form():
	username = request.form['form-name']
	email = request.form['form-email']
	phone = request.form['form-phone']
	title = request.form['form-title']
	category = request.form['form-category']
	description = request.form['form-description']
	location = request.form['form-location']
	address = request.form['form-address']

	book = Book(username = username, email = email, title = title, category = category, description = description, phone = phone, address = address, location = location)
	db.session.add(book)
	db.session.commit()

	return redirect('/')


@app.route('/book/<id>/get')
def showBook(id):
	return render_template('show_book.html', book = Book.query.filter_by(id = id)[0])



if __name__ == '__main__':
	db.create_all()
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(debug = True)