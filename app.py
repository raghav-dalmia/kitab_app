from flask import Flask, render_template, redirect, request, flash, send_from_directory, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from datetime import datetime
import smtplib
import os
from constants import *
import csv_writer


app = Flask(__name__)
app.secret_key = 'fijsdahfiw234242wdashifn9328678324y32687hwu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/raghav/Desktop/kitab_app/share_kitab.db'
app.config['UPLOAD_FOLDER'] = "/home/raghav/Desktop/kitab_app/static/images"
db = SQLAlchemy(app)



# s = smtplib.SMTP('smtp.gmail.com', 587)
# s.starttls()
# s.login(me, password) 


class Book(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(50), nullable=False)
	title = db.Column(db.String(50), nullable=False)
	category = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(200), nullable=False)
	phone = db.Column(db.Integer, nullable=False)
	location = db.Column(db.String(50), nullable=False)
	createdOn = db.Column(db.DateTime, default=datetime.now())
	image_path = db.Column(db.String(300), default="book.jpg")

	def get_book_as_tuple(self, status):
		return (self.username, self.email, self.title, self.category, self.phone, self.description, self.location, self.createdOn, datetime.now(), status)

	def __repr__(self):
		return "{} {}".format(self.email, self.title) 

class Comments(db.Model):
	__tablename__ = "Comments"

	id = db.Column(db.Integer, primary_key = True)
	pid = db.Column(db.Integer)
	comment = db.Column(db.String(100), nullable=False)
	createdOn = db.Column(db.DateTime, default=datetime.now())

	def __repr__(self):
		return "{} {}".format(self.pid, self.comment) 

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html')

@app.errorhandler(500)
def page_not_found(e):
  return render_template('404.html')

@app.errorhandler(410)
def page_not_found(e):
  return render_template('404.html')

@app.route('/')
def home():

	csv_writer.write(
		"/home/raghav/Desktop/kitab_app/user_data/url_hits.csv",
		("/", datetime.now())
	)

	def helper(s):
		return "" if(s=="" or s=="-Select-" or s=="" or s==None) else s

	location = helper(request.args.get('form-location'))
	email = helper(request.args.get('form-email'))
	category = helper(request.args.get('form-category'))
	
	if(location=="" and category=="" and email==""):
		books = Book.query.all()
	else:

		csv_writer.write(
			"/home/raghav/Desktop/kitab_app/user_data/searchs.csv",
			(location, email, category)
		)

		if(location=="" and email==""):
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
	return render_template('index.html', books = books, locations = LOCATIONS, categories = CATEGORIES)

@app.route('/donate-book')
def donate_book():

	csv_writer.write(
		"/home/raghav/Desktop/kitab_app/user_data/url_hits.csv",
		("/donate-book", datetime.now())
	)

	return render_template('donate_book.html', locations = LOCATIONS, categories = CATEGORIES)

@app.route('/about-us')
def about_us():

	csv_writer.write(
		"/home/raghav/Desktop/kitab_app/user_data/url_hits.csv",
		("/about-us", datetime.now())
	)

	return render_template('about_us.html', locations = LOCATIONS, categories = CATEGORIES)

@app.route('/donation-form', methods=['POST'])
def donation_form():

	csv_writer.write(
		"/home/raghav/Desktop/kitab_app/user_data/url_hits.csv",
		("/donation-form", datetime.now())
	)
	
	username = request.form['form-name']
	email = request.form['form-email']
	phone = request.form['form-phone']
	title = request.form['form-title']
	category = request.form['form-category']
	description = request.form['form-description']
	location = request.form['form-location']
	try:
		file = request.files['file']
		if(file.filename==""):
			filename = ""
		else:
			filename = datetime.datetime.now().strftime("%a,%d_%b_%Y_%H:%M:%S") + secure_filename(file.filename)
			image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(image_path)
	except:
		filename = ""

	try:
		book = Book(
			username = username, 
			email = email, 
			title = title, 
			category = category, 
			description = description, 
			phone = phone,
			location = location, 
			image_path = filename
		)

		db.session.add(book)
		db.session.commit()
		flash("Your card created successfully. Thank you for your interest.","alert-success")
	except:
		flash("Some error occur. Please try again later!!","alert-danger")


	return redirect('/')


