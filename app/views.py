from app import app, db, lm
from flask import render_template, request, flash, redirect, session, url_for, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm
from wtforms.validators import ValidationError
from models import User
import datetime

@lm.user_loader
def load_user(userid):
    return User.get(userid)


@app.route("/")
@app.route("/index")
@login_required
def index():
	#user = {"nickname" : "Kirill"}
	#getting connected user ip
	ip = request.remote_addr
	return render_template("index.html",
							user_ip = ip)



@app.route("/login", methods = ["GET", "POST"])
def login():

	if current_user is not None and current_user.is_authenticated():
		flash("You are logged in already")
		return redirect(url_for("index"))

	login_form = LoginForm()
	remember_me= False

	#if login_form.validate_on_submit():





	return render_template("login.html",
							title="Log in",
							login_form=login_form)



@app.route("/register", methods = ["GET", "POST"])
def register():
	if current_user is not None and current_user.is_authenticated():
		flash("You are logged in already")
		return redirect(url_for("index"))

	register_form = RegisterForm()

	if register_form.validate_on_submit():

		email = register_form.email.data
		nickname = register_form.nickname.data
		password = register_form.password.data

		user = User(email=email, password = password,
					 reg_date = datetime.datetime.now(),
					 nickname = nickname)
		db.session.add(user)
		db.session.commit()

		return redirect(url_for('index'))




		flash("Welcome " + str(register_form.nickname.data)\
				 + ", you registred successfully!!")
		return redirect ("/login")
	return render_template("register.html",
							title="Register",
							register_form=register_form)
