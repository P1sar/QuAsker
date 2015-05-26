from app import app, db, lm
from flask import render_template, request, flash, redirect, session, url_for, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm, EditProfile, EditAvatar
from wtforms.validators import ValidationError
from models import User
from datetime import datetime
from werkzeug import secure_filename
import os

@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
@app.route("/index")
def index():

    ip = request.remote_addr
    return render_template("index.html",
                            user_ip = ip)



@app.route("/login", methods = ["GET", "POST"])
def login():

    if current_user is not None and current_user.is_authenticated():
        flash("You are logged in already")
        return redirect(url_for("index"))

    login_form = LoginForm()


    if login_form.validate_on_submit():
        get_password = login_form.password.data
        #looking for an a existing email in our database
        get_user = User.query.filter_by(email=login_form.email.data)

        if get_user:

            for item in get_user:
                user_id = item.id
                user_pass = item.password
                user = User.query.get(user_id)

                if user_pass == get_password:
                    #compering password form login from with pass in database
                    user.is_authenticated = True
                    user.last_seen = datetime.now()
                    remember_me = login_form.remember_me.data
                    db.session.add(user)
                    db.session.commit()
                    login_user(user, remember = remember_me)


                    return redirect ("/")

        flash("Incorrect Login or Password", category = 'error')

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
                     reg_date = datetime.utcnow(),
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

@app.route("/logout")
def logout():
    logout_user()
    flash("Goodbuy! We will miss you...")
    return redirect(url_for("index"))

@app.route("/user/<nickname>")
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash("User" + nickname + "not found")
        return redirect(url_for("index"))

    return render_template('user.html',
                            user = user)


@app.route('/edit_profile', methods = ['GET','POST'])
@login_required

def edit():

    edit_form = EditProfile()
    edit_avatar = EditAvatar()

    if edit_avatar.avatar.data:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.nickname + ".png")
        edit_avatar.avatar.data.save(file_path)

    if edit_form.validate_on_submit():
        about_me = edit_form.about_me.data
        current_user.about_me = edit_form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('edit'))


    return render_template('edit_profile.html', edit_form = edit_form, edit_avatar = edit_avatar)