@app.route('/add-comment', methods=['POST'])
def add_comment():

	csv_writer.write(
		"/home/raghav/Desktop/kitab_app/user_data/url_hits.csv",
		("/add-comment", datetime.now())
	)

	comment = request.form['form-comment']
	id = request.form['form-id']

	try:
		comment = Comments(
			pid = id,
			comment = comment
		)

		db.session.add(comment)
		db.session.commit()
		flash("Comment posted successfully!","alert-success")
	except:
		flash("Please try again later.","alert-warning")

	return redirect('/book/{}/get'.format(id))

@app.route('/book/<id>/get')
def show_book(id):

	csv_writer.write(
		"/home/raghav/Desktop/kitab_app/user_data/url_hits.csv",
		("/book/{}/get".format(id), datetime.now())
	)

	book = Book.query.filter_by(id = id)
	print(type(book))
	# return "Abc"
	return render_template('show_book.html', book = book[0], locations = LOCATIONS, categories = CATEGORIES, comments = Comments.query.filter_by(pid = id))

@app.route('/book/<id>/request', methods=['POST'])
def request_book(id):
	book = Book.query.filter_by(id = id)[0]
	username = request.form['form-name']
	phone = request.form['form-phone']
	reason = request.form['form-reason']
	address = request.form['form-address']

	csv_writer.write(
		"/home/raghav/Desktop/kitab_app/user_data/requested_books.csv",
		(username, phone, reason, address)
	)

	message = '''
Hi {},\n
Request for your book {} on Share Kitaab.\n
Details:\n
	Requested by: {}
	Phone Number: {}
	Reason: {}
	'''.format(
		book.username,
		book.title,
		username,
		phone,
		reason,
	)
	try:
		s.sendmail(me, book.email, message)	
		flash("Request is sent to owner.","alert-success")
	except:
		flash("Please try again later!!","alert-danger")
	return redirect('/book/{}/get'.format(id))

@app.route('/book/delete/verify', methods=['POST'])
def delete_book_verify():

	csv_writer.write(
		"/home/raghav/Desktop/kitab_app/user_data/url_hits.csv",
		("/book/delete/verify", datetime.now())
	)
	
	id = request.form['form-id']
	book = Book.query.filter_by(id = id)[0]
	email = request.form['form-email']
	if(email == book.email):
		try:
			image_path = os.path.join(app.config['UPLOAD_FOLDER'], book.image_path)
			db.session.delete(book)
			db.session.commit()

			csv_writer.write(
				"/home/raghav/Desktop/kitab_app/user_data/deleted_cards.csv",
				book.get_book_as_tuple("verified")
			)

			if(os.path.exists(image_path) and os.path.isfile(image_path)):
				os.remove(image_path)

			flash("Deleted successfully!!","alert-success")
		except:

			csv_writer.write(
				"/home/raghav/Desktop/kitab_app/user_data/failed_delete.csv",
				(id, email, datetime.now())
			)

			flash("Please try again later!!","alert-danger")
	else:

		csv_writer.write(
			"/home/raghav/Desktop/kitab_app/user_data/failed_delete.csv",
			(id, email, datetime.now())
		)
		
		flash("Please enter your registered Eamil ID!!","alert-warning")

	return redirect('/')

@app.route('/book/<id>/delete')
def delete_book(id):
	
	csv_writer.write(
		"/home/raghav/Desktop/kitab_app/user_data/url_hits.csv",
		("/book/{}/delete".format(id), datetime.now())
	)

	book = Book.query.filter_by(id = id)[0]
	csv_writer.write(
		"/home/raghav/Desktop/kitab_app/user_data/deleted_cards.csv",
		book.get_book_as_tuple("not verified")
	)
	image_path = os.path.join(app.config['UPLOAD_FOLDER'], book.image_path)
	db.session.delete(book)
	db.session.commit()
	os.remove(image_path)
	return redirect('/')

if __name__ == '__main__':
	db.create_all()
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run()