from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import datetime
import smtplib


app = Flask(__name__)
app.secret_key = 'fijsdahfiw234242wdashifn9328678324y32687hwu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/raghav/Desktop/kitab_app/share_kitab.db'
db = SQLAlchemy(app)

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls() 
me = input("Email id: ")
password = input("Password: ")
s.login(me, password) 


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
		return "{} {}".format(self.email, self.title) 


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

	try:
		book = Book(username = username, email = email, title = title, category = category, description = description, phone = phone, address = address, location = location)
		db.session.add(book)
		db.session.commit()
		flash("Your card created successfully. Thank you for your interest.","alert-success")
	except:
		flash("Some error occur. Please try again later!!","alert-danger")


	return redirect('/')


@app.route('/book/<id>/get')
def show_book(id):
	return render_template('show_book.html', book = Book.query.filter_by(id = id)[0])

@app.route('/book/<id>/request', methods=['POST'])
def request_book(id):
	book = Book.query.filter_by(id = id)[0]
	username = request.form['form-name']
	email = request.form['form-email']
	phone = request.form['form-phone']
	school = request.form['form-school']
	reason = request.form['form-reason']
	location = request.form['form-location']
	address = request.form['form-address']
	message = '''
Hi {},\n
Request for your book {} on Share Kitaab.\n
Details:\n
	Requested by: {}
	Email ID: {}
	Phone Number: {}
	School Name: {}
	Reason: {}	
	Loaction: {}
	Address: {}
	'''.format(
		book.username,
		book.title,
		username,
		email,
		phone,
		school,
		reason,
		location,
		address
	)
	try:
		s.sendmail(me, book.email, message)	
		flash("Request is sent to owner.","alert-success")
	except:
		flash("Please try again later!!","alert-danger")
	return redirect('/book/{}/get'.format(id))

@app.route('/book/delete/verify', methods=['POST'])
def delete_book_verify():
	id = request.form['form-id']
	print(id)
	book = Book.query.filter_by(id = id)[0]
	email = request.form['form-email']
	print("email: ", email)
	if(email == book.email):
		try:
			s.sendmail(me, book.email, "/book/{}/delete")
			flash("Delete link is sent to your email.","alert-success")
		except:
			flash("Please try again later!!","alert-danger")
	else:
		flash("Please enter your registered Eamil ID!","alert-warning")

	return redirect('/')

if __name__ == '__main__':
	db.create_all()
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(debug = True)